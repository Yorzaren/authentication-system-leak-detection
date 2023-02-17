/* 

Using MySQL DELIMITER for stored procedures

Typically, a stored procedure contains multiple statements separated by semicolons (;). 
To compile the whole stored procedure as a single compound statement, you need to temporarily change the delimiter from the semicolon (;) 
to another delimiter such as $$ or //

Note from: https://www.mysqltutorial.org/mysql-stored-procedure/mysql-delimiter/

*/

/* Allows for easy update of the stored procedure */
DROP PROCEDURE IF EXISTS AddNormalUser;
DROP PROCEDURE IF EXISTS AddAdminUser;
DROP PROCEDURE IF EXISTS GetTable;

/* Set the delimiter for the stored procedure */
DELIMITER //


CREATE PROCEDURE AddNormalUser(Username varchar(50), Password1 varchar(32), Password2 varchar(32), Password3 varchar(32), Password4 varchar(32), Password5 varchar(32), Password6 varchar(32), Password7 varchar(32), Password8 varchar(32), Password9 varchar(32), Password10 varchar(32), Password11 varchar(32))
BEGIN
    INSERT INTO passwordTable (Username, IsAdmin, IsLockedOut, FailedLoginAttempts, LastQueried, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10, Password11)
	VALUES (Username, 0, 0, 0, NOW(), Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10, Password11); 
END //

CREATE PROCEDURE AddAdminUser(Username varchar(50), Password1 varchar(32), Password2 varchar(32), Password3 varchar(32), Password4 varchar(32), Password5 varchar(32), Password6 varchar(32), Password7 varchar(32), Password8 varchar(32), Password9 varchar(32), Password10 varchar(32), Password11 varchar(32))
BEGIN
    INSERT INTO passwordTable (Username, IsAdmin, IsLockedOut, FailedLoginAttempts, LastQueried, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10, Password11)
	VALUES (Username, 1, 0, 0, NOW(), Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10, Password11); 
END //

CREATE PROCEDURE GetTable()
BEGIN
	SELECT *  FROM passwordTable;
END//

/* Set the delimiter back to normal */
DELIMITER ;