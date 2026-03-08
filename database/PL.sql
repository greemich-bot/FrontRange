

# ------------------------------------------------------------------
# Skier Page PL/SQL
# ------------------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_CreateSkier;

DELIMITER //
create procedure sp_CreateSkier(
    in s_name varchar(45),
    in s_address varchar(255),
    in s_phone varchar(11),
    in s_email varchar(255),
    in s_ability varchar(255),
    out s_id int)
BEGIN
	insert INTO Skiers(Name, Address, Phone, Email, Ability)
    VALUES (s_name, s_address, s_phone, s_email, s_ability);
    
    -- store the skier id of the last inserted row:
    select last_insert_id() into s_id;
    -- then display id of the last inserted row
    select last_insert_id() AS 's_new_id';
   
END //
DELIMITER ;  

-- #############################
-- UPDATE Skiers
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateSkier;

DELIMITER //
CREATE PROCEDURE sp_UpdateSkier(
    IN s_id INT, 
    IN s_name VARCHAR(255), 
    IN s_address VARCHAR(255), 
    IN s_phone VARCHAR(50), 
    IN s_email VARCHAR(255), 
    IN s_ability VARCHAR(50)
)
BEGIN
    -- Verify if your column is 'id' or 'SkierID'
    UPDATE Skiers 
    SET Name = s_name, 
        Address = s_address, 
        Phone = s_phone, 
        Email = s_email, 
        Ability = s_ability 
    WHERE SkierID = s_id; -- Changed 'id' to 'SkierID' to match your Jinja2
END //
DELIMITER ;

-- #############################
-- DELETE Skiers
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteSkier;

DELIMITER //
CREATE PROCEDURE sp_DeleteSkier(IN s_id INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on any error
        ROLLBACK;
        -- Propogate the custom error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;
        -- Deleting corresponding rows from both Skiers table and 
        --      intersection table to prevent a data anamoly
        -- This can also be accomplished by using an 'ON DELETE CASCADE' constraint
        --      inside the SkiersLifts table.
        DELETE FROM Skiers WHERE SkierID = s_id;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Skiers for id: ', s_id);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;



# ------------------------------------------------------------------
# Pass Page PL/SQL
# ------------------------------------------------------------------
-- create pass sp
DROP PROCEDURE IF EXISTS sp_CreatePass;

DELIMITER //
create procedure sp_CreatePass(
    in p_type varchar(45),
    in p_purchaseDate DATETIME,
    in p_expirationDate DATETIME,
    in p_skiers_SkierID INT,
    out p_id int)
BEGIN
	insert INTO Passes(Type, PurchaseDate, ExpirationDate, Skiers_SkierID)
    VALUES (p_type, p_purchaseDate, p_expirationDate, p_skiers_SkierID);
    
    -- store the pass id of the last inserted row:
    select last_insert_id() into p_id;
    -- then display id of the last inserted row
    select last_insert_id() AS 'p_new_id';
    
   
END //
DELIMITER ;   

-- #############################
-- DELETE Passes
-- #############################
DROP PROCEDURE IF EXISTS sp_DeletePass;

DELIMITER //
CREATE PROCEDURE sp_DeletePass(IN p_id INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on any error
        ROLLBACK;
        -- Propogate the custom error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;
        -- Deleting corresponding rows from both Skiers table and 
        --      intersection table to prevent a data anamoly
        -- This can also be accomplished by using an 'ON DELETE CASCADE' constraint
        --      inside the SkiersLifts table.
        DELETE FROM Skiers WHERE Skiers_SkierID = p_id;
        DELETE FROM Passes WHERE PassID = p_id;
        

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Skiers for id: ', p_id);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;
