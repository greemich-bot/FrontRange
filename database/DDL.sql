DROP PROCEDURE IF EXISTS sp_load_front_range_data;
DELIMITER //
CREATE PROCEDURE sp_load_front_range_data()
BEGIN
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- CREATE SCHEMA IF NOT EXISTS `cs340_alyoois` DEFAULT CHARACTER SET utf8 ;
-- USE `cs340_alyoois` ;
-- -----------------------------------------------------
-- create Skiers Table
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Skiers`;
CREATE TABLE IF NOT EXISTS `Skiers` (
  `SkierID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `Address` VARCHAR(255) NULL,
  `Phone` VARCHAR(20) NULL,
  `Email` VARCHAR(255) NULL,
  `Ability` VARCHAR(45) NULL,
  PRIMARY KEY (`SkierID`)) -- add test comment!!
ENGINE = InnoDB;

INSERT INTO `Skiers` (`Name`, `Address`, `Phone`, `Email`, `Ability`) VALUES
('Alice Alpine', '123 Powder Lane', '5550101', 'alice@example.com', 'Expert'),
('Bob Backcountry', '456 Mogul Way', '5550202', 'bob@example.com', 'Intermediate'),
('Charlie Carver', '789 Shred St', '5550303', 'charlie@example.com', 'Beginner'),
('Diana Downhill', '321 Summit Rd', '5550404', 'diana@example.com', 'Advanced'),
('Ethan Edge', '654 Glacier Ave', '5550505', 'ethan@example.com', 'Intermediate'),
('Fiona Freestyle', '987 Aspen Dr', '5550606', 'fiona@example.com', 'Expert'),
('George Glide', '147 Snowcap Blvd', '5550707', 'george@example.com', 'Beginner'),
('Hannah Heli', '258 Powder Peak Ln', '5550808', 'hannah@example.com', 'Advanced');


-- -----------------------------------------------------
-- create Lifts Table
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Lifts`;
CREATE TABLE IF NOT EXISTS `Lifts` (
  `LiftID` INT NOT NULL AUTO_INCREMENT,
  `LiftNum` INT NOT NULL,
  `LiftName` VARCHAR(45) NOT NULL,
  `TravelTime` INT NOT NULL,
  `ChairCapacity` INT NOT NULL,
  `Status` TINYINT NOT NULL,
  `Altitude` INT NOT NULL,
  PRIMARY KEY (`LiftID`))
ENGINE = InnoDB;
-- Insert Lifts
INSERT INTO `Lifts` (`LiftNum`, `LiftName`, `TravelTime`, `ChairCapacity`, `Status`, `Altitude`) VALUES
(1, 'Chair 1', 8, 4, 1, 8500),
(2, 'Chair 2', 12, 4, 1, 9200),
(3, 'Chair 3', 5, 2, 1, 8900),
(4 , 'Gondola', 15, 8, 1, 9500);


-- -----------------------------------------------------
-- create SkiersLifts Table to serve as an intersection table for the many-to-many relationship between Skiers and Lifts
-- -----------------------------------------------------
DROP TABLE IF EXISTS `SkiersLifts`;
CREATE TABLE IF NOT EXISTS `SkiersLifts` (
  `SkiersLiftsID` INT NOT NULL AUTO_INCREMENT,
  `Lifts_LiftID` INT NOT NULL,
  `Skiers_SkierID` INT NOT NULL,
  PRIMARY KEY (`SkiersLiftsID`),
  CONSTRAINT `fk_SkiersLifts_Lifts`
    FOREIGN KEY (`Lifts_LiftID`)
    REFERENCES `Lifts` (`LiftID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SkiersLifts_Skiers`
    FOREIGN KEY (`Skiers_SkierID`)
    REFERENCES `Skiers` (`SkierID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

INSERT INTO `SkiersLifts` (`Lifts_LiftID`, `Skiers_SkierID`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1);


