"""
This is to be used from the terminal / command-line with arguments

PHP should call to this before:
- Trying to create a user account
- Trying to change a password

"""
import argparse
import password_checker
import username_checker
from database_controller import user_exists


def read_cmdline():
    parser = argparse.ArgumentParser(description="A small script to check if the input matches the policies",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--username", help="Username to be analyzed")
    parser.add_argument("-p", "--password", help="Password to be analyzed")
    args = parser.parse_args()
    config = vars(args)
    print(config)

    # Redefine the configs to vars
    username = config.get("username")
    password = config.get("password")

    if username is None and password is None:
        print("Error: No arguments were given.")
        return False

    if username is not None and password is not None:
        print("Error: Choose only one argument.")
        return False

    if username is not None:
        if user_exists(username) is False and username_checker.is_valid_username(username) is True:
            return True
        else:
            return False

    if password is not None:
        return password_checker.password_valid_to_policy_rules(password)


if __name__ == '__main__':
    print(read_cmdline())

