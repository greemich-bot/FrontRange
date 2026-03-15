

-- DML Operations for Ski Resort Management System
-- -----------------------------------------------------
-- Skiers CRUD Operations
-- -----------------------------------------------------
-- create Skiers input
INSERT INTO `Skiers` (`Name`, `Address`, `Phone`, `Email`, `Ability`) 
VALUES ( @Name, @Address, @Phone, @Email, @Ability);
-- Read all Skiers
SELECT * FROM `Skiers`;
-- Read a specific Skier by ID
-- SET @SkierID = 3;
SELECT * FROM `Skiers` WHERE `SkierID` = @SkierID
-- Delete a Skier
-- SET @SkierID = 5;
DELETE FROM `Skiers` WHERE `SkierID` = @SkierID;
-- Update a Skier
SET @SkierID = 1;
SET @Name = "John Smith";
SET @Address = "123 1ST St";
SET @Phone = "1234567891";
SET @Email = "js@example.com";
SET @Ability = "Expert";

UPDATE Skiers
    SET Name = @Name,
        Address = @Address,
        Phone = @Phone,
        Email = @Email,
        Ability = @Ability
    WHERE SkierID = @SkierID;

------------------------------------------------------
-- Lifts CRUD Operations
-- -----------------------------------------------------
-- create Lifts input
INSERT INTO `Lifts` (`LiftNum`, `LiftName`, `TravelTime`, `ChairCapacity`, `Status`, `Altitude`) 
VALUES ( @LiftNum, @LiftName, @TravelTime, @ChairCapacity, @Status, @Altitude);
-- Read all Lifts
SELECT * FROM `Lifts`; 
-- Read a specific Lift by ID
SELECT * FROM `Lifts` WHERE `LiftID` = @LiftID;
-- Update a Lift's information
UPDATE `Lifts` 
SET `LiftNum` = @LiftNum, `LiftName` = @LiftName, `TravelTime` = @TravelTime, `ChairCapacity` = @ChairCapacity, `Status` = @Status, `Altitude` = @Altitude
WHERE `LiftID` = @LiftID;
-- Delete a Lift
DELETE FROM `Lifts` WHERE `LiftID` = @LiftID;

------------------------------------------------------
-- SkiersLifts CRUD Operations
-- -----------------------------------------------------
-- create SkiersLifts input
INSERT INTO `SkiersLifts` (`Skiers_SkierID`, `Lifts_LiftID`) VALUES ( @Skiers_SkierID, @Lifts_LiftID);
-- Read all SkiersLifts
SELECT * FROM `SkiersLifts`;
-- Read a specific SkiersLifts item by ID
SELECT * FROM `SkiersLifts` WHERE `SkiersLiftsID` = @SkiersLiftsID;
-- Update a SkiersLifts item's information
UPDATE `SkiersLifts` 
SET `Skiers_SkierID` = @Skiers_SkierID, `Lifts_LiftID` = @Lifts_LiftID
WHERE `SkiersLiftsID` = @SkiersLiftsID;
-- Delete a SkiersLifts item
DELETE FROM `SkiersLifts` WHERE `SkiersLiftsID` = @SkiersLiftsID;

SELECT s.SkierID, s.Name, p.Type, t.TrailName, t.Difficulty
	FROM Passes AS p
	JOIN Skiers AS s
	ON p.PassID = s.SkierID
	JOIN SkiersTrails AS st
	ON s.SkierID = st.Skiers_SkierID
    JOIN Trails AS t
    ON st.Trails_TrailID = t.TrailID
    WHERE p.Type = "Full Season"
    GROUP By s.SkierID, s.Name
    HAVING AVG (t.TrailLength) > 1200;
------------------------------------------------------
-- Trails CRUD Operations
-- -----------------------------------------------------
-- create Trails input
INSERT INTO `Trails` (`TrailName`, `Difficulty`, `TrailLength`, `Status`) 
VALUES ( @TrailName, @Difficulty, @TrailLength, @Status);
-- Read all Trails
SELECT * FROM `Trails`; 
-- Read a specific Trail by ID
-- SET @TrailID = 4;
SELECT * FROM `Trails` WHERE `TrailID` = @TrailID;
-- Update a Trail's information
-- SET @TrailID = 3;
UPDATE `Trails` 
SET `Name` = @Name, `Difficulty` = @Difficulty, `TrailLength` = @TrailLength, `Status` = @Status 
WHERE `TrailID` = @TrailID;
-- Delete a Trail
-- SET @TrailID = 2;
DELETE FROM `Trails` WHERE `TrailID` = @TrailID;

