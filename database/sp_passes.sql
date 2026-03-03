

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
-- UPDATE passes
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdatePasses;

DELIMITER //
CREATE PROCEDURE sp_UpdatePasses(
    in p_type varchar(45),
    in p_purchaseDate DATETIME,
    in p_expirationDate DATETIME,
    in p_skiers_SkierID INT
)

BEGIN
    UPDATE passes SET 
        Type = p_type, 
        p_purchaseDate = PurchaseDate, 
        ExpirationDate = p_expirationDate, 
        Skiers_SkierID = p_skiers_SkierID; 
END //
DELIMITER ;

-- #############################
-- DELETE passes
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
        -- Deleting corresponding rows from both bsg_people table and 
        --      intersection table to prevent a data anamoly
        -- This can also be accomplished by using an 'ON DELETE CASCADE' constraint
        --      inside the bsg_cert_people table.
        DELETE FROM bsg_cert_people WHERE pid = p_id;
        DELETE FROM bsg_people WHERE id = p_id;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in bsg_people for id: ', p_id);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;
