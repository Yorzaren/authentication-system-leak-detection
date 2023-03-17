"""

As requested by the client, a rework of the algorithm.
Such that a password for example:
    egg$ar3t00Expensive
    should be replaced by any letter that matches the case
    e -> [a-z]
    $ -> [symbol]
    3 -> [0-9]
    E -> [A-Z]

"""
import string as alphabet_string
from random import choice

from colorama import Back, Fore, Style
from nltk import edit_distance

from python_scripts import password_checker
from python_scripts.password_checker import ALLOWED_SPECIAL_CHAR
from python_scripts.password_generator import __is_new_and_valid
from python_scripts.password_generator_helper import (
    create_random_digit,
    create_random_symbol,
)


def make_password(string: str) -> str:
    # Iterate over the string
    generated_password = ""
    for element in range(0, len(string)):
        this_char = string[element]
        if this_char.isdigit():
            generated_password += create_random_digit()
        if this_char in ALLOWED_SPECIAL_CHAR:
            generated_password += create_random_symbol()
        if this_char.islower():
            generated_password += choice(alphabet_string.ascii_lowercase)
        if this_char.isupper():
            generated_password += choice(alphabet_string.ascii_uppercase)
    return generated_password


def generate_decoy_passwords_redux(real_password: str) -> list:
    """
    :param real_password: string
    :return: array
    """

    AMOUNT_OF_DECOYS = 10

    """
    AMOUNT_OF_DECOYS is here if we choose to change the number later
    However, its probably not likely because more testing would be needed 
    to make sure nothing breaks.
    """

    decoy_passwords = []

    # Check that the real_password conforms to the policy
    # We will also check this somewhere else too, but this is to warn us of issues.
    if password_checker.password_valid_to_policy_rules(real_password) is False:
        print(
            f"{Fore.RED}{Back.BLACK}[ERROR] The real_password: {real_password} "
            f"doesn't follow policy.{Style.RESET_ALL}"
        )
        raise ValueError  # Catch this with try-except block when you call the generate_decoy_passwords just incase.

    print(f"{Fore.CYAN}[INFO] The real password is {Back.BLACK}{real_password}{Back.RESET}.{Style.RESET_ALL}")

    for i in range(0, AMOUNT_OF_DECOYS):
        new_decoy = make_password(real_password)
        print(f"Generated: {new_decoy}")
        counter = 0
        while not __is_new_and_valid(real_password, new_decoy, decoy_passwords):
            # print("Failed to be good")
            new_decoy = make_password(real_password)
            print(f"New Generated: {new_decoy} - {edit_distance(real_password, new_decoy)}")
            if counter == 1000:
                print("FAILED to generate decoy")
                break
            counter += 1

        decoy_passwords.append(new_decoy)
        print(f"Added: {new_decoy} - L_Distance: {edit_distance(real_password, new_decoy)}")

    # Debugging
    print(*decoy_passwords, sep=" | ")

    # Return the array for the other functions to use
    return decoy_passwords
