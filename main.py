"""
This code will eventually call all the other scripts for their various functions
- Add user to database
---> Check if username requirements
        On PASS:
            --> generate the passwords
            --> calc where to place the real password
            --> place in database


- Delete user from database
---> Check the user is admin
---> Then check the username exists then delete
            If it doesn't exist return the message that the username doesn't exist

- Log a user in
--> Login requires to check the username exists
----> If the username doesn't exist return that the credentials are incorrect.
            Don't tell them the username doesn't exist
----> Check if the account is locked
    ----> If it is not locked, calculate where the correct password is located.
        --> After the calc check if the username and password are correct
                If correct log them in
                Else check if the password is a decoy
                If not a decoy, increase the incorrect counter
                    When incorrect counter  == 10 lock the account



It will also be used to connect to the database


"""
import random

import database_controller as db_controller
from colorama import init as colorama_init
from colorama import Fore, Back, Style

from email_service import send_email
from password_checker import password_valid_to_policy_rules
from username_checker import is_valid_username

# Initialize for to use colorful print messages later
colorama_init()


RANDOM_NOISE = "1CPj3KSeCpaRlu6FvfG6"  # A string
RANDOM_NUMBER = 383369324388255133968499854491  # An int
NUMBER_OF_PASSWORDS = 11  # An int, N total passwords (1 real + N-1 decoy passwords)


# For this it shouldn't matter what (simple) algorithm we use for the proof of concept
# because any method of hiding it is constrained to the database having N passwords (1 real + N-1 decoy passwords)
# For this to be secure it require that no one gets the code behind the password hiding.
# This will take a string and return an int to be used as the array index
def hide_password(username: str) -> int:
    char_sum = 0
    username = username + RANDOM_NOISE
    for char in username:
        char_sum += ord(char)

    placement = (char_sum * RANDOM_NUMBER) % NUMBER_OF_PASSWORDS

    #print(f"hide_password({username}) placement: {placement}")

    return placement


# TODO: Decoy generator
def decoy_generator() -> list:
    return ['decoy1', "decoy2", 'decoy3', 'decoy4', 'decoy5', 'decoy6', 'decoy7', 'decoy8', 'decoy9', 'decoy10']


def _array_handler(real_password: str, array_decoys: list, real_placement: int) -> list:
    random.shuffle(array_decoys)  # Randomize the array
    array_decoys.insert(real_placement, real_password)
    #print(array_decoys)
    return array_decoys


hidden = _array_handler("the_real_password", decoy_generator(), hide_password("mblack"))

#print(hidden)


def create_password_array(username: str, password: str) -> list:
    # Generate decoys
    return _array_handler(password, decoy_generator(), hide_password(username))


def get_real_password(username: str, password_array) -> str:
    return password_array[hide_password(username)]


#print(get_real_password("mblack", hidden))


def is_authenticated(username: str, input_password: str) -> bool:
    if db_controller.user_exists(username):
        # If the account isn't locked out get the passwords
        if db_controller.is_locked_out(username) is False:
            # Find the real password
            user_passwords = db_controller.get_passwords(username)
            real_password = get_real_password(username, user_passwords)

            # The real password was used
            if input_password == real_password:
                # The password is the real password
                print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} Correct pass and username")

                # Reset the fail counter to zero
                db_controller.reset_failed_attempts(username)

                # Authenticate user
                return True
            # A decoy was used
            elif input_password in user_passwords:
                # The password is a decoy
                print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} DECOY USED")

                # Send the breach alert email to the admin
                send_email("test", 2, username)
                return False
            # The password is wrong but not a decoy
            else:
                # The account will be locked at 10 wrong attempts, the equality is just to make sure.
                if db_controller.get_failed_count(username) >= 10:
                    print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} Too many wrong attempts. Your account has been locked.")
                    db_controller.lock_account(username)
                    # Send the account locked email to the admin
                    send_email("test", 1, username)
                    return False
                else:
                    # Increase fails counter
                    db_controller.increment_failed_attempts(username)
                    print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} Wrong password - Wrong Attempt Count: {db_controller.get_failed_count(username)}")
                    return False
        else:
            print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL} Your account was locked for your safety. Contact an admin to unlock it.")
            return False

    else:
        print(f"{Back.BLACK}{Fore.YELLOW}[Authentication Response]{Style.RESET_ALL}Error: Username {username} doesn't exist")
        return False


