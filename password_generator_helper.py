import re
from random import choice, randint
import string as alphabet_string
import password_checker


# Simple function to flip a letter's case
# If a number or symbol gets passed to this, it just returns it unchanged
def change_case(letter: str) -> str:
    if letter.isupper():
        return letter.lower()
    else:
        return letter.upper()


# Return a set of 4 numbers which could be a plausible date
# Call as random_date() for MM-DD
# Call as random_date(month_first=False) for DD-MM
def random_date(month_first=True) -> str:
    # Date Generator
    month_number = randint(1, 12)  # Pick from 0 or 1
    if month_number < 10:  # Add a leading zero
        month_number = str(0) + str(month_number)

    # print(month_number)

    # Months with 31 days
    if (
        month_number == "01"
        or month_number == "03"
        or month_number == "05"
        or month_number == "07"
        or month_number == "08"
        or month_number == "10"
        or month_number == "12"
    ):
        day_number = randint(1, 31)
    # Months with 30 days
    elif month_number == "04" or month_number == "06" or month_number == "09" or month_number == "11":
        day_number = randint(1, 30)
    else:  # Feb
        day_number = randint(1, 28)  # 28 days

    if day_number < 10:  # Add a leading zero
        day_number = str(0) + str(day_number)

    # print(day_number)

    if month_first is True:
        return str(month_number) + str(day_number)
    else:
        return str(day_number) + str(month_number)


def random_4_numbers() -> str:
    num1 = randint(0, 9)
    num2 = randint(0, 9)
    num3 = randint(0, 9)
    num4 = randint(0, 9)
    return str(num1) + str(num2) + str(num3) + str(num4)


def leet_letters(letter: str) -> str:
    letter = letter.upper()  # Convert to upper case for sanity
    if letter == "A":
        return str(4)  # Make sure to return as string
    elif letter == "B":
        return str(8)
    elif letter == "E":
        return str(3)
    elif letter == "I":
        return str(1)
    elif letter == "L":
        return str(1)
    elif letter == "O":
        return str(0)
    elif letter == "S":
        return str(5)
    else:  # Default back
        return str(letter)


# Converts 4, 8, 3, 0, 5 , $ to a letter
def anti_leet_letters(letter: str) -> str:
    letter = str(letter).upper()  # Convert to upper case for sanity
    if letter == "4":
        return "A"
    elif letter == "8":
        return "B"
    elif letter == "3":
        return "E"
    elif letter == "0":
        return "O"
    elif letter == "5":
        return "S"
    elif letter == "$":
        return "S"
    else:  # Default back
        return str(letter)


# From what I've seen most people tend to add the digit and symbol near the end
def most_simple_password(string: str, simple_password_type: int = 1) -> str:
    """
    :param string: the password string you want to convert into a most simple password
    :param simple_password_type: the type of simple password you want
        1 - returns a stripped password with #1 at the end
        2 - returns a stripped password with ! at the end
    :return: the new simple password string
    """
    # Remove all symbols
    new_string = re.sub(r"[!@#$%^&*]", "", string)

    if simple_password_type == 1:
        # Add the symbol to the end
        return new_string + "#1"
    elif simple_password_type == 2:
        # Add the symbol to the end
        return new_string + "!"


def create_random_letter() -> str:
    return choice(alphabet_string.ascii_letters)


def create_random_digit() -> str:
    return choice(alphabet_string.digits)


def create_random_symbol() -> str:
    return choice(password_checker.ALLOWED_SPECIAL_CHAR)


def random_corruption(string: str, amount: int) -> str:
    # Always corrupt the first character in the string
    random_corruption_type = randint(1, 3)
    if random_corruption_type == 1:
        replacement = create_random_letter()
    elif random_corruption_type == 2:
        replacement = create_random_digit()
    else:
        replacement = create_random_symbol()
    # Replace
    string = string[:0] + replacement + string[0+1:]

    # Now replace random characters X amount of times
    for i in range(0, amount):
        # Pick a random place and corrupt it
        already_used = [0]
        random_place = randint(1, len(string)-1)

        # Prevent reusing an index
        while random_place in already_used:
            random_place = randint(1, len(string) - 1)

        random_corruption_type = randint(0, 3)

        if random_corruption_type == 1:
            replacement = create_random_letter()
        elif random_corruption_type == 2:
            replacement = create_random_digit()
        else:
            replacement = create_random_symbol()

        # Replace
        string = string[:random_place] + replacement + string[random_place+1:]
        already_used.append(random_place)

    return string


# TODO: Redo this and break it after considering various test cases
def convert_4_digits(string: str):
    set_of_4_digits = re.findall(r"\d{4}", string)  # If there's 4 digits near each other, group them into the array

    if len(set_of_4_digits) > 0:
        target_set_of_digits = choice(set_of_4_digits)  # Select from the array
        corruption_type = randint(1, 5)
        # print(target_set_of_digits)

        # The 1 makes it replace only once in strings that have repeating numbers EX. 1234!1234
        # Occasionally, choose the last instance of the string
        if corruption_type == 1:  # Replace it with MM-DD numbers
            if randint(0, 1) == 0:
                string = string.replace(target_set_of_digits, random_date(), 1)
            else:  # Replace last occurrence
                string = random_date().join(string.rsplit(target_set_of_digits, 1))
        elif corruption_type == 2:  # Replace it with DD-MM numbers
            if randint(0, 1) == 0:
                string = string.replace(target_set_of_digits, random_date(month_first=False), 1)
            else:  # Replace last occurrence
                string = random_date(month_first=False).join(string.rsplit(target_set_of_digits, 1))
        else:  # Replace it with random numbers to stop it from being to predictably a date
            if randint(0, 1) == 0:
                string = string.replace(target_set_of_digits, random_4_numbers(), 1)
            else:  # Replace last occurrence
                string = random_4_numbers().join(string.rsplit(target_set_of_digits, 1))

    print(string)
