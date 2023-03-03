"""

This is the main code for the program. It imports other functions to accomplish the goal of
generating similar passwords to a user provided password (the real or correct password).
The similar passwords are decoy or fake passwords intended on tricking an attacker.
If the attacker uses the decoy password in their attempt to get into a user's account
the system will alert the admin.
The system will also lock out a user account if they fail to type their password correctly.

Before the first run of the code.
1) Set up the MySQL database using the initialize_database.sql
2) Set up the .env file
3) Make sure the mailslurp credentials are up-to-date
    OR have smtpd running by using: python -m smtpd -c DebuggingServer -n localhost:1025

"""
import os
import random

from colorama import Back, Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv  # Used to load info from the .env file

import database_controller as db_controller
from email_service import send_email
from password_checker import password_valid_to_policy_rules
from password_generator import generate_decoy_passwords
from username_checker import is_valid_username

# Pull data from .env and set up the database connection
load_dotenv()  # Load the secrets from the .env file

# Initialize for to use colorful print messages later
colorama_init()

# DON'T CHANGE THESE ONCE YOU HAVE REAL ACCOUNTS IN THE DATABASE
# OR THE PROGRAM WILL NOT FIND THE CORRECT PASSWORD
RANDOM_NOISE = os.environ.get("RANDOM_NOISE")  # A string
RANDOM_NUMBER = os.environ.get("RANDOM_NUMBER")  # An int
NUMBER_OF_PASSWORDS = 11  # An int, N total passwords (1 real + N-1 decoy passwords)

# Fix things if it's undefined
if RANDOM_NOISE is None:
    RANDOM_NOISE = ""
if RANDOM_NUMBER is None:
    RANDOM_NUMBER = 1


# For this it shouldn't matter what (simple) algorithm we use for the proof of concept
# because any method of hiding it is constrained to the database having N passwords (1 real + N-1 decoy passwords)
# For this to be secure it require that no one gets the code behind the password hiding.
# This will take a string and return an int to be used as the array index
def __hide_password(username: str) -> int:
    char_sum = 0
    username = username + RANDOM_NOISE
    for char in username:
        char_sum += ord(char)

    placement = (char_sum * int(RANDOM_NUMBER)) % NUMBER_OF_PASSWORDS

    # print(f"__hide_password({username}) placement: {placement}")

    return placement


# Don't mark as private as you use it in test_main.py
def development_decoy_generator(username: str, password: str) -> list:
    """
    DO NOT USE THIS!!!! This is only for testing because it fills the array with junk and
    allows you to see the real password in the database.
    :return: list of filler
    """
    array_decoys = ["decoy1", "decoy2", "decoy3", "decoy4", "decoy5", "decoy6", "decoy7", "decoy8", "decoy9", "decoy10"]
    real_placement = __hide_password(username)
    random.shuffle(array_decoys)  # Randomize the array
    array_decoys.insert(real_placement, password)  # Place the real password in the array
    return array_decoys


def __create_password_array(username: str, password: str) -> list:
    """
    For debugging, you can swap out generate_decoy_passwords for development_decoy_generator
    This will allow you to see the real password when you dump the database table
    :param username: the name of the user
    :param password: the real password of the user
    :return: array list of decoys with the real password hidden in it
    """

    array_decoys = generate_decoy_passwords(password)  # Generate decoys
    real_placement = __hide_password(username)
    random.shuffle(array_decoys)  # Randomize the array
    array_decoys.insert(real_placement, password)  # Place the real password in the array
    return array_decoys


def __get_real_password(username: str, password_array) -> str:
    return password_array[__hide_password(username)]


def __print_system_auth_resp(msg: str) -> None:
    print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} {msg}")


def is_authenticated(username: str, input_password: str) -> bool:
    if db_controller.user_exists(username):
        # If the account isn't locked out get the passwords
        if db_controller.is_locked_out(username) is False:
            # Find the real password
            user_passwords = db_controller.get_passwords(username)
            real_password = __get_real_password(username, user_passwords)

            # The real password was used
            if input_password == real_password:
                # The password is the real password
                __print_system_auth_resp(f"Signed in as {Fore.CYAN}{username}{Fore.RESET}")

                # Reset the fail counter to zero
                db_controller.reset_failed_attempts(username)

                # Authenticate user
                return True
            # A decoy was used
            elif input_password in user_passwords:
                # The password is a decoy
                __print_system_auth_resp(f"DECOY USED for {Fore.CYAN}{username}{Fore.RESET}")

                # Send the breach alert email to the admin
                send_email("test", 2, username)
                return False
            # The password is wrong but not a decoy
            else:
                # Increase fails counter
                db_controller.increment_failed_attempts(username)

                # The account will be locked at 3 wrong attempts
                if db_controller.get_failed_count(username) >= 3:
                    print("Too many wrong attempts. Your account has been locked.")
                    db_controller.lock_account(username)
                    # Send the account locked email to the admin
                    send_email("test", 1, username)
                    return False
                else:
                    count = db_controller.get_failed_count(username)
                    __print_system_auth_resp("Wrong password - Wrong Attempt Count: " + str(count))
                    return False
        else:
            __print_system_auth_resp("Your account was locked for your safety. Contact an admin to unlock it.")
            return False
    # Username doesn't exist
    else:
        __print_system_auth_resp(f"Error: Username {Fore.CYAN}{username}{Fore.RESET} doesn't exist")
        return False


