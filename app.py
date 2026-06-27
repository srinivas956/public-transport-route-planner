from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import secrets
import time
import mysql.connector
import heapq
import os
import random
import math
import uuid
import razorpay
import re
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_dev_key_fallback')

app.config['SESSION_COOKIE_HTTPONLY']=True
app.config['SESSION_COOKIE_SECURE']=False   
app.config['SESSION_COOKIE_SAMESITE']='Lax'
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=1)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'moksh250225@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'moksh250225@gmail.com'

mail = Mail(app)

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def generate_otp():
    """Generates a 6-digit random OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, action_type="Login"):
    """Sends the OTP via Flask-Mail."""
    try:
        msg = Message(f"NaviDelhi - Your {action_type} OTP", recipients=[email])
        msg.body = f"Hello,\n\nYour One-Time Password (OTP) for {action_type} is: {otp}\n\nThis OTP is valid for 10 minutes.\n\nSecurely,\nNaviDelhi Team"
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="transit_db")

def fetch_graph_data():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stations")
    stations_data = {row['name']: {'lat': row['lat'], 'lng': row['lng'], 'type': row['type']} for row in cursor.fetchall()}
    cursor.execute("SELECT * FROM connections")
    graph_connections = {}
    for row in cursor.fetchall():
        src, dest = row['source'], row['destination']
        if src not in graph_connections:
            graph_connections[src] = []
        if dest not in graph_connections:
            graph_connections[dest] = []
        graph_connections[src].append((dest, row['time_mins'], row['mode'], row['line_name'], row['price']))
        graph_connections[dest].append((src, row['time_mins'], row['mode'], row['line_name'], row['price']))
    cursor.close()
    db.close()
    return stations_data, graph_connections

def find_route(start, end, stations_data, graph_connections, optimize_for='time'):
    tiebreaker = 0
    queue = [(0, tiebreaker, start, [], 0, 0, None)]
    visited = {}
    while queue:
        (curr_cost, _, u, path, curr_time, curr_price, curr_line) = heapq.heappop(queue)
        if u == end:
            return path, curr_time, curr_price
        state_key = (u, curr_line)
        if state_key in visited and visited[state_key] <= curr_cost:
            continue
        visited[state_key] = curr_cost
        for (v, time, mode, line, price) in graph_connections.get(u, []):
            is_transfer = 1 if (curr_line and curr_line != line) else 0
            if optimize_for == 'time':
                edge_cost = time + (4 if is_transfer else 0)
            elif optimize_for == 'price':
                edge_cost = price + (0.1 if is_transfer else 0)
            elif optimize_for == 'transfers':
                edge_cost = time + (1000 if is_transfer else 0)
            new_cost = curr_cost + edge_cost
            if (v, line) not in visited or new_cost < visited.get((v, line), float('inf')):
                step_details = {
                    'from': u,
                    'to': v,
                    'mode': mode,
                    'line': line,
                    'time': time,
                    'price': price,
                    'from_coords': stations_data[u],
                    'to_coords': stations_data[v]
                }
                tiebreaker += 1
                heapq.heappush(queue, (new_cost, tiebreaker, v, path + [step_details],
                                       curr_time + time, curr_price + price, line))
    return None, 0, 0

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

@app.route('/')
def index():
    stations_data, _ = fetch_graph_data()
    return render_template('index.html', locations=stations_data, current_user=session.get('user_name'))

@app.route('/support')
def support():
    return render_template('support.html', current_user=session.get('user_name'))

@app.route('/about')
def about():
    return render_template('about.html', current_user=session.get('user_name'))

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    start, end = data['start'], data['end']
    stations_data, graph_connections = fetch_graph_data()
    routes_found = []
    strategies = [('time', 'Best & Fastest'), ('transfers', 'Least Transfers'), ('price', 'Cheapest Fare')]
    for strategy, label in strategies:
        raw_path, total_time, total_price = find_route(start, end, stations_data, graph_connections, optimize_for=strategy)
        if not raw_path:
            continue
        path_fingerprint = tuple(step['to'] for step in raw_path)
        is_duplicate = False
        for existing_route in routes_found:
            if existing_route['fingerprint'] == path_fingerprint:
                existing_route['label'] += ' • ' + label.replace('Best & Fastest', 'Fastest')
                is_duplicate = True
                break
        if is_duplicate:
            continue
        processed_instructions = []
        transfer_count = 0
        current_ride = None
        
        for i, step in enumerate(raw_path):
            true_mode = 'walk' if 'Walking' in step['line'] else step['mode']
            if current_ride is None:
                current_ride = {
                    'type': 'ride',
                    'data': {
                        'from': step['from'],
                        'to': step['to'],
                        'mode': true_mode,
                        'line': step['line'],
                        'time': step['time'],
                        'price': step['price'],
                        'from_coords': step['from_coords'],
                        'to_coords': step['to_coords'],
                        'intermediate_stops': [] # <--- NEW: Initialize the list
                    }
                }
            else:
                if current_ride['data']['line'] == step['line']:
                    # <--- NEW: Add the station we just passed through to the list
                    current_ride['data']['intermediate_stops'].append({
                        'name': step['from'],
                        'coords': step['from_coords']
                    })
                    
                    current_ride['data']['to'] = step['to']
                    current_ride['data']['time'] += step['time']
                    current_ride['data']['price'] += step['price']
                    current_ride['data']['to_coords'] = step['to_coords']
                else:
                    processed_instructions.append(current_ride)
                    transfer_count += 1
                    processed_instructions.append({
                        'type': 'transfer',
                        'station': current_ride['data']['to'],
                        'next_line': step['line']
                    })
                    next_true_mode = 'walk' if 'Walking' in step['line'] else step['mode']
                    current_ride = {
                        'type': 'ride',
                        'data': {
                            'from': step['from'],
                            'to': step['to'],
                            'mode': next_true_mode,
                            'line': step['line'],
                            'time': step['time'],
                            'price': step['price'],
                            'from_coords': step['from_coords'],
                            'to_coords': step['to_coords'],
                            'intermediate_stops': [] # <--- NEW: Initialize the list
                        }
                    }
            if i == len(raw_path) - 1:
                processed_instructions.append(current_ride)
                processed_instructions.append({
                    'type': 'arrive',
                    'station': current_ride['data']['to'],
                    'coords': current_ride['data']['to_coords']
                })
        tickets = []
        current_ticket = None
        badges = []
        for inst in processed_instructions:
            if inst['type'] == 'ride':
                data_obj = inst['data']
                mode = data_obj['mode']
                if mode != 'walk' and data_obj['line'] not in badges:
                    badges.append(data_obj['line'])
                if mode == 'walk' or data_obj['price'] == 0:
                    continue
                need_new_ticket = False
                if current_ticket is None:
                    need_new_ticket = True
                elif mode != current_ticket['mode']:
                    need_new_ticket = True
                elif mode in ['bus', 'train']:
                    need_new_ticket = True
                if need_new_ticket:
                    if current_ticket:
                        tickets.append(current_ticket)
                    current_ticket = {'mode': mode, 'start': data_obj['from'], 'end': data_obj['to'], 'price': data_obj['price']}
                else:
                    current_ticket['end'] = data_obj['to']
                    current_ticket['price'] += data_obj['price']
        if current_ticket:
            tickets.append(current_ticket)
        routes_found.append({
            'label': label,
            'time': total_time,
            'price': total_price,
            'transfer_count': transfer_count,
            'instructions': processed_instructions,
            'tickets': tickets,
            'badges': badges,
            'fingerprint': path_fingerprint
        })
    if not routes_found:
        return jsonify({'success': False})
    db = get_db_connection()
    cursor = db.cursor()
    user_email = session.get('user_email')
    cursor.execute(
        "INSERT INTO search_logs (user_email, source, destination) VALUES (%s, %s, %s)",
        (user_email, start, end)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'routes': routes_found})

@app.route('/api/live-status', methods=['POST'])
def live_status():
    return jsonify({'success': True, 'station': request.json.get('station'), 't1': random.randint(1, 5), 't2': random.randint(6, 15)})

@app.route('/api/nearby', methods=['POST'])
def get_nearby():
    data = request.json
    user_lat, user_lng = data.get('lat'), data.get('lng')
    stations_data, _ = fetch_graph_data()
    closest = {'metro': {'name': '', 'dist': float('inf')}, 'bus': {'name': '', 'dist': float('inf')}, 'train': {'name': '', 'dist': float('inf')}}
    for name, info in stations_data.items():
        dist = haversine_distance(user_lat, user_lng, info['lat'], info['lng'])
        cat = 'metro' if info['type'] == 'interchange' else info['type']
        if dist < closest[cat]['dist']:
            closest[cat] = {'name': name, 'dist': round(dist, 1)}
    return jsonify({'success': True, 'closest': closest})

@app.route('/api/create-order', methods=['POST'])
def create_order():
    data = request.json
    amount_in_paise = int(float(data['price']) * 100)
    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"receipt_{uuid.uuid4().hex[:8]}",
        "notes": {"type": data.get('type', 'ticket')}
    }
    try:
        order = razorpay_client.order.create(data=order_data)
        return jsonify({'success': True, 'order_id': order['id'], 'amount': order_data['amount']})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/generate-ticket', methods=['POST'])
def generate_ticket():
    data = request.json
    email = session.get('user_email')
    if email:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user_tickets (user_email, start_station, end_station, price) VALUES (%s, %s, %s, %s)",
                       (email, data['start'], data['end'], data['price']))
        db.commit()
        cursor.close()
        db.close()
    secure_token = f"NAVIDELHI-TICKET-{uuid.uuid4().hex[:8].upper()}"
    return jsonify({'success': True, 'qr_data': f"TICKET ID: {secure_token} | Route: {data['start']} to {data['end']} | PAID: Rs.{data['price']}"})

@app.route('/api/generate-pass', methods=['POST'])
def generate_pass():
    data = request.json
    email = session.get('user_email')
    if email:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user_passes (user_email, tier_price) VALUES (%s, %s)",
                       (email, data['tier']))
        db.commit()
        cursor.close()
        db.close()
    secure_token = f"DELHI-MASTER-{uuid.uuid4().hex[:10].upper()}"
    return jsonify({'success': True, 'qr_data': f"MASTER PASS: {secure_token} | TIER: Rs.{data['tier']} | TYPE: All-Access Transit"})

@app.route('/api/my-wallet', methods=['GET'])
def my_wallet():
    email = session.get('user_email')
    if not email:
        return jsonify({'success': False, 'message': 'Not logged in'})
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_passes WHERE user_email = %s ORDER BY purchase_date DESC", (email,))
    passes = cursor.fetchall()
    cursor.execute("SELECT * FROM user_tickets WHERE user_email = %s ORDER BY purchase_date DESC", (email,))
    tickets = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'tickets': tickets, 'passes': passes})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required.'})
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already registered. Please log in.'})

    otp = generate_otp()
    password_hash = generate_password_hash(password)
    
    session['temp_reg_data'] = {
        'name': name,
        'email': email,
        'password_hash': password_hash,
        'otp': otp,
        'otp_time': time.time()
    }
    
    if send_otp_email(email, otp, "Registration"):
        return jsonify({'success': True, 'requires_otp': True, 'message': 'OTP sent to your email.'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP. Check server email config.'})

@app.route('/api/verify-register', methods=['POST'])
def verify_register():
    data = request.json
    user_otp = data.get('otp', '').strip()
    temp_data = session.get('temp_reg_data')
    
    if not temp_data:
        return jsonify({'success': False, 'message': 'Session expired. Please try registering again.'})
        
    if time.time() - temp_data['otp_time'] > 600: # 10 minutes expiry
        return jsonify({'success': False, 'message': 'OTP has expired.'})
        
    if user_otp != temp_data['otp']:
        return jsonify({'success': False, 'message': 'Invalid OTP. Please try again.'})
        
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (temp_data['name'], temp_data['email'], temp_data['password_hash'])
        )
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': 'Database error. Please try again.'})
    finally:
        cursor.close()
        db.close()
        
    session['user_name'] = temp_data['name']
    session['user_email'] = temp_data['email']
    session.permanent = True
    session.pop('temp_reg_data', None) 
    
    return jsonify({'success': True, 'message': 'Account created securely!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user and check_password_hash(user['password_hash'], password):
        otp = generate_otp()
        session['temp_login_data'] = {
            'name': user['name'],
            'email': user['email'],
            'otp': otp,
            'otp_time': time.time()
        }
        
        if send_otp_email(user['email'], otp, "Login"):
            return jsonify({'success': True, 'requires_otp': True, 'message': 'OTP sent to your email.'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send OTP.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password.'})

@app.route('/api/verify-login', methods=['POST'])
def verify_login():
    data = request.json
    user_otp = data.get('otp', '').strip()
    temp_data = session.get('temp_login_data')
    
    if not temp_data:
        return jsonify({'success': False, 'message': 'Session expired. Please try logging in again.'})
        
    if time.time() - temp_data['otp_time'] > 600:
        return jsonify({'success': False, 'message': 'OTP has expired.'})
        
    if user_otp != temp_data['otp']:
        return jsonify({'success': False, 'message': 'Invalid OTP. Please try again.'})
        
    session['user_name'] = temp_data['name']
    session['user_email'] = temp_data['email']
    session.permanent = True
    session.pop('temp_login_data', None) 
    
    return jsonify({'success': True, 'name': temp_data['name']})
    
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)
    session.pop('user_email', None)
    return jsonify({'success': True})

@app.route('/admin/login')
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
    admin = cursor.fetchone()
    cursor.close()
    db.close()
    if admin and check_password_hash(admin['password_hash'], password):
        session['admin_logged_in'] = True
        session['admin_email'] = admin['email']
        session['admin_username'] = admin['username']
        session.permanent = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid admin credentials'})

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')
    return render_template('admin.html')

@app.route('/admin/routes')
def admin_manage_routes():
    if not session.get('admin_logged_in'): return redirect('/admin/login')
    return render_template('admin_routes.html')

@app.route('/api/admin/users-report', methods=['GET'])
def admin_users_report():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    user_email = request.args.get('user_email')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    filter_type = request.args.get('filter_type', 'purchase')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if user_email:
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': 'User not found'}), 404
        tickets_query = "SELECT * FROM user_tickets WHERE user_email = %s"
        ticket_params = [user_email]
        if filter_type == 'purchase':
            if start_date:
                tickets_query += " AND purchase_date >= %s"
                ticket_params.append(start_date)
            if end_date:
                tickets_query += " AND purchase_date <= %s"
                ticket_params.append(end_date)
        tickets_query += " ORDER BY purchase_date DESC"
        cursor.execute(tickets_query, ticket_params)
        tickets = cursor.fetchall()
        passes_query = "SELECT * FROM user_passes WHERE user_email = %s"
        pass_params = [user_email]
        if filter_type == 'purchase':
            if start_date:
                passes_query += " AND purchase_date >= %s"
                pass_params.append(start_date)
            if end_date:
                passes_query += " AND purchase_date <= %s"
                pass_params.append(end_date)
        passes_query += " ORDER BY purchase_date DESC"
        cursor.execute(passes_query, pass_params)
        passes = cursor.fetchall()
        report = [{'user': user, 'tickets': tickets, 'passes': passes}]
    else:
        if filter_type == 'join' and (start_date or end_date):
            users_query = "SELECT id, name, email, created_at FROM users WHERE 1=1"
            params = []
            if start_date:
                users_query += " AND created_at >= %s"
                params.append(start_date)
            if end_date:
                users_query += " AND created_at <= %s"
                params.append(end_date)
            users_query += " ORDER BY created_at DESC"
            cursor.execute(users_query, params)
            users = cursor.fetchall()
        else:
            cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()
        report = []
        for user in users:
            tickets_query = "SELECT * FROM user_tickets WHERE user_email = %s"
            ticket_params = [user['email']]
            if filter_type == 'purchase':
                if start_date:
                    tickets_query += " AND purchase_date >= %s"
                    ticket_params.append(start_date)
                if end_date:
                    tickets_query += " AND purchase_date <= %s"
                    ticket_params.append(end_date)
            tickets_query += " ORDER BY purchase_date DESC"
            cursor.execute(tickets_query, ticket_params)
            tickets = cursor.fetchall()
            passes_query = "SELECT * FROM user_passes WHERE user_email = %s"
            pass_params = [user['email']]
            if filter_type == 'purchase':
                if start_date:
                    passes_query += " AND purchase_date >= %s"
                    pass_params.append(start_date)
                if end_date:
                    passes_query += " AND purchase_date <= %s"
                    pass_params.append(end_date)
            passes_query += " ORDER BY purchase_date DESC"
            cursor.execute(passes_query, pass_params)
            passes = cursor.fetchall()
            if filter_type == 'purchase' and (start_date or end_date):
                if tickets or passes:
                    report.append({'user': user, 'tickets': tickets, 'passes': passes})
            else:
                report.append({'user': user, 'tickets': tickets, 'passes': passes})
    cursor.close()
    db.close()
    return jsonify({'success': True, 'report': report})

@app.route('/api/admin/popular-routes', methods=['GET'])
def popular_routes():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT source, destination, COUNT(*) as count
        FROM search_logs
        GROUP BY source, destination
        ORDER BY count DESC
        LIMIT 10
    """)
    routes = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'routes': routes})

