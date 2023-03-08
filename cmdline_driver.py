#!/usr/bin/env python3
"""

Test driver to check some stuff using the command line

call venv/Scripts/activate.bat
python cmdline_driver.py
deactivate

python -m smtpd -c DebuggingServer -n localhost:1025

"""


import os  # Used to get the .env file
import sys

import mysql.connector
from colorama import Back, Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv  # Used to load info from the .env file

import python_scripts.database_controller as db_controller
from python_scripts.main import (
    add_user_account,
    delete_user,
    is_authenticated,
    unlock_account,
    update_password,
)

# Initialize for to use colorful print messages later
colorama_init()

# Pull data from .env and set up the database connection
load_dotenv()  # Load the secrets from the .env file
database_password = os.environ.get("DB_PASSWORD")
db_config = {"user": "root", "password": database_password, "host": "127.0.0.1", "database": "passwordKeepers"}

print(f"{Fore.CYAN}|--------------------------------------------------------------------------|{Style.RESET_ALL}")
print(
    f"{Fore.CYAN}|------------- {Fore.RED}Authentication System Leak Detection Prototype"
    f"{Fore.CYAN} -------------|{Style.RESET_ALL}"
)
print(
    f"{Fore.CYAN}|------------------------- {Fore.RED}By: Team Password F.M.{Fore.CYAN} "
    f"-------------------------|{Style.RESET_ALL}"
)
print(
    f"{Fore.CYAN}|---- {Fore.GREEN}{Style.BRIGHT}https://github.com/Yorzaren/authentication-system-leak-detection"
    f"{Style.RESET_ALL}{Fore.CYAN} ----|{Style.RESET_ALL}"
)
print(f"{Fore.CYAN}|--------------------------------------------------------------------------|{Style.RESET_ALL}")

try:
    print(f"{Fore.YELLOW}{Style.BRIGHT}Testing Database Connection...{Style.RESET_ALL}")
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print(f"{Fore.GREEN}SUCCESS: Connected to MySQL Server version {db_Info}{Style.RESET_ALL}")

except mysql.connector.Error as err:
    print(
        f"{Fore.RED}FAILED: Make you have the .env setup and the database running.{Style.RESET_ALL}\n" f"Error: {err}"
    )
    if err.errno == 2003:
        print("--> Check that the mysql service is running.")
    if err.errno == 1045:
        print("--> The password is wrong check the .env file.")
    if err.errno == 1049:
        print("--> Make sure you have created the mysql database using initialize_database.sql")
    sys.exit("Program closing. No database connection.")


def reset_db():
    # Create the connector
    cnx = mysql.connector.connect(**db_config)
    my_cursor = cnx.cursor(buffered=True)
    command = "CALL ResetDatabase()"
    my_cursor.execute(command)

    # Commit the changes
    cnx.commit()

    # Close the connector
    cnx.close()


def add_predefined_users():
    add_user_account("admin", "password", "testuser", "this!is!n0t!Good")
    add_user_account("admin", "password", "admin2", "s49^yxz!*xV!", add_as_admin=True)
    add_user_account("admin", "password", "jsmith", "9Jl%62EQMK4%")
    add_user_account("admin", "password", "mwilliams", "GreatLakes!1")
    add_user_account("admin", "password", "cReynolds23", "Bubble*t3a!!")
    add_user_account("admin", "password", "xzhang", "tngL9yWYZAaqV25E7&^$*kbKREq", add_as_admin=True)


