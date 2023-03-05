import os  # Used to get the .env file

import mysql.connector
import pytest
from dotenv import load_dotenv  # Used to load info from the .env file

from python_scripts import database_controller as db_controller
from python_scripts import main

load_dotenv()  # Load the secrets from the .env file


@pytest.mark.skipif(not os.environ.get("DB_PASSWORD"), reason="No database connection")
class TestMain:
    # Reset everything before the tests
    if os.environ.get("DB_PASSWORD"):
        print("\n-->Resetting the system back to the default state\n")
        database_password = os.environ.get("DB_PASSWORD")
        db_config = {"user": "root", "password": database_password, "host": "127.0.0.1", "database": "passwordKeepers"}
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        my_cursor.execute("CALL ResetDatabase()")
        # Commit the changes and close
        cnx.commit()
        cnx.close()
        # Create a user to be breached
        db_controller.add_user("attackedUser", main.development_decoy_generator("attackedUser", "realP@ssword!"))

    @pytest.mark.order(1)
    def test_basic_auth(self):
        print("\n------Messages------")
        assert main.is_authenticated("admin", "password") is True  # Correct Username + Password
        assert main.is_authenticated("nonUser", "somepassword") is False  # Username doesn't exist

    @pytest.mark.order(2)
    def test_prevent_only_admin_deletion(self):
        print("\n------Messages------")
        assert main.delete_user("admin", "password", "admin") is False  # Can't delete as only admin

    @pytest.mark.order(3)
    def test_add_accounts(self):
        print("\n------Messages------")
        # Test that they don't exist yet
        assert main.is_authenticated("testuser", "Q49^y1z!uxV!") is False
        assert main.is_authenticated("jsmith", "Sm1th&W3ss0n") is False
        assert main.is_authenticated("oldUser", "@4Ix45@USJq8") is False
        assert main.is_authenticated("oldUser2", "8Pc7!PX5e^CR") is False
        assert main.is_authenticated("admin2", "s49^yxz!*xV!") is False
        # Create them
        main.add_user_account("admin", "password", "testuser", "Q49^y1z!uxV!")
        main.add_user_account("admin", "password", "jsmith", "Sm1th&W3ss0n")
        main.add_user_account("admin", "password", "oldUser", "@4Ix45@USJq8", add_as_admin=True)
        main.add_user_account("admin", "password", "oldUser2", "8Pc7!PX5e^CR")
        main.add_user_account("admin", "password", "admin2", "s49^yxz!*xV!", add_as_admin=True)
        # Test they were made
        assert main.is_authenticated("testuser", "Q49^y1z!uxV!") is True
        assert main.is_authenticated("jsmith", "Sm1th&W3ss0n") is True
        assert main.is_authenticated("oldUser", "@4Ix45@USJq8") is True
        assert main.is_authenticated("oldUser2", "8Pc7!PX5e^CR") is True
        assert main.is_authenticated("admin2", "s49^yxz!*xV!") is True

    @pytest.mark.order(4)
    def test_fail_auth_when_deleting(self):
        print("\n------Messages------")
        # admin4 is not an admin / They don't exist at all but its fine for the system to be vague.
        assert main.delete_user("admin4", "nopassword", "oldUser2") is False
        # Check the requested users wasn't deleted on the failed request
        assert main.is_authenticated("oldUser2", "8Pc7!PX5e^CR") is True

        # Real admin but wrong password should also fail
        assert main.delete_user("admin", "badpassword", "oldUser2") is False
        # Check the requested users wasn't deleted on the failed request
        assert main.is_authenticated("oldUser2", "8Pc7!PX5e^CR") is True

        # Real user and right password but not an admin
        assert main.delete_user("testuser", "Q49^y1z!uxV!", "oldUser2") is False
        # Check the requested users wasn't deleted on the failed request
        assert main.is_authenticated("oldUser2", "8Pc7!PX5e^CR") is True

    @pytest.mark.order(5)
    def test_use_decoy(self):
        print("\n------Messages------")
        assert main.is_authenticated("oldUser2", "decoy5") is False  # This shouldn't send an email.
        assert main.is_authenticated("attackedUser", "decoy5") is False  # THis should trigger the breach.

    @pytest.mark.order(6)
    def test_auth_lockout(self):
        print("\n------Messages------")
        assert main.is_authenticated("admin2", "s49^yxz!*xV!") is True  # Reset the counter
        # Lock out
        assert main.is_authenticated("admin2", "asdasd") is False
        assert main.is_authenticated("admin2", "asdasd") is False
        assert main.is_authenticated("admin2", "asdasd") is False  # This should email.
        # Trigger the account being locked
        assert main.is_authenticated("admin2", "asdasd") is False  # Print msg the account has been locked out.
        # Check that the admin account can't do anything when locked
        assert main.add_user_account("admin2", "s49^yxz!*xV!", "sstestss", "8Pc79!Ph5e!CR") is False

    @pytest.mark.order(7)
    def test_fail_adding_users(self):
        print("\n------Messages------")
        assert main.add_user_account("admin", "password", "testuser", "dasd") is False  # Already exists
        assert main.add_user_account("admin5", "password", "newUser", "dasd") is False  # Bad admin
        assert main.add_user_account("admin", "password", "newUser", "dasd") is False  # New user's password isn't good.

    @pytest.mark.order(8)
    def test_delete_user_msg(self):
        print("\n------Messages------")
        # Delete out a user and succeed.
        assert main.is_authenticated("oldUser", "@4Ix45@USJq8") is True
        assert main.delete_user("oldUser", "@4Ix45@USJq8", "oldUser") is True
        assert main.is_authenticated("oldUser", "@4Ix45@USJq8") is False
        # Try to delete something that doesn't exist.
        assert main.delete_user("admin", "password", "oldUser") is False  # Doesn't exist

    @pytest.mark.order(9)
    def test_unlock_account(self):
        print("\n------Messages------")
        # admin2 should still be locked out.
        assert main.is_authenticated("admin2", "s49^yxz!*xV!") is False
        assert main.unlock_account("admin", "password", "admin2")
        assert main.is_authenticated("admin2", "s49^yxz!*xV!") is True

        # Test failing to unlock bc not admin or right password
        assert main.unlock_account("admin", "badpassword", "testuser") is False

        assert main.unlock_account("admin", "password", "noUserByThisName") is False

    @pytest.mark.order(10)
    def test_change_password(self):
        print("\n------Messages------")
        assert main.update_password("jsmith", "notpassword", "Wcd@8sdf*dfdop#") is False  # Not the right password
        # Password isn't valid to rules
        assert main.update_password("jsmith", "Sm1th&W3ss0n", "invalidtoPolicy") is False
        assert main.update_password("jsmith", "Sm1th&W3ss0n", "Wcd@8sdf*dfdop#") is True  # Updated it fine.