@app.route('/api/admin/pass-types', methods=['GET'])
def pass_types():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            CASE tier_price
                WHEN 50 THEN '1-Day Pass'
                WHEN 130 THEN '3-Day Pass'
                WHEN 250 THEN '7-Day Pass'
                ELSE 'Other'
            END AS tier_name,
            COUNT(*) as count
        FROM user_passes
        GROUP BY tier_price
        ORDER BY tier_price
    """)
    pass_types = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'pass_types': pass_types})

@app.route('/api/admin/popular-ticket-routes', methods=['GET'])
def popular_ticket_routes():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT CONCAT(start_station, ' → ', end_station) AS route, COUNT(*) as count
        FROM user_tickets
        GROUP BY start_station, end_station
        ORDER BY count DESC
        LIMIT 10
    """)
    routes = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'routes': routes})

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    session.pop('admin_username', None)
    return jsonify({'success': True})

@app.route('/api/admin/stations', methods=['GET'])
def admin_stations():
    if not session.get('admin_logged_in'): return jsonify({'success': False}), 401
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name FROM stations ORDER BY name")
    stations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'stations': stations})

@app.route('/api/admin/routes', methods=['GET', 'POST', 'DELETE'])
def admin_routes():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM connections ORDER BY source, destination")
        routes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify({'success': True, 'routes': routes})
        
    elif request.method == 'POST':
        data = request.json
        source = data.get('source')
        destination = data.get('destination')
        time_mins = data.get('time_mins')
        mode = data.get('mode')
        line_name = data.get('line_name')
        price = data.get('price')
        
        if not source or not destination or not mode or not line_name or time_mins is None or price is None:
            return jsonify({'success': False, 'message': 'All fields are required.'})
            
        if source == destination:
            return jsonify({'success': False, 'message': 'Source and destination cannot be the same.'})
        if time_mins <= 0:
            return jsonify({'success': False, 'message': 'Time must be positive.'})
        if price < 0:
            return jsonify({'success': False, 'message': 'Price cannot be negative.'})
        
        cursor.execute(
            "SELECT * FROM connections WHERE source=%s AND destination=%s AND mode=%s AND line_name=%s",
            (source, destination, mode, line_name)
        )
        if cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': 'This connection already exists.'})
        
        try:
            cursor.execute(
                "INSERT INTO connections (source, destination, time_mins, mode, line_name, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (source, destination, time_mins, mode, line_name, price)
            )
            cursor.execute(
                "INSERT INTO connections (source, destination, time_mins, mode, line_name, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (destination, source, time_mins, mode, line_name, price)
            )
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'success': True, 'message': 'Route added successfully.'})
        except Exception as e:
            db.rollback()
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': str(e)})
    
    elif request.method == 'DELETE':
        data = request.json
        source = data.get('source')
        destination = data.get('destination')
        line_name = data.get('line_name')
        if not source or not destination or not line_name:
            return jsonify({'success': False, 'message': 'Missing parameters.'})
        try:
            cursor.execute(
                "DELETE FROM connections WHERE source=%s AND destination=%s AND line_name=%s",
                (source, destination, line_name)
            )
            cursor.execute(
                "DELETE FROM connections WHERE source=%s AND destination=%s AND line_name=%s",
                (destination, source, line_name)
            )
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'success': True, 'message': 'Route deleted.'})
        except Exception as e:
            db.rollback()
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': str(e)})


