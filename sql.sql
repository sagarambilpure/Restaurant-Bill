SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `restaurant` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `restaurant`;

-- --------------------------------------------------------

--
-- Table structure for table `details`
--

CREATE TABLE `details` (
  `code` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `price` int(11) NOT NULL,
  `veg` tinyint(1) NOT NULL,
  `type` varchar(40) NOT NULL,
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `details`
--

INSERT INTO `details` (`code`, `name`, `price`, `veg`, `type`, `count`) VALUES
(1, 'Buttered Garlic Sticks', 170, 1, 'appetizer', 0),
(2, 'BBQ Brisket Nachos', 180, 1, 'appetizer', 0),
(3, 'Paneer Chilly', 200, 1, 'appetizer', 0),
(4, 'Chicken Lollypop', 200, 0, 'appetizer', 0),
(5, 'Chicken Teriyaki', 190, 0, 'appetizer', 0),
(6, 'Chicken Chilly', 180, 0, 'appetizer', 0),
(7, 'Paneer Makhanwala', 190, 1, 'main_course', 0),
(8, 'Veg Kadai', 210, 1, 'main_course', 0),
(9, 'Paneer Lababdar', 200, 1, 'main_course', 0),
(10, 'Paneer Patiala', 230, 1, 'main_course', 0),
(11, 'Butter Chicken', 210, 0, 'main_course', 0),
(12, 'Chicken Banjara', 225, 0, 'main_course', 0),
(13, 'Chicken Hyderabadi', 225, 0, 'main_course', 0),
(14, 'Shrimp Scampi', 225, 0, 'main_course', 0),
(15, 'Brewed Coffee', 120, 1, 'beverage', 0),
(16, 'Mocha', 110, 1, 'beverage', 0),
(17, 'Lemonade', 90, 1, 'beverage', 0),
(18, 'Bottled Water', 60, 1, 'beverage', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `details`
--
ALTER TABLE `details`
  ADD PRIMARY KEY (`code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `details`
--
ALTER TABLE `details`
  MODIFY `code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `test`;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
