#!C:\Users\User\AppData\Local\Microsoft\WindowsApps\python.exe
"""

This is to be used from the terminal / command-line with arguments

PHP should call this script and use the returned values to do things.

True means the script action completed

False means an error occurred along the way

"""

import argparse
import main
import sys
sys.path.append("c:/users/user/documents/github/authentication-system-leak-detection/venv/lib/site-packages")

def read_cmdline():
    parser = argparse.ArgumentParser(description="The authentication system",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--add-account", action="store_true", help="Add an account")
    parser.add_argument("--add-admin-account", action="store_true", help="Add an admin account")
    parser.add_argument("-d", "--delete-account", action="store_true", help="Delete an account")
    parser.add_argument("-f", "--unlock-account", action="store_true", help="Unlock an account")
    parser.add_argument("-t", "--target-user", help="The username of the account you want to have the action done to")
    parser.add_argument("-np", "--new-user-password", help="The new password of the account you want to have the action done to")
    parser.add_argument("auth_username", help="The username of the account requesting authentication")
    parser.add_argument("auth_password", help="The password of the account requesting authentication")
    args = parser.parse_args()
    config = vars(args)
    #print(config)

    # Redefine the configs to vars
    a_username = config.get("auth_username")
    a_password = config.get("auth_password")
    target_u = config.get("target_user")
    new_password = config.get("new_user_password")
    is_adding_account = config.get("add_account")
    is_adding_admin_account = config.get("add_admin_account")
    is_deleting_account = config.get("delete_account")
    is_unlocking_account = config.get("unlock_account")

    # It's not doing a special action, so just treat it as a regular login.
    if is_adding_account is False and is_adding_admin_account is False and is_deleting_account is False and is_unlocking_account is False:
        return main.is_authenticated(a_username, a_password)

    # Adding a normal account
    if is_adding_account is True and is_adding_admin_account is False and is_deleting_account is False and is_unlocking_account is False:
        # Check that we have the required inputs
        if target_u is None:
            #print("Missing --target-user argument")
            return False
        if new_password is None:
            #print("Missing --new-user-password")
            return False

        # Run the script
        return main.add_user_account(a_username, a_password, target_u, new_password, add_as_admin=False)

    # Adding an admin account
    if is_adding_account is False and is_adding_admin_account is True and is_deleting_account is False and is_unlocking_account is False:
        # Check that we have the required inputs
        if target_u is None:
            #print("Missing --target-user argument")
            return False
        if new_password is None:
            #print("Missing --new-user-password")
            return False

        # Run the script
        return main.add_user_account(a_username, a_password, target_u, new_password, add_as_admin=True)

    # Deleting an account
    elif is_adding_account is False and is_adding_admin_account is False and is_deleting_account is False and is_unlocking_account is False:
        # Check that we have the required inputs
        if target_u is None:
            #print("Missing --target-user argument")
            return False

        # Run the script
        return main.delete_user(a_username, a_password, target_u)

    # Unlocking an account
    elif is_adding_account is False and is_adding_admin_account is False and is_deleting_account is False and is_unlocking_account is False:
        # Check that we have the required inputs
        if target_u is None:
            #print("Missing --target-user argument")
            return False

        # Run the script
        return main.unlock_account(a_username, a_password, target_u)
    else:
        #print("Something is badly formatted.")
        return False


read_cmdline()