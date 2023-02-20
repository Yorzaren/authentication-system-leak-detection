/* 

MySQL Database

This should be enough to generate the database and table needed for the program
- Create the database called passwordKeepers
- Create the table called passwordTable
- Create the stored procedures to be used by the python scripts to cut down on SQL commands in the scripts
- Add a default administrator account
        username: admin 
        password: password
- The password needs to be changed after setup to something more secure through the web interface.
- This is will ensure the decoy passwords are randomized based off the new password.

*/

--
-- Create the database
--

CREATE DATABASE IF NOT EXISTS passwordKeepers;
USE passwordKeepers;

--
-- Table structure for table `passwordTable`
--

DROP TABLE IF EXISTS `passwordTable`;
CREATE TABLE `passwordTable` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `IsAdmin` tinyint NOT NULL,
  `IsLockedOut` tinyint DEFAULT 0,
  `FailedLoginAttempts` int DEFAULT 0,
  `LastQueried` DATETIME DEFAULT NULL,
  `Password0` varchar(32) DEFAULT NULL,
  `Password1` varchar(32) DEFAULT NULL,
  `Password2` varchar(32) DEFAULT NULL,
  `Password3` varchar(32) DEFAULT NULL,
  `Password4` varchar(32) DEFAULT NULL,
  `Password5` varchar(32) DEFAULT NULL,
  `Password6` varchar(32) DEFAULT NULL,
  `Password7` varchar(32) DEFAULT NULL,
  `Password8` varchar(32) DEFAULT NULL,
  `Password9` varchar(32) DEFAULT NULL,
  `Password10` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Username`),
  KEY (`UID`), -- If this isn't marked as a key the table will break
  UNIQUE KEY `Username_UNIQUE` (`Username`)
);

--
-- Create stored procedures
--

/* 

Using MySQL DELIMITER for stored procedures

Typically, a stored procedure contains multiple statements separated by semicolons (;). 
To compile the whole stored procedure as a single compound statement, you need to temporarily change the delimiter from the semicolon (;) 
to another delimiter such as $$ or //

Note from: https://www.mysqltutorial.org/mysql-stored-procedure/mysql-delimiter/

*/

/* Allows for easy update of the stored procedure */
DROP PROCEDURE IF EXISTS GetTable;
DROP PROCEDURE IF EXISTS UserExists;
DROP PROCEDURE IF EXISTS AddAdminUser;
DROP PROCEDURE IF EXISTS AddNormalUser;
DROP PROCEDURE IF EXISTS DeleteUser;
DROP PROCEDURE IF EXISTS GetPasswords;
DROP PROCEDURE IF EXISTS UpdatePassword;
DROP PROCEDURE IF EXISTS IsUserAdmin;
DROP PROCEDURE IF EXISTS IsUserLockedOut;
DROP PROCEDURE IF EXISTS LockUser;
DROP PROCEDURE IF EXISTS UnlockUser;
DROP PROCEDURE IF EXISTS UpdateLastQuery;
DROP PROCEDURE IF EXISTS GetFailsCount;
DROP PROCEDURE IF EXISTS IncrementFails;
DROP PROCEDURE IF EXISTS ResetFails;
DROP PROCEDURE IF EXISTS GetAdminCount;

/* Set the delimiter for the stored procedure */
DELIMITER //

CREATE PROCEDURE GetTable()
BEGIN
	SELECT * FROM passwordTable;
END//

CREATE PROCEDURE UserExists(inputUsername varchar(50))
BEGIN
	SELECT COUNT(*) FROM passwordTable WHERE Username = inputUsername;
END//

CREATE PROCEDURE AddAdminUser(Username varchar(50), Password0 varchar(32), Password1 varchar(32), Password2 varchar(32), Password3 varchar(32), Password4 varchar(32), Password5 varchar(32), Password6 varchar(32), Password7 varchar(32), Password8 varchar(32), Password9 varchar(32), Password10 varchar(32))
BEGIN
    INSERT INTO passwordTable (Username, IsAdmin, IsLockedOut, FailedLoginAttempts, LastQueried, Password0, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10)
	VALUES (Username, 1, 0, 0, NOW(), Password0, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10); 
END //

CREATE PROCEDURE AddNormalUser(Username varchar(50), Password0 varchar(32), Password1 varchar(32), Password2 varchar(32), Password3 varchar(32), Password4 varchar(32), Password5 varchar(32), Password6 varchar(32), Password7 varchar(32), Password8 varchar(32), Password9 varchar(32), Password10 varchar(32))
BEGIN
    INSERT INTO passwordTable (Username, IsAdmin, IsLockedOut, FailedLoginAttempts, LastQueried, Password0, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10)
	VALUES (Username, 0, 0, 0, NOW(), Password0, Password1, Password2, Password3, Password4, Password5, Password6, Password7, Password8, Password9, Password10); 
END //

CREATE PROCEDURE DeleteUser(inputUsername varchar(50))
BEGIN
	DELETE FROM passwordTable
	WHERE Username = inputUsername;
END//

CREATE PROCEDURE GetPasswords(inputUsername varchar(50))
BEGIN
	SELECT
		Password0,
		Password1,
		Password2,
		Password3,
		Password4,
		Password5,
		Password6,
		Password7,
		Password8,
		Password9,
		Password10
    FROM passwordTable
	WHERE Username = inputUsername;
END//


CREATE PROCEDURE UpdatePassword(inputUsername varchar(50), updatedPassword0 varchar(32), updatedPassword1 varchar(32), updatedPassword2 varchar(32), updatedPassword3 varchar(32), updatedPassword4 varchar(32), updatedPassword5 varchar(32), updatedPassword6 varchar(32), updatedPassword7 varchar(32), updatedPassword8 varchar(32), updatedPassword9 varchar(32), updatedPassword10 varchar(32))
BEGIN
	UPDATE passwordTable 
	SET 
		Password0 = updatedPassword0,
		Password1 = updatedPassword1,
		Password2 = updatedPassword2,
		Password3 = updatedPassword3,
		Password4 = updatedPassword4,
		Password5 = updatedPassword5,
		Password6 = updatedPassword6,
		Password7 = updatedPassword7,
		Password8 = updatedPassword8,
		Password9 = updatedPassword9,
		Password10 = updatedPassword10
	WHERE
		Username = inputUsername;
END//

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

CREATE PROCEDURE GetFailsCount(inputUsername varchar(50))
BEGIN
	SELECT FailedLoginAttempts
    FROM passwordTable
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

CREATE PROCEDURE GetAdminCount()
BEGIN
	SELECT COUNT(*)
	FROM passwordTable
	WHERE IsAdmin = 1;
END//

/* Set the delimiter back to normal */
DELIMITER ;

--
-- Create the default admin account
--

CALL AddAdminUser("admin", "password", "password", "password", "password", "password", "password", "password", "password", "password", "password", "password");