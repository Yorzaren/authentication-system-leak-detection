"""
database_controller.py requires a connection to the database so can't be tested automatically on GitHub.

The test should skip

Make sure the database is running and is database entries are fresh from initialize_database.sql

If the database isn't in default config, then the test will throw errors.
"""
import os  # Used to get the .env file

import mysql.connector
import pytest
from dotenv import load_dotenv  # Used to load info from the .env file

from python_scripts import database_controller as db

load_dotenv()  # Load the secrets from the .env file


class TestDatabaseController:
    # Skip if not able to make a database connection because password missing in .env
    # @pytest.mark.skip(reason="DISABLED")
    @pytest.mark.skipif(not os.environ.get("DB_PASSWORD"), reason="No database connection")
    def test_db_functions(self):
        print("\n-->Resetting the system back to the default state\n")
        database_password = os.environ.get("DB_PASSWORD")
        db_config = {"user": "root", "password": database_password, "host": "127.0.0.1", "database": "passwordKeepers"}
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        my_cursor.execute("CALL ResetDatabase()")
        # Commit the changes and close
        cnx.commit()
        cnx.close()

        print("\n----- database_controller test -----\n->Make sure you have the system in the default state\n")
        print("Check case-sensitivity...")
        assert db.is_admin("Admin") is False
        assert db.is_admin("admin") is True

        print("Check if users exist...")
        assert db.user_exists("nonperson") is False
        assert db.user_exists("testuser") is False
        assert db.user_exists("testadmin") is False
        assert db.user_exists("admin") is True

        print("Print the default table...")

        db.print_table()

        array = ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8", "test9", "test10", "test11"]
        array2 = [
            "random1",
            "random2",
            "random3",
            "random4",
            "random5",
            "random6",
            "random7",
            "random8",
            "random9",
            "random10",
            "random11",
        ]

        db.add_user("testuser", array)  # add normal user
        db.add_user("testadmin", array, True)  # add admin user

        print("Check if they were added...")
        assert db.user_exists("testuser") is True
        assert db.user_exists("testadmin") is True
        assert db.user_exists("admin") is True

        db.print_table()

        print("Get passwords from testadmin...")
        pw = db.get_passwords("testadmin")
        assert pw == array

        db.update_password("testadmin", array2)
        pw = db.get_passwords("testadmin")

        assert pw != array  # Check that it changed the passwords
        assert pw == array2  # Check that the passwords are the same as we set it to.

        db.print_table()

        print("Checking the failed counter...")
        assert db.get_failed_count("testuser") == 0
        db.increment_failed_attempts("testuser")
        assert db.get_failed_count("testuser") == 1
        db.increment_failed_attempts("testuser")
        db.increment_failed_attempts("testuser")
        assert db.get_failed_count("testuser") == 3

        db.print_table()

        print("Reset counter for testuser...")
        db.reset_failed_attempts("testuser")
        assert db.get_failed_count("testuser") == 0

        print("Lockout/Unlock")
        assert db.is_locked_out("testuser") is False
        # lock out
        db.lock_account("testuser")
        assert db.is_locked_out("testuser") is True
        # unlock
        db.unlock_account("testuser")
        assert db.is_locked_out("testuser") is False

        print("Check is_only_admin / delete_user...")
        # There's two admins. Delete one of them.
        assert db.is_only_admin() is False
        assert db.user_exists("testadmin") is True
        db.delete_user("testadmin")
        assert db.user_exists("testadmin") is False
        assert db.is_only_admin() is True
