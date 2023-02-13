import password_checker
from password_analysis_helper import is_random_string, split_uppercase_strings, split_lowercase_strings, \
    split_capital_strings
from password_generator_helper import (
    change_case,
    random_date,
    random_4_numbers,
    leet_letters,
    anti_leet_letters,
    convert_4_digits,
)
from password_checker import count_uppercase, count_lowercase, count_digits, count_special_char
from colorama import init as colorama_init
from colorama import Fore, Back, Style

# Initialize for to use colorful print messages later
colorama_init()

"""
Type of passwords:
- Passwords that wont be remembered 
    --> Handle with random letter, symbol, and number corruption.
- Passwords with social engineering weakness (dates/pet names/important life people) 
    --> Change letter case, leet it, change symbols, simplify, corrupt some numbers, 
    but leave multiple cases with the correct numbers but wrong symbols and cases
- Passwords of fandom/pop culture
    --> This might be a sub type of the previous and can probably be handled the same way.
- Passwords of immaturity (69, 420)
    --> Leave the numbers, leet it, change symbols, simplify 
- Passwords on keys patterns (probably wont be addressing this)
    --> Won't be handle in this iteration


"""


def password_analysis(real_password):
    length_password = len(real_password)
    # Track the character counts
    upper_count = count_uppercase(real_password)
    lower_count = count_lowercase(real_password)
    digit_count = count_digits(real_password)
    special_char_count = count_special_char(real_password)
    # Track info about the string composition
    max_uppercase_string_length = len(max(split_uppercase_strings(real_password)))
    max_lowercase_string_length = len(max(split_lowercase_strings(real_password)))
    max_capital_string_length = len(max(split_capital_strings(real_password)))
    count_uppercase_strings = len(split_uppercase_strings(real_password))
    count_lowercase_strings = len(split_lowercase_strings(real_password))
    count_capital_strings = len(split_capital_strings(real_password))

    print(f"{Back.BLACK}password: " + f"{Fore.GREEN}" + real_password + f"{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}General Analysis:{Style.RESET_ALL}")
    print("password_length: " + str(length_password))
    print("upper_count: " + str(upper_count))
    print("lower_count: " + str(lower_count))
    print("digit_count: " + str(digit_count))
    print("special_char_count: " + str(special_char_count))
    print("------------")
    print(f"{Back.CYAN}{Fore.BLACK}Policy Analysis:{Style.RESET_ALL}")
    print("policy diff length_password: " + str(length_password - password_checker.MIN_PASSWORD_LENGTH))
    print("policy diff upper_count: " + str(upper_count - password_checker.MIN_UPPERCASE_LETTERS))
    print("policy diff lower_count: " + str(lower_count - password_checker.MIN_LOWERCASE_LETTERS))
    print("policy diff digit_count: " + str(digit_count - password_checker.MIN_AMOUNT_DIGITS))
    print("policy diff special_char_count: " + str(special_char_count - password_checker.MIN_AMOUNT_SPECIAL_CHAR))

    print("is_likely_random_string: " + str(is_random_string(real_password)))
    print("------------")
    print(f"{Back.CYAN}{Fore.BLACK}String Analysis:{Style.RESET_ALL}")
    print("array_uppercase_strings: " + str(split_uppercase_strings(real_password)))
    print("array_lowercase_strings: " + str(split_lowercase_strings(real_password)))
    print("array_capital_strings: " + str(split_capital_strings(real_password)))
    print("count_uppercase_strings: " + str(count_uppercase_strings))
    print("count_lowercase_strings: " + str(count_lowercase_strings))
    print("count_capital_strings: " + str(count_capital_strings))
    print("max_uppercase_string_length: " + str(max_uppercase_string_length))
    print("max_lowercase_string_length: " + str(max_lowercase_string_length))
    print("max_capital_string_length: " + str(max_capital_string_length))
    print("\n|****************************************************|\n")


def generate_fakes(real_password="", amount=10):
    simple_symbol_corruption = False
    simple_letter_case = False  # THis!i5AnAlert0963 --> This!i5analert0963
    simple_leet_corruption = False
    simple_digit_corruption = False
    password_analysis(real_password)
    for i in range(0, amount):
        print("\n")
        # convert_4_digits(real_password)


if __name__ == '__main__':
    """
    pass_test = ["THis!i5AnAlert0963",
                 "1234!Cc1234",
                 "D32$jr#Q^VpD",
                 "45dsIfji34",
                 "sDfjkhuih3240",
                 "ifG3499mlerm@0346",
                 "Marrywe1299",
                 "123mar3rywe1299"]

    """
    other = ["HT5p5Py!hZQWxNg"]

    pass_test = []
    with open("examples/example_valid_passwords.txt") as file:
        for line in file:
            pass_test.append(line.strip())
        for s in pass_test:
            password_analysis(s)
