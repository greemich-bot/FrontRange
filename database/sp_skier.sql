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
    
    -- to call the sp and show the newely created id:
   -- call sp_CreateSkier('Joe smith', '123 st phx az', '6667778888', 'joes@email.com', 'Expert', @s_new_id)
   -- select @s_new_id as 'New Skier ID';
   
END //
DELIMITER ;  

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
-- UPDATE skiers
-- #############################