-- -----------------------------------------------------
-- create Trails Table
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Trails`;
CREATE TABLE IF NOT EXISTS `Trails` (
  `TrailID` INT NOT NULL AUTO_INCREMENT,
  `TrailName` VARCHAR(45) NOT NULL,
  `Difficulty` VARCHAR(45) NOT NULL,
  `TrailLength` INT NOT NULL,
  `Status` TINYINT NOT NULL,
  PRIMARY KEY (`TrailID`))
ENGINE = InnoDB;

-- Insert Trails
INSERT INTO `Trails` (`TrailName`, `Difficulty`, `TrailLength`, `Status`) VALUES
('Easy Street', 'Blue', 1500, 1),
('Moose Tracks', 'Green', 800, 1),
('Alpine Way', 'Blue', 1200, 1),
('Bluebell', 'Blue', 2000, 1),
('The Wall', 'Black', 1000, 1),
('Miner''s Alley', 'Green', 1800, 1),
('Avalanche Alley', 'Black', 2200, 0),
('The Grove', 'Black', 1900, 1),
('The Chute', 'Black', 1600, 1),
('Timberline', 'Blue', 1400, 1);



-- -----------------------------------------------------
-- create SkiersTrails Table to serve as an intersection table for the many-to-many relationship between Skiers and Trails
-- -----------------------------------------------------
DROP TABLE IF EXISTS `SkiersTrails`;
CREATE TABLE IF NOT EXISTS `SkiersTrails` (
  `SkiersTrailsID` INT NOT NULL AUTO_INCREMENT,
  `Skiers_SkierID` INT NOT NULL,
  `Trails_TrailID` INT NOT NULL,
  PRIMARY KEY (`SkiersTrailsID`),
  CONSTRAINT `fk_SkiersTrails_Skiers`
    FOREIGN KEY (`Skiers_SkierID`)
    REFERENCES `Skiers` (`SkierID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SkiersTrails_Trails`
    FOREIGN KEY (`Trails_TrailID`)
    REFERENCES `Trails` (`TrailID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

INSERT INTO `SkiersTrails` (`Skiers_SkierID`, `Trails_TrailID`) VALUES
(1, 1),
(2, 3),
(3, 2);
  
-- -----------------------------------------------------
-- create Pass Table
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Passes`;
CREATE TABLE IF NOT EXISTS `Passes` (
  `PassID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(45) NOT NULL,
  `PurchaseDate` DATETIME NOT NULL,
  `ExpirationDate` DATETIME NOT NULL,
  `Skiers_SkierID` INT NOT NULL,
  PRIMARY KEY (`PassID`),
  INDEX `fk_Pass_Skiers1_idx` (`Skiers_SkierID` ASC) VISIBLE,
  CONSTRAINT `fk_Pass_Skiers`
    FOREIGN KEY (`Skiers_SkierID`)
    REFERENCES `Skiers` (`SkierID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Insert Passes (linking to Skiers)
INSERT INTO `Passes` (`Type`, `PurchaseDate`, `ExpirationDate`, `Skiers_SkierID`) VALUES
('Full Season', '2023-11-01 09:00:00', '2024-05-01 23:59:59', 1),
('Day Pass', '2024-02-03 08:30:00', '2024-02-03 16:00:00', 2),
('3-Day Pass', '2024-02-04 12:00:00', '2024-02-06 16:00:00', 3);


-- -----------------------------------------------------
-- create RentalInventory Table
-- -----------------------------------------------------

DROP TABLE IF EXISTS `RentalInventory`;
CREATE TABLE IF NOT EXISTS `RentalInventory` (
  `RentalID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`RentalID`))
ENGINE = InnoDB;

INSERT INTO `RentalInventory` (`Type`) VALUES
('Performance Skis'),
('All-Mountain Skis'),
('Beginner Skis'),
('Snowboard'),
('Ski Boots'),
('Snowboard Boots'),
('Poles'),
('Helmet'), 
('Goggles');


-- -----------------------------------------------------
-- create SkiersRentals Table to serve as an intersection table for the many-to-many relationship between Skiers and Rental Inventory
-- -----------------------------------------------------
DROP TABLE IF EXISTS `SkiersRentals`;
CREATE TABLE IF NOT EXISTS `SkiersRentals` (
  `SkiersRentalsID` INT NOT NULL AUTO_INCREMENT,
  `Skiers_SkierID` INT NOT NULL,
  `RentalInventory_RentalID` INT NOT NULL,
  PRIMARY KEY (`SkiersRentalsID`),
  CONSTRAINT `fk_SkiersRentals_Skiers`
    FOREIGN KEY (`Skiers_SkierID`)
    REFERENCES `Skiers` (`SkierID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SkiersRentals_RentalInventory`
    FOREIGN KEY (`RentalInventory_RentalID`)
    REFERENCES `RentalInventory` (`RentalID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Intersection Table: Skier Rentals
INSERT INTO `SkiersRentals` (`Skiers_SkierID`, `RentalInventory_RentalID`) VALUES
(2, 2),
(3, 1),
(3, 3);






















SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

END //
DELIMITER ;
