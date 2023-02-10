import password_checker
from password_analysis_helper import is_random_string
from password_generator_helper import (
    change_case,
    random_date,
    random_4_numbers,
    leet_letters,
    anti_leet_letters,
    convert_4_digits,
)
from password_checker import count_uppercase, count_lowercase, count_digits, count_special_char


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
    upper_count = count_uppercase(real_password)
    lower_count = count_lowercase(real_password)
    digit_count = count_digits(real_password)
    special_char_count = count_special_char(real_password)
    print(
        "password: "
        + real_password
        + "\n"
        + "upper_count: "
        + str(upper_count)
        + "\n"
        + "lower_count: "
        + str(lower_count)
        + "\n"
        + "digit_count: "
        + str(digit_count)
        + "\n"
        + "special_char_count: "
        + str(special_char_count)
    )
    print("------------")
    print(
        "policy diff upper_count: "
        + str(upper_count - password_checker.MIN_UPPERCASE_LETTERS)
        + "\n"
        + "policy diff lower_count: "
        + str(lower_count - password_checker.MIN_LOWERCASE_LETTERS)
        + "\n"
        + "policy diff digit_count: "
        + str(digit_count - password_checker.MIN_AMOUNT_DIGITS)
        + "\n"
        + "policy diff special_char_count: "
        + str(special_char_count - password_checker.MIN_AMOUNT_SPECIAL_CHAR)
        + "\n"
        + "is_likely_random_string: " + str(is_random_string(real_password))
        + "\n-----------------\n"
    )





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
    pass_test = []
    with open("examples/example_valid_passwords.txt") as file:
        for line in file:
            pass_test.append(line.strip())
        for s in pass_test:
            password_analysis(s)