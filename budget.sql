/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for budget
CREATE DATABASE IF NOT EXISTS `budget` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `budget`;

-- Dumping structure for table budget.accounts
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_general_ci NOT NULL,
  `currency` tinytext COLLATE utf8mb4_general_ci NOT NULL,
  `balance` decimal(20,2) NOT NULL DEFAULT (0),
  KEY `Index 1` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table budget.accounts: ~0 rows (approximately)
REPLACE INTO `accounts` (`id`, `name`, `currency`, `balance`) VALUES
	(1, 'PrivatBank Personal', 'UAH', 10000.00),
	(2, 'PrivatBank Social', 'UAH', 0.00),
	(3, 'PrivatBank PE', 'UAH', 0.00),
	(4, 'Cash UAH', 'UAH', 0.00),
	(5, 'Cash EUR', 'EUR', 0.00),
	(6, 'Cash USD', 'USD', 0.00);

-- Dumping structure for table budget.expenses
CREATE TABLE IF NOT EXISTS `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL DEFAULT '2024',
  `month` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `amount` decimal(10,2) DEFAULT '0.00',
  `total_in_month` decimal(10,2) DEFAULT '0.00',
  `total_in_year` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`,`year`,`category`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- Dumping data for table budget.expenses: ~6 rows (approximately)
REPLACE INTO `expenses` (`id`, `year`, `month`, `category`, `amount`, `total_in_month`, `total_in_year`) VALUES
	(1, 2023, 'April', 'Utilities', 2545.15, 2545.15, 2545.15),
	(2, 2023, 'April', 'Food', 2093.35, 4685.00, 4685.00),
	(3, 2023, 'April', 'Cigaretes', 261.00, 4946.00, 4946.00),
	(4, 2023, 'April', 'Alcohol', 899.21, 5845.21, 5845.21),
	(5, 2023, 'April', 'Gaming', 418.41, 6263.62, 6263.62);

-- Dumping structure for table budget.incomes
CREATE TABLE IF NOT EXISTS `incomes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL DEFAULT '2024',
  `month` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `exchange_rate` decimal(10,4) DEFAULT NULL,
  `income_usd` decimal(10,2) DEFAULT '0.00',
  `income_uah` decimal(10,2) DEFAULT '0.00',
  `single_tax` decimal(10,2) DEFAULT '0.00',
  `ssc` decimal(10,2) DEFAULT '1474.00',
  `total_taxes` decimal(10,2) DEFAULT '0.00',
  `clean_income` decimal(10,2) DEFAULT '0.00',
  `additional_income` decimal(10,2) DEFAULT '0.00',
  `expenses` decimal(10,2) DEFAULT '0.00',
  `total_left` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`,`year`,`month`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- Dumping data for table budget.incomes: ~1 rows (approximately)
REPLACE INTO `incomes` (`id`, `year`, `month`, `exchange_rate`, `income_usd`, `income_uah`, `single_tax`, `ssc`, `total_taxes`, `clean_income`, `additional_income`, `expenses`, `total_left`) VALUES
	(1, 2023, 'April', 36.5686, 300.00, 10970.58, 548.53, 1474.00, 2022.53, 8948.05, 5686.00, 6303.62, 8330.43),
	(4, 2024, 'December', 36.5646, 2000.00, 73129.20, 3656.46, 1474.00, 5130.46, 67998.74, 0.00, 0.00, 67998.74),
	(5, 2024, 'May', 36.5646, 2147.00, 78504.20, 3925.21, 1474.00, 5399.21, 73104.99, 2100.00, 0.00, 75204.99);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