def add_user_account(admin_name: str, auth_password: str, username: str, new_user_password: str, add_as_admin=False):
    """
    When an admin requests it, they can create a new user with password of their choosing.

    :param admin_name: username of the admin account adding the new user
    :param auth_password: the password of the admin account adding the new user
    :param username: the name of the new user the admin wants to add to the system
    :param new_user_password: the password of the new user to be added to the system
    :param add_as_admin: boolean (Default: false) If true, the account added is made an admin to the system
    :return: None
    """

    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print(f"Admin is really admin")

        if db_controller.user_exists(username) is False:
            if is_valid_username(username) is True:
                print(f"Username is unique")
                if password_valid_to_policy_rules(new_user_password):
                    # Generate fake passwords
                    password_array = create_password_array(username, new_user_password)
                    db_controller.add_user(username, password_array, add_as_admin)
                    print(f"Account created")
                    return True  # Success
                else:
                    print(f"Password didn't meet standards.")
                    return False
        else:
            print(f"The user already exists in the system.")
            return False
    else:
        print(f"Admin requesting is a faker")
        return False


    # Check admin requirements of: isadmin and password is correct


def delete_user(admin_name: str, auth_password: str, username: str) -> bool:
    """
    Function will delete a requested user if the caller is an admin and the password is correct.
    :param admin_name: the username of the admin account requesting account deletion
    :param auth_password: the password of the admin account requesting account deletion
    :param username: the username of the account to be deleted
    :return: action_successful: A boolean telling if the action was completed or if where was an error
    """
    # Check if the requesting account is the admin and is authenticated
    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print(f"Admin is really admin")
        if db_controller.user_exists(username):
            # TODO: Create a safety to prevent the only admin from removing themselves
            # Delete the user if they exist
            db_controller.delete_user(username)
            print(f"Success: Deleted {username}")
            return True  # Success
        else:
            print(f"The user you have requested to delete doesn't exist.")
            return False
    else:
        print(f"Admin requesting is a faker")
        return False


def unlock_account(admin_name: str, auth_password: str, username: str) -> bool:
    """
    Function will unlock a requested user's account if the caller is an admin and the password is correct.
    :param admin_name: the username of the admin account requesting account deletion
    :param auth_password: the password of the admin account requesting account deletion
    :param username: the username of the account to be unlocked
    :return: action_successful: A boolean telling if the action was completed or if where was an error
    """
    # Check if the requesting account is the admin and is authenticated
    if db_controller.is_admin(admin_name) and is_authenticated(admin_name, auth_password):
        print(f"Admin is really admin")
        if db_controller.user_exists(username):
            # Unlock the account
            db_controller.unlock_account(username)
            print(f"Success: Unlocked {username}'s account")
            return True  # Success
        else:
            print(f"The user account you have requested to unlock doesn't exist.")
            return False
    else:
        print(f"Admin requesting is a faker")
        return False


def update_password(username: str, current_password: str, new_password: str) -> bool:
    """
    Any account can change their own password, provided they give the correct current password.
    :param username: the username of the account wanting the password change
    :param current_password: the current_password of the account wanting the password change
    :param new_password: the new_password of the account wanting the password change
    :return: bool which is true on success, false on fail
    """
    # Check if the requesting account is really the account owner
    if is_authenticated(username, current_password):
        print(f"User is really the user")
        if password_valid_to_policy_rules(new_password):
            if password_valid_to_policy_rules(new_password):
                # Generate fake passwords
                password_array = create_password_array(username, new_password)
                db_controller.update_password(username, password_array)
            print(f"Success: Updated the password to {username}'s account")
            return True  # Success
        else:
            print(f"The new password doesn't meet the policy standards.")
            return False
    else:
        print(f"User requesting is a faker")
        return False

#add_user_account("admin", "password", "testuser", "Q49^y1z!uxV!")
#is_authenticated("testuser", "sdfsdfsdsdf")
#unlock_account("admin", "password", "testuser")

print(update_password("admin", "gqL3031%$#qK", "password"))

db_controller.print_table()