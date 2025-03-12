-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Mar 12, 2025 at 04:04 PM
-- Server version: 9.2.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `company`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` char(36) NOT NULL,
  `item_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_image` varchar(50) NOT NULL,
  `item_lat` varchar(50) NOT NULL,
  `item_lon` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_name`, `item_address`, `item_image`, `item_lat`, `item_lon`) VALUES
('e4c2995c-884a-4bba-86f9-7687db6cc4a7', '5', 'address 5', '5.webp', '', ''),
('26658a06-c2f7-4e23-893b-296d5c7261b5', '6', 'address 6', '6.webp', '', ''),
('8b11f1dc-65fc-4a62-b9c0-e8b83abb5dc9', 'Byens Lopper', 'Væreløse 20', '1.webp', '', ''),
('', 'd', 'd', 'd', '', ''),
('', 'hej', 'hej', '', 'hej', 'hej'),
('e0a33d1f-731b-47da-a10e-7dfd9d76e2cf', 'Københavns Loppetorv', 'Lundebakken 1, 2400 København NV.', '2.webp', '', ''),
('d29cd622-1927-475b-9e84-5dfc76f89e90', 'Loppetorv på Frederiksberg', 'Frederiksberg Rådhus. Smallegade 1, 2000 Frederiksberg', '3.webp', '', ''),
('5308e37a-53de-4b1f-960f-28757327ee40', 'Vera\s Marked Under Buen', 'Studiestræde 27. København K', '4.webp', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` bigint UNSIGNED NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_last_name` varchar(50) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_name`, `user_last_name`, `user_email`, `user_password`) VALUES
(4, 'a', 'aa', 'a@a.a', 'aaaaaa');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD UNIQUE KEY `item_name` (`item_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
