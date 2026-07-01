"""

This file connects to the database and allows for the other parts of the program to communicate with the database.

There is no authentication before the commands execute, so check if the user calling for it has the proper
credentials in scripts that call the functions created here.

"""

import os  # Used to get the .env file

import mysql.connector
from colorama import Back, Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv  # Used to load info from the .env file

# Initialize for to use colorful print messages later
colorama_init()

# Pull data from .env and set up the database connection
load_dotenv()  # Load the secrets from the .env file
database_password = os.environ.get("DB_PASSWORD")
database_user = os.environ.get("DB_USER")

if database_user is None:  # If it's not defined, default to root
    database_user = "root"

db_config = {
    "user": database_user,
    "password": database_password,
    "host": "127.0.0.1",
    "database": "passwordKeepers",
}

"""
Admins:
    - add_user
    - delete_user
    - unlock_user
    - unlock_account

Everything else is used by the system to verify or set states.
"""


def __db_connection_error(err) -> None:  # pragma: no cover
    """
    This is a private helper function just to shorten a repeated message if there's an issue with
    the database connection.
    :return: Prints a message to the terminal/console.
    """
    if err.errno == 1049:  # Can't find the database
        print("Make sure you have created the database by using the script.")
    elif err.errno == 1045:
        print(
            "You haven't passed the password for the database from the .env file OR the password is incorrect."
        )
    else:
        print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def user_exists(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL UserExists("{username}");'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        # Close the connector
        cnx.close()

        if count == 1:
            return True
        else:
            return False
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def is_admin(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL IsUserAdmin("{username}");'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        # Close the connector
        cnx.close()

        if count == 1:
            return True
        else:
            return False
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def is_locked_out(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL IsUserLockedOut("{username}");'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        # Close the connector
        cnx.close()

        if count == 1:
            return True
        else:
            return False
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def add_user(username: str, password_array, create_admin_account=False):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command_create_admin = (
            f'CALL AddAdminUser("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", '
            f'"{password_array[5]}", "{password_array[6]}", "{password_array[7]}", '
            f'"{password_array[8]}", "{password_array[9]}", "{password_array[10]}");'
        )
        command_create_normal = (
            f'CALL AddNormalUser("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", '
            f'"{password_array[5]}", "{password_array[6]}", "{password_array[7]}", '
            f'"{password_array[8]}", "{password_array[9]}", "{password_array[10]}");'
        )

        if create_admin_account is True:
            my_cursor.execute(command_create_admin)
        else:
            my_cursor.execute(command_create_normal)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def delete_user(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL DeleteUser("{username}");'

        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def get_passwords(username: str) -> list:  # Return a list/array
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)

        # Update the last queried date
        command = f'CALL UpdateLastQuery("{username}");'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        query = f'CALL GetPasswords("{username}");'
        my_cursor.execute(query)

        # Close the connector
        cnx.close()

        return list(my_cursor.fetchone())
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def update_password(username: str, password_array):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = (
            f'CALL UpdatePassword("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", "{password_array[5]}", '
            f'"{password_array[6]}", "{password_array[7]}", "{password_array[8]}", "{password_array[9]}", '
            f'"{password_array[10]}");'
        )
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def lock_account(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL LockUser("{username}");'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def unlock_account(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL UnlockUser("{username}");'
        my_cursor.execute(command)
        # You need to reset this or the account will re-lock next time
        command2 = f'CALL ResetFails("{username}");'
        my_cursor.execute(command2)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def get_failed_count(username: str) -> int:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL GetFailsCount("{username}");'
        my_cursor.execute(query)

        # Close the connector
        cnx.close()

        return int(my_cursor.fetchone()[0])
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def increment_failed_attempts(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL IncrementFails("{username}");'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def reset_failed_attempts(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL ResetFails("{username}");'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def is_only_admin() -> bool:
    """
    This function returns true if there's only one admin in the system.
    It does not identify which account is the admin.
    When you call this, you need to combine it with an is_admin.
    :return: bool
    """
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = "CALL GetAdminCount();"
        my_cursor.execute(query)

        # Close the connector
        cnx.close()

        if int(my_cursor.fetchone()[0]) == 1:
            return True
        else:
            return False
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def lock_system():
    """
    When this is called, it will set the database to lockout every user.
    There is no recovery from this unless you manually unlock the accounts.
    However, you should NOT attempt to recover the system.
    This function should be called when there's more than one account
    that has used a decoy password.
    :return: none
    """
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = "CALL LockAllUsers();"
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()

    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def log_used_decoy(username: str):
    """
    This will add a user a decoy password associated with their account was used
    :param username: username of the account suspected be breached
    :return: none
    """
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL AddDecoyUsedFromUser("{username}");'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()

    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def get_global_decoy_usage() -> int:
    """
    This pulls the number of entries from passwordBreached.
    :return: int
    """
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = "CALL GetGlobalDecoyUsedCount();"
        my_cursor.execute(query)

        # Close the connector
        cnx.close()

        return int(my_cursor.fetchone()[0])
    except mysql.connector.Error as err:  # pragma: no cover
        __db_connection_error(err)


def print_table():
    # Debugging DUMP THE TABLE
    print(f"{Fore.CYAN}{Back.BLACK}--- DUMPING TABLE ---{Style.RESET_ALL}")
    cnx = mysql.connector.connect(**db_config)
    my_cursor = cnx.cursor(buffered=True)
    my_cursor.execute("CALL GetTable();")
    records = my_cursor.fetchall()
    for row in records:
        print(row)
    my_cursor.close()
    cnx.close()
    print(f"{Fore.CYAN}{Back.BLACK}-------- END --------{Style.RESET_ALL}")