def menu():
    loop_condition = True
    has_added_predefined_users = False

    while loop_condition:
        print(f"\n{Fore.LIGHTMAGENTA_EX}" f"|~~~~~~~~~~~~~~ MENU ~~~~~~~~~~~~~~|")
        print("\nPlease enter a number for what you want to do.\n")
        print("Enter 1 To Login.")
        print(f"Enter 2 {Fore.RED}[DEV]{Fore.LIGHTMAGENTA_EX} - Dump TABLE.")
        if has_added_predefined_users is False:  # Hide if already used.
            print(
                f"Enter 3 {Fore.RED}[DEV]{Fore.LIGHTMAGENTA_EX} - Add Predefined Test Users.* \n"
                f"    * (Only works if you have not changed the default admin account / password)"
            )
        print(f"Enter 4 {Fore.RED}[DEV]{Fore.LIGHTMAGENTA_EX} - Reset Database to Default.")
        print("Enter 0 to quit.\n")
        print(f"|~~~~~~~~~~~~ END MENU ~~~~~~~~~~~~|\n{Style.RESET_ALL}")

        main_input = input("What would you like to do? ")

        while main_input == "" or main_input.isdigit() is False:
            main_input = input("What would you like to do? ")
        main_input = int(main_input)  # Now that it's a digit it can be converted.

        if main_input == 0:
            print("Good Bye.")
            break
        else:
            if main_input == 1:
                username = input("Username: ")
                password = input("Password: ")

                if is_authenticated(username, password):
                    print(f"You have logged in as {Back.WHITE}{Fore.BLACK}{username}{Style.RESET_ALL}")
                    logged_in = True

                    while logged_in:  # Start USER MENU LOOP
                        # Show the admin menu
                        if db_controller.is_admin(username):
                            print("|---------------- USER MENU ----------------|")
                            print("    1 - Change password")
                            print("    2 - Add Normal User Account")
                            print("    3 - Add Admin Account")
                            print("    4 - Delete a User Account")
                            print("    5 - Unlock a User Account")
                            print("    0 - Return to Previous")
                            print("|-------------- END USER MENU --------------|")

                            # Loop until the user gives a valid choice
                            user_choice = input("Choice: ")

                            while user_choice == "" or user_choice.isdigit() is False:
                                user_choice = input("Choice: ")

                            user_choice = int(user_choice)

                            if user_choice == 0:
                                logged_in = False
                            elif user_choice == 1:
                                new_password = input("New Password: ")
                                print("Attempting to change your password...")
                                update_password(username, password, new_password)
                            elif user_choice == 2:
                                print("You are adding a normal user...")
                                username_to_be_added = input("New username to add: ")
                                new_user_password = input("Create Password for new user: ")
                                add_user_account(username, password, username_to_be_added, new_user_password)
                                print()
                            elif user_choice == 3:
                                print("You are adding an admin user...")
                                username_to_be_added = input("New username to add: ")
                                new_user_password = input("Create Password for new user: ")
                                add_user_account(username, password, username_to_be_added, new_user_password, True)
                            elif user_choice == 4:
                                print("You are deleting a user account...")
                                delete_user_named = input("Username of the account to delete: ")
                                delete_user(username, password, delete_user_named)
                            elif user_choice == 5:
                                print("You are unlocking a user account...")
                                unlock_user_named = input("Username of the account to unlock: ")
                                unlock_account(username, password, unlock_user_named)
                            else:
                                print("No selection")
                        # Normal User menu
                        else:
                            print("|---------------- USER MENU ----------------|")
                            print("    1 - Change password")
                            print("    0 - Return to Previous\n")
                            print("|-------------- END USER MENU --------------|")

                            # Loop until the user gives a valid choice
                            user_choice = input("Choice: ")

                            while user_choice == "" or user_choice.isdigit() is False:
                                user_choice = input("Choice: ")

                            user_choice = int(user_choice)

                            if user_choice == 0:
                                logged_in = False
                            elif user_choice == 1:
                                new_password = input("New Password: ")
                                print("Attempting to change your password...")
                                update_password(username, password, new_password)
                            else:
                                print("No selection")
                    # END - USER MENU LOOP
                # This else is related to is_authenticated
                else:
                    print("You couldn't be verified.")

            elif main_input == 2:
                db_controller.print_table()
            elif main_input == 3 and has_added_predefined_users is False:
                if is_authenticated("admin", "password"):
                    has_added_predefined_users = True
                    add_predefined_users()
                    print("Added the predefined users for testing.")
                else:
                    print(
                        f"{Fore.RED}[Error]: {Style.RESET_ALL}"
                        f"Database is not in the default state, so the users can't be added automatically.\n"
                        "You can reset the database for testing by using initialize_database.sql "
                        "to replace the current database."
                    )
            elif main_input == 4:
                reset_db()
                has_added_predefined_users = False


menu()
