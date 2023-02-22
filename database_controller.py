"""

This file connects to the database and allows for the other parts of the program to communicate with the database.

There is no authentication before the commands are used, so check if the user calling for it has the proper
credentials in scripts that invoke the commands created in here.

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
db_config = {"user": "root", "password": database_password, "host": "127.0.0.1", "database": "passwordKeepers"}

"""

Theres are the intended users of the commands.
If it's marked as system is is meant for internal calls to verify things.
Admins:
    - add_user
    - delete_user
    - unlock_user

Who should be calling what:

user_exists : sys
is_admin : sys
is_locked_out : sys
add_user : admin
delete_user : admin
get_passwords : sys -> array_passwords & update_last_queried in the back end
update_password : must be the user (the admin can't change a user's password)
lock_account : sys | triggers on 10 bad password entries on the account
unlock_account : admin   --> also call reset_failed_attempts
get_failed_count : sys
increment_failed_attempts : sys
reset_failed_attempts : sys | reset on successful login | on unlock_account

"""


def user_exists(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL UserExists("{username}")'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        if count == 1:
            return True
        else:
            return False

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def is_admin(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL IsUserAdmin("{username}")'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        if count == 1:
            return True
        else:
            return False

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def is_locked_out(username: str) -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL IsUserLockedOut("{username}")'
        my_cursor.execute(query)
        count = my_cursor.fetchone()[0]

        if count == 1:
            return True
        else:
            return False

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def add_user(username: str, password_array, create_admin_account=False):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command_create_admin = (
            f'CALL AddAdminUser("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", '
            f'"{password_array[5]}", "{password_array[6]}", "{password_array[7]}", '
            f'"{password_array[8]}", "{password_array[9]}", "{password_array[10]}")'
        )
        command_create_normal = (
            f'CALL AddNormalUser("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", '
            f'"{password_array[5]}", "{password_array[6]}", "{password_array[7]}", '
            f'"{password_array[8]}", "{password_array[9]}", "{password_array[10]}")'
        )

        if create_admin_account is True:
            my_cursor.execute(command_create_admin)
        else:
            my_cursor.execute(command_create_normal)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def delete_user(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL DeleteUser("{username}")'

        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def get_passwords(username: str):  # Return an array
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)

        # Update the last queried date
        command = f'CALL UpdateLastQuery("{username}")'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        query = f'CALL GetPasswords("{username}")'
        my_cursor.execute(query)

        return list(my_cursor.fetchone())

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def update_password(username: str, password_array):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = (
            f'CALL UpdatePassword("{username}", "{password_array[0]}", "{password_array[1]}", '
            f'"{password_array[2]}", "{password_array[3]}", "{password_array[4]}", "{password_array[5]}", '
            f'"{password_array[6]}", "{password_array[7]}", "{password_array[8]}", "{password_array[9]}", '
            f'"{password_array[10]}")'
        )
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def lock_account(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL LockUser("{username}")'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def unlock_account(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL UnlockUser("{username}")'
        my_cursor.execute(command)
        # You need to reset this or the account will re-lock next time
        command2 = f'CALL ResetFails("{username}")'
        my_cursor.execute(command2)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def get_failed_count(username: str) -> int:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = f'CALL GetFailsCount("{username}")'
        my_cursor.execute(query)

        return int(my_cursor.fetchone()[0])

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def increment_failed_attempts(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL IncrementFails("{username}")'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def reset_failed_attempts(username: str):
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        command = f'CALL ResetFails("{username}")'
        my_cursor.execute(command)

        # Commit the changes
        cnx.commit()

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def is_only_admin() -> bool:
    try:
        # Create the connector
        cnx = mysql.connector.connect(**db_config)
        my_cursor = cnx.cursor(buffered=True)
        query = "CALL GetAdminCount()"
        my_cursor.execute(query)

        if int(my_cursor.fetchone()[0]) == 1:
            return True
        else:
            return False

        # Close the connector
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Can't find the database
            print("Make sure you have created the database by using the script.")
        elif err.errno == 1045:
            print("You haven't passed the password for the database from the .env file OR the password is incorrect.")
        else:
            print(f"{Fore.RED}{Back.BLACK}[ERROR]: {err}{Style.RESET_ALL}")


def print_table():
    # Debugging DUMP THE TABLE
    print(f"{Fore.CYAN}{Back.BLACK}--- DUMPING TABLE ---{Style.RESET_ALL}")
    cnx = mysql.connector.connect(**db_config)
    my_cursor = cnx.cursor(buffered=True)
    my_cursor.execute("CALL GetTable()")
    records = my_cursor.fetchall()
    for row in records:
        print(row)
    my_cursor.close()
    cnx.close()
    print(f"{Fore.CYAN}{Back.BLACK}-------- END --------{Style.RESET_ALL}")


if __name__ == "__main__":
    print(is_admin("Admin"))
    print(user_exists("Assdmin"))
    print_table()

    array = ["test1", "test2", "test3", "test4", "test5", "test6", "test7", "test8", "test9", "test10", "test11"]

    # add_user("testuser", array)
    # add_user("testadmin", array, True)
    update_password("Admin", array)

    print((get_passwords("Admin")[10]))
    increment_failed_attempts("Admin")
    print(get_failed_count("Admin") < 5)

    reset_failed_attempts("Admin")
    print(is_only_admin())
    print_table()
