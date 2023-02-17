/* 

Using MySQL DELIMITER for stored procedures

Typically, a stored procedure contains multiple statements separated by semicolons (;). 
To compile the whole stored procedure as a single compound statement, you need to temporarily change the delimiter from the semicolon (;) 
to another delimiter such as $$ or //

Note from: https://www.mysqltutorial.org/mysql-stored-procedure/mysql-delimiter/

*/

/* Allows for easy update of the stored procedure */
DROP PROCEDURE IF EXISTS GetTable;
DROP PROCEDURE IF EXISTS AddNormalUser;
DROP PROCEDURE IF EXISTS AddAdminUser;
DROP PROCEDURE IF EXISTS IsUserAdmin;
DROP PROCEDURE IF EXISTS IsUserLockedOut;
DROP PROCEDURE IF EXISTS LockUser;
DROP PROCEDURE IF EXISTS UnlockUser;
DROP PROCEDURE IF EXISTS UpdateLastQuery;
DROP PROCEDURE IF EXISTS IncrementFails;
DROP PROCEDURE IF EXISTS ResetFails;

/* Set the delimiter for the stored procedure */
DELIMITER //

CREATE PROCEDURE GetTable()
BEGIN
	SELECT *  FROM passwordTable;
END//

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

CREATE PROCEDURE IsUserAdmin(inputUsername varchar(50))
BEGIN
	SELECT COUNT(*) FROM passwordTable WHERE (Username = inputUsername AND IsAdmin = 1);
END//

CREATE PROCEDURE IsUserLockedOut(inputUsername varchar(50))
BEGIN
	SELECT COUNT(*) FROM passwordTable WHERE (Username = inputUsername AND IsLockedOut = 1);
END//

CREATE PROCEDURE LockUser(inputUsername varchar(50))
BEGIN
	UPDATE passwordTable
	SET IsLockedOut = 1
    WHERE Username = inputUsername;
END//

CREATE PROCEDURE UnlockUser(inputUsername varchar(50))
BEGIN
	UPDATE passwordTable
	SET IsLockedOut = 0
    WHERE Username = inputUsername;
END//

CREATE PROCEDURE UpdateLastQuery(inputUsername varchar(50))
BEGIN
	UPDATE passwordTable
	SET LastQueried = NOW()
    WHERE Username = inputUsername;
END//

CREATE PROCEDURE IncrementFails(inputUsername varchar(50))
BEGIN
	SET @currentFailCount = (SELECT FailedLoginAttempts FROM passwordTable WHERE Username=inputUsername);
	UPDATE passwordTable
	SET FailedLoginAttempts = @currentFailCount + 1
	WHERE Username = inputUsername;
END//

CREATE PROCEDURE ResetFails(inputUsername varchar(50))
BEGIN
	UPDATE passwordTable
	SET FailedLoginAttempts = 0
	WHERE Username = inputUsername;
END//

/* Set the delimiter back to normal */
DELIMITER ;