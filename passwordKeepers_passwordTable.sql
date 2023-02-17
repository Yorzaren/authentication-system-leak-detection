/* Create the database */
CREATE DATABASE IF NOT EXISTS passwordKeepers;
USE passwordKeepers;

--
-- Table structure for table `passwordTable`
--

DROP TABLE IF EXISTS `passwordTable`;
CREATE TABLE `passwordTable` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `IsAdmin` tinyint NOT NULL,
  `IsLockedOut` tinyint DEFAULT 0,
  `FailedLoginAttempts` int DEFAULT 0,
  `LastQueried` DATETIME DEFAULT NULL,
  `Password1` varchar(32) DEFAULT NULL,
  `Password2` varchar(32) DEFAULT NULL,
  `Password3` varchar(32) DEFAULT NULL,
  `Password4` varchar(32) DEFAULT NULL,
  `Password5` varchar(32) DEFAULT NULL,
  `Password6` varchar(32) DEFAULT NULL,
  `Password7` varchar(32) DEFAULT NULL,
  `Password8` varchar(32) DEFAULT NULL,
  `Password9` varchar(32) DEFAULT NULL,
  `Password10` varchar(32) DEFAULT NULL,
  `Password11` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
);