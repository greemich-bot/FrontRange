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
