

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
