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

-- #############################
-- UPDATE skiers
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateSkier;

DELIMITER //
CREATE PROCEDURE sp_UpdateSkier(
    int s_id int,
    in s_name varchar,
    in s_address varchar,
    in s_phone varchar,
    in s_email varchar,
    in s_ability varchar
    )

BEGIN
    UPDATE Skiers SET 
        Name = s_name,
        Address = n s_address,
        Phone =  s_phone,
        Email =  s_email,
        Ability =  s_ability 
    WHERE SkierID = s_id; 
END //
DELIMITER ;