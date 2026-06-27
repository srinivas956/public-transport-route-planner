# 🚇 NaviDelhi: Urban Transit Intelligence

NaviDelhi is a comprehensive, web-based multi-modal public transport route planner designed for the Delhi NCR region. It integrates Metro, Bus, and Local Train networks to provide users with optimized journey planning, digital ticketing, and unified pass management.

## ✨ Key Features
* **Smart Route Optimization:** Utilizes Dijkstra's algorithm to calculate routes based on specific user preferences (Fastest Route, Least Transfers, Cheapest Fare).
* **Multi-Modal Integration:** Seamlessly connects DMRC Metro, DTC Buses, and EMU Local Trains into a single journey view.
* **Digital Wallet & E-Ticketing:** Users can purchase individual digital tickets or unified "Master Passes" powered by Razorpay integration.
* **Interactive Mapping:** Spatial visualization of routes and stations using Leaflet.js.
* **Admin Dashboard:** Comprehensive analytics panel for monitoring ticket sales, popular routes, and peak transit hours.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** MySQL (transit_db)
* **Algorithms:** Dijkstra's Algorithm (Pathfinding), Haversine Formula (Spatial distance)
* **Frontend:** HTML5, CSS3, JavaScript (Leaflet.js, Chart.js)
* **Integrations:** Razorpay API (Payments), Flask-Mail (OTP Verification)

## 🚀 Local Setup Instructions

1. Clone the repository: git clone https://github.com/srinivas956/public-transport-route-planner.git
2. Install dependencies: pip install -r requirements.txt
3. Import the database: Use the transit_db.sql file in your MySQL/phpMyAdmin setup.
4. Run the app: python app.py