-- ---------------------------------------------------
--SkiersTrails CRUD Operations
-- -----------------------------------------------------
-- create SkiersTrails input
INSERT INTO `SkiersTrails` (`Skiers_SkierID`, `Trails_TrailID`) VALUES ( @Skiers_SkierID, @Trails_TrailID);
-- Read all SkiersTrails
SELECT * FROM `SkiersTrails`;
-- Read a specific SkiersTrails item by ID
SELECT * FROM `SkiersTrails` WHERE `SkiersTrailsID` = @SkiersTrailsID;
-- Update a SkiersTrails item's information
UPDATE `SkiersTrails` 
SET `Skiers_SkierID` = @Skiers_SkierID, `Trails_TrailID` = @Trails_TrailID
WHERE `SkiersTrailsID` = @SkiersTrailsID;
-- Delete a SkiersTrails item
DELETE FROM `SkiersTrails` WHERE `SkiersTrailsID` = @SkiersTrailsID;

-- View to return Expert Skiers whose average Lift Altitude above 8000
CREATE VIEW ExpertSkiersWithHighAlt AS 
SELECT Skiers.SkierID, Skiers.Name, Lifts.LiftName, Lifts.Altitude
	FROM Skiers
	JOIN SkiersLifts
	ON Skiers.SkierID = SkiersLifts.Skiers_SkierID
	JOIN Lifts
	ON SkiersLifts.Lifts_LiftID = Lifts.LiftID
    WHERE Skiers.Ability = "Expert"
    GROUP By Skiers.SkierID, Skiers.Name
    HAVING AVG(Lifts.Altitude) > 8000;
    
 SELECT * FROM ExpertSkiersWithHighAlt;
------------------------------------------------------
-- Passes CRUD Operations
-- -----------------------------------------------------
-- create Passes input
INSERT INTO `Passes` (`Type`, `PurchaseDate`, `ExpirationDate`, `Skiers_SkierID`) 
VALUES ( @Type, @PurchaseDate, @ExpirationDate, @Skiers_SkierID);
-- Read all Passes
SELECT * FROM `Passes`;
-- Read a specific Pass by ID
SELECT * FROM `Passes` WHERE `PassID` = @PassID;
-- Update a Pass's information
UPDATE `Passes` 
SET `Type` = @Type, `PurchaseDate` = @PurchaseDate, `ExpirationDate` = @ExpirationDate, `Skiers_SkierID` = @Skiers_SkierID
WHERE `PassID` = @PassID;
-- Delete a Pass
DELETE FROM `Passes` WHERE `PassID` = @PassID;

------------------------------------------------------
-- Rentals CRUD Operations
-- -----------------------------------------------------
-- create RentalsInventory input
INSERT INTO `RentalInventory` (`Type`) VALUES ( @Type);
-- Read all RentalInventory
SELECT * FROM `RentalInventory`;
-- Read a specific RentalInventory item by ID
SELECT * FROM `RentalInventory` WHERE `RentalID` = @RentalID;
-- Update a RentalInventory item's information
UPDATE `RentalInventory` 
SET `Type` = @Type
WHERE `RentalID` = @RentalID;
-- Delete a RentalInventory item
DELETE FROM `RentalInventory` WHERE `RentalID` = @RentalID;

------------------------------------------------------
-- SkiersRentals CRUD Operations
-- -----------------------------------------------------
-- create SkiersRentals input
INSERT INTO `SkiersRentals` (`Skiers_SkierID`, `RentalInventory_RentalID`) VALUES ( @Skiers_SkierID, @RentalInventory_RentalID);
-- Read all SkiersRentals
SELECT * FROM `SkiersRentals`;
-- Read a specific SkiersRentals item by ID
SELECT * FROM `SkiersRentals` WHERE `SkiersRentalsID` = @SkiersRentalsID;
-- Update a SkiersRentals item's information
UPDATE `SkiersRentals` 
SET `Skiers_SkierID` = @Skiers_SkierID, `RentalInventory_RentalID` = @RentalInventory_RentalID
WHERE `SkiersRentalsID` = @SkiersRentalsID;
-- Delete a SkiersRentals item
DELETE FROM `SkiersRentals` WHERE `SkiersRentalsID` = @SkiersRentalsID;

-- Return all expert skiers and the equipment type they rented:
SELECT DISTINCT Skiers.Name, Skiers.Ability, RentalInventory.Type
	FROM Skiers
	JOIN SkiersRentals
	ON Skiers.SkierID = SkiersRentals.Skiers_SkierID
	JOIN RentalInventory
	ON SkiersRentals.RentalInventory_RentalID = RentalInventory.RentalID
	WHERE Skiers.Ability = "Expert"; 