def add_user_account(admin_name: str, auth_password: str, username: str, new_user_password: str, add_as_admin=False):
    """
    When an admin requests it, they can create a new user with password of their choosing
    :param admin_name: username of the admin account adding the new user
    :param auth_password: the password of the admin account adding the new user
    :param username: the name of the new user the admin wants to add to the system
    :param new_user_password: the password of the new user to be added to the system
    :param add_as_admin: boolean (Default: false) If true, the account added is made an admin to the system
    :return: None
    """

    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print(f"The requesting account, {Fore.CYAN}{admin_name}{Fore.RESET}, IS an admin"
              f"\nAttempting to add account...")

        if db_controller.user_exists(username) is False:
            if is_valid_username(username) is True:
                print(f"Username: {Fore.CYAN}{username}{Fore.RESET} is unique")
                if password_valid_to_policy_rules(new_user_password):
                    # Generate fake passwords
                    password_array = __create_password_array(username, new_user_password)
                    db_controller.add_user(username, password_array, add_as_admin)
                    print(f"Success: Account named {username} had been created.")
                    return True  # Success
                else:
                    print(f"Error: Password {Fore.CYAN}{new_user_password}{Fore.RESET} didn't meet standards.")
                    return False
        else:
            print(f"Error: Username {Fore.CYAN}{username}{Fore.RESET} already exists in the system.")
            return False
    else:
        print(f"FAILURE: The requesting account, {admin_name} is NOT an admin OR Wrong Password.")
        return False

    # Check admin requirements of: isadmin and password is correct


def delete_user(admin_name: str, auth_password: str, username: str) -> bool:
    """
    Function will delete a requested user if the caller is an admin and the password is correct
    :param admin_name: the username of the admin account requesting account deletion
    :param auth_password: the password of the admin account requesting account deletion
    :param username: the username of the account to be deleted
    :return: action_successful: A boolean telling if the action was completed or if where was an error
    """
    # Check if the requesting account is the admin and is authenticated
    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print(f"The requesting account, {Fore.CYAN}{admin_name}{Fore.RESET}, IS an admin"
              f"\nAttempting to delete account...")
        if db_controller.user_exists(username):
            if db_controller.is_only_admin() is True:
                print(f"FAILURE: You can't delete {username} because they are the only admin.")
                return False
            # Delete the user if they exist
            db_controller.delete_user(username)
            print(f"Success: Deleted {username}")
            return True  # Success
        else:
            print("Error: The user you have requested to delete doesn't exist.")
            return False
    else:
        print(f"FAILURE: The requesting account, {admin_name} is NOT an admin OR Wrong Password.")
        return False


def unlock_account(admin_name: str, auth_password: str, username: str) -> bool:
    """
    Function will unlock a requested user's account if the caller is an admin and the password is correct
    :param admin_name: the username of the admin account requesting account deletion
    :param auth_password: the password of the admin account requesting account deletion
    :param username: the username of the account to be unlocked
    :return: action_successful: A boolean telling if the action was completed or if where was an error
    """
    # Check if the requesting account is the admin and is authenticated
    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print("Admin is really admin")
        if db_controller.user_exists(username):
            # Unlock the account
            db_controller.unlock_account(username)
            print(f"Success: Unlocked {username}'s account")
            return True  # Success
        else:
            print("The user account you have requested to unlock doesn't exist.")
            return False
    else:
        print(f"FAILURE: The requesting account, {admin_name} is NOT an admin OR Wrong Password.")
        return False


def update_password(username: str, current_password: str, new_password: str) -> bool:
    """
    Any account can change their own password, provided they give the correct current password
    :param username: the username of the account wanting the password change
    :param current_password: the current_password of the account wanting the password change
    :param new_password: the new_password of the account wanting the password change
    :return: bool which is true on success, false on fail
    """
    # Check if the requesting account is really the account owner
    if is_authenticated(username, current_password):
        print("User is really the user")
        if password_valid_to_policy_rules(new_password):
            if password_valid_to_policy_rules(new_password):
                # Generate fake passwords
                password_array = __create_password_array(username, new_password)
                db_controller.update_password(username, password_array)
            print(f"Success: Updated the password to {username}'s account")
            return True  # Success
        else:
            print("The new password doesn't meet the policy standards.")
            return False
    else:
        print(f"FAILURE: Wrong Username and/or Wrong Password.")
        return False