@app.route('/api/admin/add-station', methods=['POST'])
def add_station():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.json
    name = data.get('name', '').strip()
    lat = data.get('lat')
    lng = data.get('lng')
    station_type = data.get('type', 'bus') 
    
    if not name or lat is None or lng is None:
        return jsonify({'success': False, 'message': 'Name, latitude, and longitude are required.'})
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid coordinates.'})
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO stations (name, lat, lng, type) VALUES (%s, %s, %s, %s)",
            (name, lat, lng, station_type)
        )
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'success': True, 'message': 'Station added successfully.'})
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/admin/all-stations', methods=['GET'])
def all_stations():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stations ORDER BY name")
    stations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({'success': True, 'stations': stations})
    
@app.route('/api/admin/delete-station', methods=['POST'])
def delete_station():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'message': 'Station name required.'})
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM connections WHERE source = %s OR destination = %s", (name, name))
        cursor.execute("DELETE FROM stations WHERE name = %s", (name,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'success': True, 'message': 'Station deleted.'})
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()
        return jsonify({'success': False, 'message': str(e)})
        
@app.route('/api/admin/financial-analytics', methods=['GET'])
def financial_analytics():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT date, SUM(revenue) as total_revenue
        FROM (
            SELECT DATE(purchase_date) as date, price as revenue FROM user_tickets
            UNION ALL
            SELECT DATE(purchase_date) as date, tier_price as revenue FROM user_passes
        ) AS combined_revenue
        WHERE date >= DATE(NOW()) - INTERVAL 7 DAY
        GROUP BY date
        ORDER BY date ASC
    """)
    daily_revenue = cursor.fetchall()
    
    cursor.execute("""
        SELECT HOUR(purchase_date) as hour_of_day, COUNT(*) as volume
        FROM user_tickets
        GROUP BY HOUR(purchase_date)
        ORDER BY hour_of_day ASC
    """)
    peak_hours = cursor.fetchall()
 
    cursor.execute("""
        SELECT CONCAT(start_station, ' → ', end_station) AS route, SUM(price) as total_revenue
        FROM user_tickets
        GROUP BY start_station, end_station
        ORDER BY total_revenue DESC
        LIMIT 5
    """)
    profitable_routes = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return jsonify({
        'success': True, 
        'daily_revenue': daily_revenue,
        'peak_hours': peak_hours,
        'profitable_routes': profitable_routes
    })

if __name__ == '__main__':
    app.run(debug=True)
    
