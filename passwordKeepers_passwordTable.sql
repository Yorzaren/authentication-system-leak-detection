-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: passwordKeepers
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `passwordTable`
--

DROP TABLE IF EXISTS `passwordTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwordTable` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `IsAdmin` tinyint NOT NULL,
  `IsLockedOut` tinyint DEFAULT NULL,
  `FailedLoginAttempts` int NOT NULL,
  `LastQueried` date DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwordTable`
--

LOCK TABLES `passwordTable` WRITE;
/*!40000 ALTER TABLE `passwordTable` DISABLE KEYS */;
/*!40000 ALTER TABLE `passwordTable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-14 12:47:27
