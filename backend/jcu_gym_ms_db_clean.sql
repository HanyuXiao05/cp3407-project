
-- Host: 127.0.0.1    Database: jcu_gym_ms
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `BOOKING_Ref` varchar(12) NOT NULL,
  `MEMBER_ID` int NOT NULL,
  `SESSION_ID` int NOT NULL,
  `BOOKING_Date` date NOT NULL,
  `BOOKING_Time` time NOT NULL,
  `BOOKING_Status` enum('Booked','Deleted','Attended','No-Show') NOT NULL,
  PRIMARY KEY (`BOOKING_Ref`),
  KEY `fk_SESSION_has_MEMBER_MEMBER1_idx` (`MEMBER_ID`),
  KEY `fk_SESSION_has_MEMBER_SESSION1_idx` (`SESSION_ID`),
  CONSTRAINT `fk_SESSION_has_MEMBER_MEMBER1` FOREIGN KEY (`MEMBER_ID`) REFERENCES `member` (`MEMBER_ID`),
  CONSTRAINT `fk_SESSION_has_MEMBER_SESSION1` FOREIGN KEY (`SESSION_ID`) REFERENCES `session` (`SESSION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `MEMBER_ID` int NOT NULL,
  `MEMBER_Title` enum('Mr','Mrs','Ms') NOT NULL,
  `MEMBER_Name` varchar(45) NOT NULL,
  `MEMBER_Gender` enum('Male','Female') NOT NULL,
  `MEMBER_DOB` date NOT NULL,
  `MEMBER_Phone` varchar(20) NOT NULL,
  `MEMBER_Email` varchar(100) NOT NULL,
  `MEMBER_EmgContactName` varchar(45) DEFAULT NULL,
  `MEMBER_EmgContactPhone` varchar(20) DEFAULT NULL,
  `MEMBER_PwdHash` char(60) NOT NULL,
  `MEMBER_Type` enum('Student','Staff') NOT NULL,
  PRIMARY KEY (`MEMBER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership` (
  `MEMBERSHIP_ID` int NOT NULL,
  `MEMBER_ID` int NOT NULL,
  `MEM_TYPE_ID` int NOT NULL,
  `MEMBERSHIP_StartDate` date NOT NULL,
  `MEMBERSHIP_ExpDate` date NOT NULL,
  `MEMBERSHIP_Declared` tinyint NOT NULL,
  PRIMARY KEY (`MEMBERSHIP_ID`),
  KEY `fk_MEMBERSHIP_MEMBER1_idx` (`MEMBER_ID`),
  KEY `fk_MEMBERSHIP_MEMBERSHIP_TYPE1_idx` (`MEM_TYPE_ID`),
  CONSTRAINT `fk_MEMBERSHIP_MEMBER1` FOREIGN KEY (`MEMBER_ID`) REFERENCES `member` (`MEMBER_ID`),
  CONSTRAINT `fk_MEMBERSHIP_MEMBERSHIP_TYPE1` FOREIGN KEY (`MEM_TYPE_ID`) REFERENCES `membership_type` (`MEM_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership_type`
--

DROP TABLE IF EXISTS `membership_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership_type` (
  `MEM_TYPE_ID` int NOT NULL,
  `MEM_TYPE_Name` varchar(45) NOT NULL,
  `MEM_TYPE_Fee` decimal(6,2) NOT NULL,
  PRIMARY KEY (`MEM_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership_type`
--

LOCK TABLES `membership_type` WRITE;
/*!40000 ALTER TABLE `membership_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `membership_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `PAYMENT_ID` int NOT NULL,
  `MEMBERSHIP_ID` int NOT NULL,
  `PAYMENT_Date` date NOT NULL,
  `PAYMENT_TotalFee` decimal(6,2) NOT NULL,
  `PAYMENT_Type` enum('Cash','Cheque','NETS','MasterCard','Visa','Amex','Union Pay','Salary Deduction') NOT NULL,
  `PAYMENT_RcptNum` varchar(20) DEFAULT NULL,
  `PAYMENT_RcptVerifiedBy` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`PAYMENT_ID`),
  KEY `fk_PAYMENT_MEMBERSHIP1_idx` (`MEMBERSHIP_ID`),
  CONSTRAINT `fk_PAYMENT_MEMBERSHIP1` FOREIGN KEY (`MEMBERSHIP_ID`) REFERENCES `membership` (`MEMBERSHIP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `SESSION_ID` int NOT NULL,
  `SESSION_Date` date NOT NULL,
  `SESSION_Time` time NOT NULL,
  `SESSION_Capacity` int NOT NULL,
  PRIMARY KEY (`SESSION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-20 20:00:51
