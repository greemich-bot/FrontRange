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
        DELETE FROM SkiersLifts WHERE Skiers_SkierID = s_id;
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