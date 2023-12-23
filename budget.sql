SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for expenses
-- ----------------------------
DROP TABLE IF EXISTS `expenses`;
CREATE TABLE `expenses`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL DEFAULT 2024,
  `month` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `amount` decimal(10, 2) NULL DEFAULT 0.00,
  `total_in_month` decimal(10, 2) NULL DEFAULT 0.00,
  `total_in_year` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`id`, `year`, `category`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of expenses
-- ----------------------------
INSERT INTO `expenses` VALUES (1, 2023, 'April', 'Utilities', 2545.15, 2545.15, 2545.15);
INSERT INTO `expenses` VALUES (2, 2023, 'April', 'Food', 2093.35, 4685.00, 4685.00);
INSERT INTO `expenses` VALUES (3, 2023, 'April', 'Cigaretes', 261.00, 4946.00, 4946.00);
INSERT INTO `expenses` VALUES (4, 2023, 'April', 'Alcohol', 899.21, 5845.21, 5845.21);
INSERT INTO `expenses` VALUES (5, 2023, 'April', 'Gaming', 418.41, 6263.62, 6263.62);
INSERT INTO `expenses` VALUES (6, 2023, 'April', 'Transport', 40.00, 6303.62, 6303.62);

-- ----------------------------
-- Table structure for incomes
-- ----------------------------
DROP TABLE IF EXISTS `incomes`;
CREATE TABLE `incomes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL DEFAULT 2024,
  `month` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `exchange_rate` decimal(10, 4) NULL DEFAULT NULL,
  `income_usd` decimal(10, 2) NULL DEFAULT 0.00,
  `income_uah` decimal(10, 2) NULL DEFAULT 0.00,
  `single_tax` decimal(10, 2) NULL DEFAULT 0.00,
  `ssc` decimal(10, 2) NULL DEFAULT 1474.00,
  `total_taxes` decimal(10, 2) NULL DEFAULT 0.00,
  `clean_income` decimal(10, 2) NULL DEFAULT 0.00,
  `additional_income` decimal(10, 2) NULL DEFAULT 0.00,
  `expenses` decimal(10, 2) NULL DEFAULT 0.00,
  `total_left` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`id`, `year`, `month`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of incomes
-- ----------------------------
INSERT INTO `incomes` VALUES (1, 2023, 'April', 36.5686, 300.00, 10970.58, 548.53, 1474.00, 2022.53, 8948.05, 5686.00, 6303.62, 8330.43);

SET FOREIGN_KEY_CHECKS = 1;
