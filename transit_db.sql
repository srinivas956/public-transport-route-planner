-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2026 at 11:50 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `transit_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `connections`
--

CREATE TABLE `connections` (
  `id` int(11) NOT NULL,
  `source` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `time_mins` int(11) NOT NULL,
  `mode` varchar(50) NOT NULL,
  `line_name` varchar(100) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `connections`
--

INSERT INTO `connections` (`id`, `source`, `destination`, `time_mins`, `mode`, `line_name`, `price`) VALUES
(1, 'Rithala', 'Netaji Subhash Place', 10, 'metro', 'Red Line', 20),
(2, 'Netaji Subhash Place', 'Rithala', 10, 'metro', 'Red Line', 20),
(3, 'Netaji Subhash Place', 'Kashmere Gate', 15, 'metro', 'Red Line', 30),
(4, 'Kashmere Gate', 'Netaji Subhash Place', 15, 'metro', 'Red Line', 30),
(5, 'Kashmere Gate', 'Dilshad Garden', 12, 'metro', 'Red Line', 25),
(6, 'Dilshad Garden', 'Kashmere Gate', 12, 'metro', 'Red Line', 25),
(7, 'Dilshad Garden', 'Shaheed Sthal (Ghaziabad)', 10, 'metro', 'Red Line', 20),
(8, 'Shaheed Sthal (Ghaziabad)', 'Dilshad Garden', 10, 'metro', 'Red Line', 20),
(9, 'Samaypur Badli', 'GTB Nagar', 10, 'metro', 'Yellow Line', 20),
(10, 'GTB Nagar', 'Samaypur Badli', 10, 'metro', 'Yellow Line', 20),
(11, 'GTB Nagar', 'Kashmere Gate', 8, 'metro', 'Yellow Line', 15),
(12, 'Kashmere Gate', 'GTB Nagar', 8, 'metro', 'Yellow Line', 15),
(13, 'Kashmere Gate', 'Rajiv Chowk', 10, 'metro', 'Yellow Line', 20),
(14, 'Rajiv Chowk', 'Kashmere Gate', 10, 'metro', 'Yellow Line', 20),
(15, 'Rajiv Chowk', 'Central Secretariat', 5, 'metro', 'Yellow Line', 10),
(16, 'Central Secretariat', 'Rajiv Chowk', 5, 'metro', 'Yellow Line', 10),
(17, 'Central Secretariat', 'Hauz Khas', 15, 'metro', 'Yellow Line', 25),
(18, 'Hauz Khas', 'Central Secretariat', 15, 'metro', 'Yellow Line', 25),
(19, 'Hauz Khas', 'Huda City Centre (Gurgaon)', 20, 'metro', 'Yellow Line', 40),
(20, 'Huda City Centre (Gurgaon)', 'Hauz Khas', 20, 'metro', 'Yellow Line', 40),
(21, 'Dwarka Sector 21', 'Rajouri Garden', 25, 'metro', 'Blue Line', 40),
(22, 'Rajouri Garden', 'Dwarka Sector 21', 25, 'metro', 'Blue Line', 40),
(23, 'Rajouri Garden', 'Karol Bagh', 15, 'metro', 'Blue Line', 25),
(24, 'Karol Bagh', 'Rajouri Garden', 15, 'metro', 'Blue Line', 25),
(25, 'Karol Bagh', 'Rajiv Chowk', 8, 'metro', 'Blue Line', 15),
(26, 'Rajiv Chowk', 'Karol Bagh', 8, 'metro', 'Blue Line', 15),
(27, 'Rajiv Chowk', 'Mandi House', 4, 'metro', 'Blue Line', 10),
(28, 'Mandi House', 'Rajiv Chowk', 4, 'metro', 'Blue Line', 10),
(29, 'Mandi House', 'Noida Sector 18', 20, 'metro', 'Blue Line', 30),
(30, 'Noida Sector 18', 'Mandi House', 20, 'metro', 'Blue Line', 30),
(31, 'Noida Sector 18', 'Noida Electronic City', 15, 'metro', 'Blue Line', 20),
(32, 'Noida Electronic City', 'Noida Sector 18', 15, 'metro', 'Blue Line', 20),
(33, 'Vaishali', 'Anand Vihar Terminal', 5, 'metro', 'Blue Line', 10),
(34, 'Anand Vihar Terminal', 'Vaishali', 5, 'metro', 'Blue Line', 10),
(35, 'Anand Vihar Terminal', 'Mandi House', 15, 'metro', 'Blue Line', 30),
(36, 'Mandi House', 'Anand Vihar Terminal', 15, 'metro', 'Blue Line', 30),
(37, 'Mandi House', 'ITO', 2, 'metro', 'Violet Line', 10),
(38, 'ITO', 'Mandi House', 2, 'metro', 'Violet Line', 10),
(39, 'ITO', 'Lajpat Nagar', 15, 'metro', 'Violet Line', 25),
(40, 'Lajpat Nagar', 'ITO', 15, 'metro', 'Violet Line', 25),
(41, 'Lajpat Nagar', 'Kalkaji Mandir', 10, 'metro', 'Violet Line', 20),
(42, 'Kalkaji Mandir', 'Lajpat Nagar', 10, 'metro', 'Violet Line', 20),
(43, 'Kalkaji Mandir', 'Badarpur Border', 15, 'metro', 'Violet Line', 30),
(44, 'Badarpur Border', 'Kalkaji Mandir', 15, 'metro', 'Violet Line', 30),
(45, 'Netaji Subhash Place', 'Rajouri Garden', 10, 'metro', 'Pink Line', 20),
(46, 'Rajouri Garden', 'Netaji Subhash Place', 10, 'metro', 'Pink Line', 20),
(47, 'Lajpat Nagar', 'Hazrat Nizamuddin (NZM)', 10, 'metro', 'Pink Line', 20),
(48, 'Hazrat Nizamuddin (NZM)', 'Lajpat Nagar', 10, 'metro', 'Pink Line', 20),
(49, 'Hauz Khas', 'Kalkaji Mandir', 12, 'metro', 'Magenta Line', 30),
(50, 'Kalkaji Mandir', 'Hauz Khas', 12, 'metro', 'Magenta Line', 30),
(51, 'New Delhi Rly Stn (NDLS)', 'Rajiv Chowk', 3, 'metro', 'Yellow Line', 10),
(52, 'Rajiv Chowk', 'New Delhi Rly Stn (NDLS)', 3, 'metro', 'Yellow Line', 10),
(53, 'New Delhi Rly Stn (NDLS)', 'Old Delhi Rly Stn (DLI)', 10, 'train', 'EMU Local', 5),
(54, 'Old Delhi Rly Stn (DLI)', 'New Delhi Rly Stn (NDLS)', 10, 'train', 'EMU Local', 5),
(55, 'New Delhi Rly Stn (NDLS)', 'Hazrat Nizamuddin (NZM)', 15, 'train', 'Express Train', 10),
(56, 'Hazrat Nizamuddin (NZM)', 'New Delhi Rly Stn (NDLS)', 15, 'train', 'Express Train', 10),
(57, 'Old Delhi Rly Stn (DLI)', 'Kashmere Gate', 5, 'metro', 'Violet Line', 10),
(58, 'Kashmere Gate', 'Old Delhi Rly Stn (DLI)', 5, 'metro', 'Violet Line', 10),
(59, 'Anand Vihar Terminal', 'New Delhi Rly Stn (NDLS)', 20, 'train', 'EMU Local', 10),
(60, 'New Delhi Rly Stn (NDLS)', 'Anand Vihar Terminal', 20, 'train', 'EMU Local', 10),
(61, 'Kashmere Gate', 'ISBT Kashmere Gate (Bus)', 2, 'bus', 'Walking Transfer', 0),
(62, 'ISBT Kashmere Gate (Bus)', 'Kashmere Gate', 2, 'bus', 'Walking Transfer', 0),
(63, 'Anand Vihar Terminal', 'ISBT Anand Vihar (Bus)', 2, 'bus', 'Walking Transfer', 0),
(64, 'ISBT Anand Vihar (Bus)', 'Anand Vihar Terminal', 2, 'bus', 'Walking Transfer', 0),
(65, 'Hazrat Nizamuddin (NZM)', 'ISBT Sarai Kale Khan', 5, 'bus', 'Feeder Bus', 5),
(66, 'ISBT Sarai Kale Khan', 'Hazrat Nizamuddin (NZM)', 5, 'bus', 'Feeder Bus', 5),
(67, 'ISBT Kashmere Gate (Bus)', 'ISBT Sarai Kale Khan', 25, 'bus', 'DTC 412', 15),
(68, 'ISBT Sarai Kale Khan', 'ISBT Kashmere Gate (Bus)', 25, 'bus', 'DTC 412', 15),
(69, 'ISBT Sarai Kale Khan', 'ISBT Anand Vihar (Bus)', 30, 'bus', 'DTC 534', 15),
(70, 'ISBT Anand Vihar (Bus)', 'ISBT Sarai Kale Khan', 30, 'bus', 'DTC 534', 15),
(71, 'Dilshad Garden', 'Seemapuri Bus Depot', 5, 'bus', 'DTC Local', 5),
(72, 'Seemapuri Bus Depot', 'Dilshad Garden', 5, 'bus', 'DTC Local', 5),
(73, 'Seemapuri Bus Depot', 'Nand Nagri Terminal', 8, 'bus', 'DTC 212', 10),
(74, 'Nand Nagri Terminal', 'Seemapuri Bus Depot', 8, 'bus', 'DTC 212', 10),
(75, 'Nand Nagri Terminal', 'Shahdara Terminal', 15, 'bus', 'DTC 212', 15),
(76, 'Shahdara Terminal', 'Nand Nagri Terminal', 15, 'bus', 'DTC 212', 15),
(77, 'Shahdara Terminal', 'ISBT Kashmere Gate (Bus)', 20, 'bus', 'DTC 333', 15),
(78, 'ISBT Kashmere Gate (Bus)', 'Shahdara Terminal', 20, 'bus', 'DTC 333', 15),
(79, 'Nand Nagri Terminal', 'Yamuna Vihar Depot', 10, 'bus', 'DTC 254', 10),
(80, 'Yamuna Vihar Depot', 'Nand Nagri Terminal', 10, 'bus', 'DTC 254', 10),
(81, 'Yamuna Vihar Depot', 'Bhajanpura Bus Stop', 5, 'bus', 'DTC 254', 5),
(82, 'Bhajanpura Bus Stop', 'Yamuna Vihar Depot', 5, 'bus', 'DTC 254', 5),
(83, 'Bhajanpura Bus Stop', 'ISBT Kashmere Gate (Bus)', 15, 'bus', 'DTC 258', 10),
(84, 'ISBT Kashmere Gate (Bus)', 'Bhajanpura Bus Stop', 15, 'bus', 'DTC 258', 10),
(85, 'Laxmi Nagar Bus Stand', 'Mandi House', 15, 'bus', 'DTC 73', 10),
(86, 'Mandi House', 'Laxmi Nagar Bus Stand', 15, 'bus', 'DTC 73', 10),
(87, 'Laxmi Nagar Bus Stand', 'ISBT Anand Vihar (Bus)', 12, 'bus', 'DTC 73', 10),
(88, 'ISBT Anand Vihar (Bus)', 'Laxmi Nagar Bus Stand', 12, 'bus', 'DTC 73', 10),
(89, 'GTB Nagar', 'Mukherjee Nagar Stand', 5, 'bus', 'DTC Feeder', 5),
(90, 'Mukherjee Nagar Stand', 'GTB Nagar', 5, 'bus', 'DTC Feeder', 5),
(91, 'Azadpur Terminal', 'Jahangirpuri Bus Depot', 12, 'bus', 'DTC 159', 10),
(92, 'Jahangirpuri Bus Depot', 'Azadpur Terminal', 12, 'bus', 'DTC 159', 10),
(93, 'Kalkaji Mandir', 'Nehru Place Bus Terminal', 5, 'bus', 'DTC 425', 10),
(94, 'Nehru Place Bus Terminal', 'Kalkaji Mandir', 5, 'bus', 'DTC 425', 10),
(95, 'AIIMS Bus Stop', 'Lajpat Nagar', 10, 'bus', 'DTC 522', 10),
(96, 'Lajpat Nagar', 'AIIMS Bus Stop', 10, 'bus', 'DTC 522', 10),
(97, 'Central Secretariat', 'Dhaula Kuan Bus Stop', 20, 'bus', 'DTC 720', 15),
(98, 'Dhaula Kuan Bus Stop', 'Central Secretariat', 20, 'bus', 'DTC 720', 15),
(99, 'Janakpuri District Center', 'Uttam Nagar Terminal', 10, 'bus', 'DTC 817', 10),
(100, 'Uttam Nagar Terminal', 'Janakpuri District Center', 10, 'bus', 'DTC 817', 10),
(101, 'Shivaji Stadium Terminal', 'Rajiv Chowk', 5, 'bus', 'Walking Transfer', 0),
(102, 'Rajiv Chowk', 'Shivaji Stadium Terminal', 5, 'bus', 'Walking Transfer', 0);

-- --------------------------------------------------------

--
-- Table structure for table `stations`
--

CREATE TABLE `stations` (
  `name` varchar(100) NOT NULL,
  `lat` float NOT NULL,
  `lng` float NOT NULL,
  `type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stations`
--

INSERT INTO `stations` (`name`, `lat`, `lng`, `type`) VALUES
('AIIMS Bus Stop', 28.567, 77.21, 'bus'),
('Anand Vihar Terminal', 28.6469, 77.316, 'interchange'),
('Ashram Chowk Bus Stop', 28.572, 77.26, 'bus'),
('Azadpur Terminal', 28.706, 77.175, 'bus'),
('Badarpur Border', 28.5032, 77.3018, 'metro'),
('Bawana Bus Depot', 28.798, 77.042, 'bus'),
('Bhajanpura Bus Stop', 28.705, 77.275, 'bus'),
('Central Secretariat', 28.6146, 77.2119, 'interchange'),
('Dhaula Kuan Bus Stop', 28.5921, 77.1612, 'bus'),
('Dilshad Garden', 28.6759, 77.3215, 'metro'),
('Dwarka Sector 21', 28.5524, 77.0583, 'interchange'),
('GTB Nagar', 28.698, 77.2065, 'metro'),
('Hauz Khas', 28.543, 77.2065, 'interchange'),
('Hazrat Nizamuddin (NZM)', 28.587, 77.251, 'train'),
('Huda City Centre (Gurgaon)', 28.4594, 77.0725, 'metro'),
('India Gate Bus Stop', 28.612, 77.229, 'bus'),
('ISBT Anand Vihar (Bus)', 28.6475, 77.315, 'bus'),
('ISBT Kashmere Gate (Bus)', 28.667, 77.229, 'bus'),
('ISBT Sarai Kale Khan', 28.588, 77.253, 'bus'),
('ITO', 28.6289, 77.2432, 'metro'),
('Jahangirpuri Bus Depot', 28.725, 77.163, 'bus'),
('Janakpuri District Center', 28.628, 77.078, 'bus'),
('Kalkaji Mandir', 28.549, 77.255, 'interchange'),
('Karol Bagh', 28.643, 77.187, 'metro'),
('Kashmere Gate', 28.6675, 77.23, 'interchange'),
('Kendriya Terminal', 28.62, 77.205, 'bus'),
('Lajpat Nagar', 28.57, 77.237, 'interchange'),
('Laxmi Nagar Bus Stand', 28.63, 77.276, 'bus'),
('Malviya Nagar Bus Stop', 28.535, 77.21, 'bus'),
('Mandi House', 28.6258, 77.2343, 'interchange'),
('Mayur Vihar Ph-1 Terminal', 28.605, 77.295, 'bus'),
('Mayur Vihar Ph-3 Bus Stop', 28.6, 77.33, 'bus'),
('Mehrauli Bus Stand', 28.518, 77.182, 'bus'),
('Mukherjee Nagar Stand', 28.712, 77.2, 'bus'),
('Najafgarh Terminal', 28.61, 76.98, 'bus'),
('Nand Nagri Terminal', 28.696, 77.312, 'bus'),
('Nehru Place Bus Terminal', 28.55, 77.25, 'bus'),
('Netaji Subhash Place', 28.6963, 77.1519, 'interchange'),
('New Delhi Rly Stn (NDLS)', 28.6429, 77.2191, 'train'),
('Noida Electronic City', 28.627, 77.372, 'metro'),
('Noida Sector 18', 28.5708, 77.3262, 'metro'),
('Okhla Bus Depot', 28.535, 77.276, 'bus'),
('Old Delhi Rly Stn (DLI)', 28.66, 77.227, 'train'),
('Paharganj Police Station (Bus)', 28.645, 77.212, 'bus'),
('Palam Village Bus Stand', 28.585, 77.085, 'bus'),
('Peeragarhi Bus Depot', 28.68, 77.095, 'bus'),
('Pitampura TV Tower Bus Stop', 28.697, 77.141, 'bus'),
('Punjabi Bagh Terminal', 28.665, 77.13, 'bus'),
('Rajiv Chowk', 28.6328, 77.2197, 'interchange'),
('Rajouri Garden', 28.6495, 77.1215, 'interchange'),
('Rithala', 28.7208, 77.1071, 'metro'),
('Rohini Sector 15 Depot', 28.73, 77.13, 'bus'),
('Rohini Sector 22 Depot', 28.72, 77.07, 'bus'),
('Safdarjung Terminal', 28.575, 77.205, 'bus'),
('Saket Terminal', 28.52, 77.215, 'bus'),
('Samaypur Badli', 28.7456, 77.1378, 'metro'),
('Seemapuri Bus Depot', 28.682, 77.324, 'bus'),
('Shahdara Terminal', 28.675, 77.294, 'bus'),
('Shaheed Sthal (Ghaziabad)', 28.6712, 77.4159, 'metro'),
('Shivaji Stadium Terminal', 28.631, 77.213, 'bus'),
('Uttam Nagar Terminal', 28.621, 77.066, 'bus'),
('Vaishali', 28.65, 77.34, 'metro'),
('Vasant Kunj Sector C', 28.535, 77.155, 'bus'),
('Yamuna Vihar Depot', 28.701, 77.283, 'bus');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `connections`
--
ALTER TABLE `connections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `source` (`source`),
  ADD KEY `destination` (`destination`);

--
-- Indexes for table `stations`
--
ALTER TABLE `stations`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `connections`
--
ALTER TABLE `connections`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `connections`
--
ALTER TABLE `connections`
  ADD CONSTRAINT `connections_ibfk_1` FOREIGN KEY (`source`) REFERENCES `stations` (`name`),
  ADD CONSTRAINT `connections_ibfk_2` FOREIGN KEY (`destination`) REFERENCES `stations` (`name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
