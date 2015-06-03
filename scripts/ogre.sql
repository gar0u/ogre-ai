--
CREATE DATABASE ogre;
USE ogre;
--

-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ogre
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Behaviors`
--

DROP TABLE IF EXISTS `Behaviors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Behaviors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `behaviorName` varchar(50) DEFAULT NULL,
  `gene` char(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Behaviors`
--

LOCK TABLES `Behaviors` WRITE;
/*!40000 ALTER TABLE `Behaviors` DISABLE KEYS */;
INSERT INTO `Behaviors` VALUES (1,'Brave','b'),(2,'Disciplined','d'),(3,'Cowardly','c');
/*!40000 ALTER TABLE `Behaviors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Games`
--

DROP TABLE IF EXISTS `Games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `turns` int(11) DEFAULT NULL,
  `cpDestroyed` tinyint(1) DEFAULT NULL,
  `ogreDestroyed` tinyint(1) DEFAULT NULL,
  `remainingDefensePoints` int(11) DEFAULT NULL,
  `victoryTypeID` int(11) NOT NULL,
  `gameID` char(36) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Games`
--

LOCK TABLES `Games` WRITE;
/*!40000 ALTER TABLE `Games` DISABLE KEYS */;
/*!40000 ALTER TABLE `Games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ogres`
--

DROP TABLE IF EXISTS `Ogres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ogres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gameID` int(11) NOT NULL,
  `remainingMissiles` int(11) DEFAULT NULL,
  `remainingMainBattery` int(11) DEFAULT NULL,
  `remainingSecondaryBatteries` int(11) DEFAULT NULL,
  `remainingAP` int(11) DEFAULT NULL,
  `remainingTread` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ogres`
--

LOCK TABLES `Ogres` WRITE;
/*!40000 ALTER TABLE `Ogres` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ogres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UnitTypes`
--

DROP TABLE IF EXISTS `UnitTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UnitTypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gene` char(2) DEFAULT NULL,
  `unitTypeName` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UnitTypes`
--

LOCK TABLES `UnitTypes` WRITE;
/*!40000 ALTER TABLE `UnitTypes` DISABLE KEYS */;
INSERT INTO `UnitTypes` VALUES (1,'I1','Infantry 1-1'),(2,'I2','Infantry 2-1'),(3,'I3','Infantry 3-1'),(4,'GV','GEV'),(5,'HV','Heavy Tank'),(6,'HZ','Howitzer'),(7,'MT','Missle Tank'),(8,'CP','Command Post');
/*!40000 ALTER TABLE `UnitTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Units`
--

DROP TABLE IF EXISTS `Units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unitTypeID` int(11) NOT NULL,
  `behaviorID` int(11) NOT NULL,
  `startingHex` char(4) DEFAULT NULL,
  `gameID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Units`
--

LOCK TABLES `Units` WRITE;
/*!40000 ALTER TABLE `Units` DISABLE KEYS */;
/*!40000 ALTER TABLE `Units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VictoryTypes`
--

DROP TABLE IF EXISTS `VictoryTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VictoryTypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rank` int(11) NOT NULL,
  `victoryTypeName` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VictoryTypes`
--

LOCK TABLES `VictoryTypes` WRITE;
/*!40000 ALTER TABLE `VictoryTypes` DISABLE KEYS */;
INSERT INTO `VictoryTypes` VALUES (1,6,'Complete OGRE victory'),(2,5,'OGRE victory'),(3,4,'Marginal OGRE victory'),(4,2,'Defense victory'),(5,3,'Marginal defense victory'),(6,1,'Complete defense victory');
/*!40000 ALTER TABLE `VictoryTypes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-12  0:39:16

--
USE mysql;
CREATE user 'ogre'@'localhost' identified by 'ogrepw';
GRANT ALL on ogre.* to 'ogre'@'localhost';
FLUSH PRIVILEGES;
--
