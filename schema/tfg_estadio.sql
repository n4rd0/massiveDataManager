-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: tfg
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `estadio`
--

DROP TABLE IF EXISTS `estadio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estadio` (
  `idEstadio` int NOT NULL,
  `NombreEstadio` varchar(45) NOT NULL,
  `Capacidad` int NOT NULL,
  `Ubicacion` varchar(45) NOT NULL,
  `Secciones` int DEFAULT NULL,
  `Grupos` int DEFAULT NULL,
  `Filas` int DEFAULT NULL,
  `Asientos` int DEFAULT NULL,
  `PorcentajeLLeno` double DEFAULT '0',
  PRIMARY KEY (`idEstadio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estadio`
--

LOCK TABLES `estadio` WRITE;
/*!40000 ALTER TABLE `estadio` DISABLE KEYS */;
INSERT INTO `estadio` VALUES (0,'Teatro Real',1400,'Madrid',7,10,20,1,18.5),(1,'Cines Callao',1200,'Madrid',5,12,20,1,20.3333),(2,'Gran Teatre del Liceu',2100,'Barcenlona',7,12,25,1,12.619),(3,'Teatro de Rojas',720,'Toledo',4,10,18,1,34.1667),(4,'Teatro Arriaga Antzokia',1200,'Madrid',10,12,10,1,21.6667),(5,'Teatro Lope de Vega',1875,'Sevilla',5,15,25,1,13.1733),(6,'Gran Teatro Falla',1200,'Cadiz',6,10,20,1,19.75),(7,'Teatro Calderon',720,'Valladolid',4,10,18,1,33.6111);
/*!40000 ALTER TABLE `estadio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-09 15:10:16
