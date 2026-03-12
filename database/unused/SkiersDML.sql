-- DML Operations for Ski Resort Management System
-- -----------------------------------------------------
-- Skiers CRUD Operations
-- -----------------------------------------------------
-- create Skiers input
INSERT INTO `Skiers` (`Name`, `Address`, `Phone`, `Email`, `Ability`) 
VALUES ( @Name, @Address, @Phone, @Email, @Ability);

-- Read all Skiers
-- SELECT * FROM `Skiers`;

-- select a skier
SELECT SkierID, Name, Address, Phone, Email, Ability
FROM Skiers
WHERE SkierID = @SkierID;

-- Update a Skier's information
UPDATE `Skiers` 
SET `Name` = @Name, `Address` = @Address, `Phone` = @Phone, `Email` = @Email, `Ability` = @Ability 
WHERE `SkierID` = @SkierID;

-- Delete a Skier
DELETE FROM `Skiers` WHERE `SkierID` = @SkierID;

------------------------------------------------------
-- Trails CRUD Operations
-- -----------------------------------------------------
-- create Trails input
INSERT INTO `Trails` (`Name`, `Difficulty`, `Length`, `Status`) 
VALUES ( @Name, @Difficulty, @Length, @Status);


-- select all trails:
SELECT TrailID, TrailName, Difficulty, TrailLength, Status
FROM Trails;

-- select one of the trails
SELECT TrailID, TrailName, Difficulty, TrailLength, Status
FROM Trails
WHERE TrailID = @TrailID;


-- Update a Trail's information
UPDATE `Trails` 
SET `Name` = @Name, `Difficulty` = @Difficulty, `Length` = @Length, `Status` = @Status 
WHERE `TrailID` = @TrailID;
-- Delete a Trail
DELETE FROM `Trails` WHERE `TrailID` = @TrailID;
-- ---------------------------------------------------
-- SkiersTrails CRUD Operations
-- -----------------------------------------------------
-- create SkiersTrails input
INSERT INTO `SkiersTrails` (`Skiers_SkierID`, `Trails_TrailID`) VALUES ( @Skiers_SkierID, @Trails_TrailID);

-- Read all SkiersTrails
SELECT `SkiersTrailsID`, `Skiers_SkierID`, `Trails_TrailID`
FROM `SkiersTrails`
WHERE `SkiersTrailsID` = @SkiersTrailsID;

-- Update a SkiersTrails item's information
UPDATE `SkiersTrails` 
SET `Skiers_SkierID` = @Skiers_SkierID, `Trails_TrailID` = @Trails_TrailID
WHERE `SkiersTrailsID` = @SkiersTrailsID;
-- Delete a SkiersTrails item
DELETE FROM `SkiersTrails` WHERE `SkiersTrailsID` = @SkiersTrailsID;
------------------------------------------------------
-- Lifts CRUD Operations
-- -----------------------------------------------------
-- create Lifts input
INSERT INTO `Lifts` (`LiftNum`, `LiftName`, `TravelTime`, `ChairCapacity`, `Status`, `Altitude`) 
VALUES ( @LiftNum, @LiftName, @TravelTime, @ChairCapacity, @Status, @Altitude);


-- read all lifts:
SELECT LiftID, LiftNum, LiftName, TravelTime, ChairCapacity, Status, Altitude
FROM Lifts;

-- select on lift:
SELECT LiftID, LiftNum, LiftName, TravelTime, ChairCapacity, Status, Altitude
FROM Lifts
WHERE LiftID = @LiftID;

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
-- SELECT * FROM `SkiersLifts`;
-- Read a specific SkiersLifts item by ID
-- SELECT * FROM `SkiersLifts` WHERE `SkiersLiftsID` = @SkiersLiftsID;
-- Update a SkiersLifts item's information
UPDATE `SkiersLifts` 
SET `Skiers_SkierID` = @Skiers_SkierID, `Lifts_LiftID` = @Lifts_LiftID
WHERE `SkiersLiftsID` = @SkiersLiftsID;
-- Delete a SkiersLifts item
DELETE FROM `SkiersLifts` WHERE `SkiersLiftsID` = @SkiersLiftsID;

------------------------------------------------------
-- Passes CRUD Operations
-- -----------------------------------------------------
-- create Passes input
INSERT INTO `Passes` (`Type`, `PurchaseDate`, `ExpirationDate`, `Skiers_SkierID`) 
VALUES ( @Type, @PurchaseDate, @ExpirationDate, @Skiers_SkierID);

-- read one pass and join skier
SELECT Passes.PassID,
       Passes.Type,
       Passes.PurchaseDate,
       Passes.ExpirationDate,
       Skiers.Name AS SkierName
FROM Passes
JOIN Skiers
  ON Passes.Skiers_SkierID = Skiers.SkierID
WHERE Passes.PassID = @PassID;

-- Read a specific Pass by ID
-- SELECT * FROM `Passes` WHERE `PassID` = @PassID;

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
-- SELECT * FROM `RentalInventory`;
-- Read a specific RentalInventory item by ID
-- SELECT * FROM `RentalInventory` WHERE `RentalID` = @RentalID;
-- select rental id and type:
SELECT `RentalID`, `Type`
FROM `RentalInventory`
WHERE `RentalID` = @RentalID;

-- select all skiers and trails:
SELECT Skiers.Name,
       Trails.TrailName,
       Trails.Difficulty
FROM SkiersTrails
JOIN Skiers
  ON SkiersTrails.Skiers_SkierID = Skiers.SkierID
JOIN Trails
  ON SkiersTrails.Trails_TrailID = Trails.TrailID;

-- select all skiers and lifts:
SELECT Skiers.Name,
       Lifts.LiftName,
       Lifts.Altitude
FROM SkiersLifts
JOIN Skiers
  ON SkiersLifts.Skiers_SkierID = Skiers.SkierID
JOIN Lifts
  ON SkiersLifts.Lifts_LiftID = Lifts.LiftID;

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
-- SELECT * FROM `SkiersRentals`;
-- Read a specific SkiersRentals item by ID
-- SELECT * FROM `SkiersRentals` WHERE `SkiersRentalsID` = @SkiersRentalsID;
-- Update a SkiersRentals item's information
UPDATE `SkiersRentals` 
SET `Skiers_SkierID` = @Skiers_SkierID, `RentalInventory_RentalID` = @RentalInventory_RentalID
WHERE `SkiersRentalsID` = @SkiersRentalsID;
-- Delete a SkiersRentals item
DELETE FROM `SkiersRentals` WHERE `SkiersRentalsID` = @SkiersRentalsID;
