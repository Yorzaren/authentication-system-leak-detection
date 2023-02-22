from random import randint

from nltk import edit_distance

import password_checker
from password_analysis_helper import is_random_string, split_uppercase_strings, split_lowercase_strings, \
    split_capital_strings, split_digit_strings, contains_very_common_string, has_x_digits_in_a_row
from password_generator_helper import (
    change_case,
    random_date,
    random_4_numbers,
    leet_letters,
    anti_leet_letters,
    convert_4_digits, random_corruption, random_leet, random_symbol_change, simple_changes, regular_handler,
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


def password_analysis_randomness(real_password, debugging=False) -> bool:
    """
    is_random_string() returns a boolean based off a score, but has both false
    positives and negatives. The new analysis score will take into account the
    composition of the password  in relation to the password policy.

    This will return a boolean for the variable: is_random
    """

    ANALYSIS_SCORE = 0  # Higher score means more likely to be random.
    is_random = False

    # Allows you to reduce the amount of messages you get when debugging
    DEBUG_GENERAL = True
    DEBUG_POLICY = True
    DEBUG_STRING = True

    # Password differences
    # --- STAT TRACKING VARS ---
    length_password = len(real_password)
    # Track the character counts
    upper_count = count_uppercase(real_password)
    lower_count = count_lowercase(real_password)
    digit_count = count_digits(real_password)
    special_char_count = count_special_char(real_password)

    # Track things about the string and the policy difference
    policy_diff_length = length_password - password_checker.MIN_PASSWORD_LENGTH
    policy_diff_upper = upper_count - password_checker.MIN_UPPERCASE_LETTERS
    policy_diff_lower = lower_count - password_checker.MIN_LOWERCASE_LETTERS
    policy_diff_digit = digit_count - password_checker.MIN_AMOUNT_DIGITS
    policy_diff_special = special_char_count - password_checker.MIN_AMOUNT_SPECIAL_CHAR

    # Track info about the string composition
    max_uppercase_string_length = len(max(split_uppercase_strings(real_password), key=len))
    max_lowercase_string_length = len(max(split_lowercase_strings(real_password), key=len))
    max_capital_string_length = len(max(split_capital_strings(real_password), key=len))
    max_digital_string_length = len(max(split_digit_strings(real_password), key=len))
    count_uppercase_strings = len(split_uppercase_strings(real_password))
    count_lowercase_strings = len(split_lowercase_strings(real_password))
    count_capital_strings = len(split_capital_strings(real_password))
    count_digital_strings = len(split_digit_strings(real_password))

    # Debugging information
    if debugging is True:
        print(f"{Back.BLACK}password: " + f"{Fore.GREEN}" + real_password + f"{Style.RESET_ALL}")

        if DEBUG_GENERAL is True:
            print(f"{Back.CYAN}{Fore.BLACK}General Analysis:{Style.RESET_ALL}")
            print(f"password_length: {length_password}")
            print(f"upper_count: {upper_count}")
            print(f"lower_count: {lower_count}")
            print(f"digit_count: {digit_count}")
            print(f"special_char_count: {special_char_count}")

        if DEBUG_POLICY is True:
            print("------------")

            print(f"{Back.CYAN}{Fore.BLACK}Policy Analysis:{Style.RESET_ALL}")
            print(f"policy diff length_password: {policy_diff_length}")
            print(f"policy diff upper_count: {policy_diff_upper}")
            print(f"policy diff lower_count: {policy_diff_lower}")
            print(f"policy diff digit_count: {policy_diff_digit}")
            print(f"policy diff special_char_count: {policy_diff_special}")

        if DEBUG_STRING is True:
            print("------------")

            print(f"{Back.CYAN}{Fore.BLACK}String Analysis:{Style.RESET_ALL}")
            print(f"array_uppercase_strings: {split_uppercase_strings(real_password)}")
            print(f"array_lowercase_strings: {split_lowercase_strings(real_password)}")
            print(f"array_capital_strings: {split_capital_strings(real_password)}")
            print(f"array_digital_strings: {split_digit_strings(real_password)}")
            print("--")
            print(f"count_uppercase_strings: {count_uppercase_strings}")
            print(f"count_lowercase_strings: {count_lowercase_strings}")
            print(f"count_capital_strings: {count_capital_strings}")
            print(f"count_digital_strings: {count_digital_strings}")
            print("--")
            print(f"max_uppercase_string_length: {max_uppercase_string_length}")
            print(f"max_lowercase_string_length: {max_lowercase_string_length}")
            print(f"max_capital_string_length: {max_capital_string_length}")
            print(f"max_digital_string_length: {max_digital_string_length}")

        # Change the color based off the answer
        if is_random_string(real_password):
            print(f"is_likely_random_string: {Fore.GREEN}{is_random_string(real_password)}{Style.RESET_ALL}")
        else:
            print(f"is_likely_random_string: {Fore.RED}{is_random_string(real_password)}{Style.RESET_ALL}")
        print(f"{Back.BLACK}PASSWORD: {Fore.GREEN}{real_password}{Style.RESET_ALL}")

        print("\n|****************************************************|\n")

    # The important part is actually eliminating passwords that aren't random from being listed as random.
    if is_random_string(real_password):  # If the initial check returns true
        # Interesting read which validates my assumptions
        # https://resources.infosecinstitute.com/topic/beyond-password-length-complexity/

        # Length Checks - People tend to make passwords close to the policy length
        if policy_diff_length >= 10:
            ANALYSIS_SCORE += 5
        elif policy_diff_length >= 5:
            ANALYSIS_SCORE += 2
        elif policy_diff_length > 2:
            ANALYSIS_SCORE += 0.5

        # Uppercase Check
        if policy_diff_upper >= 3:
            ANALYSIS_SCORE += 2

        # We can prob skip a lowercase because most people will do lowercase passwords over uppercase
        # Symbol Check
        if policy_diff_special >= 3:
            ANALYSIS_SCORE += 2

        length_ratio = int(length_password / 3) - 1

        # print(f"{length_ratio} {count_uppercase_strings} {Fore.BLACK}{count_uppercase_strings >= length_ratio}{Style.RESET_ALL}")

        if count_uppercase_strings >= 5 or count_uppercase_strings >= length_ratio:
            ANALYSIS_SCORE += 2
        if count_lowercase_strings >= 5 or count_lowercase_strings >= length_ratio:
            ANALYSIS_SCORE += 2
        if count_capital_strings >= 5 or count_capital_strings >= length_ratio:
            ANALYSIS_SCORE += 2
        if count_digital_strings >= 5 or count_digital_strings >= length_ratio:
            ANALYSIS_SCORE += 2

        if debugging is True:
            print(f"ANALYSIS_SCORE--After adding bonuses: {Fore.GREEN}{ANALYSIS_SCORE}{Style.RESET_ALL}")

        # If it barely meets the policy is probably not random.
        if policy_diff_upper == 0:
            ANALYSIS_SCORE -= 1
            # print("policy_diff_upper")
        if policy_diff_lower == 0:
            ANALYSIS_SCORE -= 1
            # print("policy_diff_lower")
        if policy_diff_digit == 0:
            ANALYSIS_SCORE -= 1
            # print("policy_diff_digit")
        if policy_diff_special == 0:
            ANALYSIS_SCORE -= 1
            # print("policy_diff_digit")

        if count_uppercase_strings == 1:
            ANALYSIS_SCORE -= 1
        if count_lowercase_strings == 1:
            ANALYSIS_SCORE -= 1
        if count_capital_strings == 1:
            ANALYSIS_SCORE -= 1
        if count_digital_strings == 1:
            ANALYSIS_SCORE -= 1

        if contains_very_common_string(real_password) is True:
            ANALYSIS_SCORE -= 5

    if debugging is True:
        print(real_password)
        print(
            f"{Fore.RED}{Back.BLACK}[FINAL]{Style.RESET_ALL} ANALYSIS_SCORE: {Fore.GREEN}{ANALYSIS_SCORE}{Style.RESET_ALL}")

    if ANALYSIS_SCORE > 0:
        is_random = True

    if debugging is True:
        print(f"IsRandom: {is_random}")

        print("\n|******************************************************************|\n")

    return is_random


def _is_distanced(real: str, decoy: str, dist: int = 1) -> bool:
    """
    If the distance isn't far enough it's likely for people to type a decoy if they mess up.
    :param real: real password
    :param decoy: decoy password
    :param dist: distance from the real password
    :return: boolean
    If True then it's at least a 2 character difference.
    If False, its probably too close, and you should regenerate the decoy
    """
    # Levenshtein distance if 1 then its likely someone might hit it when mistyping
    return edit_distance(real, decoy) > dist


def _is_new_and_valid(real: str, decoy: str, array: list) -> bool:
    # if you use this in a while. You should have a NOT in front of it.
    if (password_checker.password_valid_to_policy_rules(decoy) is False
            or decoy == real
            or decoy in array
            or not _is_distanced(real, decoy)):
        return False
    else:
        return True

def generate_decoy_passwords(real_password: str):  # Returns an array
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
    simple_symbol_corruption = False
    simple_letter_case = False  # THis!i5AnAlert0963 --> This!i5analert0963
    simple_leet_corruption = False
    simple_digit_corruption = False

    # Check that the real_password conforms to the policy
    # We will also check this somewhere else too, but this is to warn us of issues.
    if password_checker.password_valid_to_policy_rules(real_password) is False:
        print(f"{Fore.RED}{Back.BLACK}[ERROR] The real_password: {real_password} "
              f"doesn't follow policy.{Style.RESET_ALL}")
        raise ValueError  # Catch this with try-except block when you call the generate_decoy_passwords just incase.

    # If the string is random, it doesn't matter what we do to it.
    if password_analysis_randomness(real_password, debugging=False) is True:
        print(f"{Fore.CYAN}[INFO] The string {Back.BLACK}{real_password}{Back.RESET} "
              f"is assumed to be very random.{Style.RESET_ALL}")
        print(f"Real Password: {Back.BLACK}{real_password}{Style.RESET_ALL}")
        # Generate X amount of decoys - The string is assumed to be very random.
        # Therefore, we can just generate the max amount of decoys requested.
        for i in range(0, AMOUNT_OF_DECOYS):  # The number is 10 to generate 10 decoy passwords
            # Generate the potential decoy
            new_decoy = random_corruption(real_password, int(len(real_password) / 2))
            # Check that the decoy follows the policy, if it doesn't keep trying until we get one.
            while password_checker.password_valid_to_policy_rules(new_decoy) is False:
                new_decoy = random_corruption(real_password, int(len(real_password) / 2))
            # Shouldn't be needed, but just incase, regen if its already in the decoy password array.
            while new_decoy in decoy_passwords:
                new_decoy = random_corruption(real_password, int(len(real_password) / 2))
            # If it passed the tests, then add it to the array.
            decoy_passwords.append(new_decoy)

    # String is not really random, so we have to handle it carefully
    else:
        print(f"{Fore.CYAN}[INFO] The string {Back.BLACK}{real_password}{Back.RESET} is not random.{Style.RESET_ALL}")

        # Check if it has a series of 4 digits in a row, because it might be a date or year
        if has_x_digits_in_a_row(real_password, 4):
            print("-->Method: 4 digits in a row")
            """
            The goal here is to figure out how to break them into groups.
            Basically, if someone were to know which set of 4 digits are in 
            the password, they shouldn't be able to pick it out quickly.
            
            If we have real password + 2 or 3 decoys with the same digits
            pass_set_1 which is a different set of numbers
            pass_set_2 which is a different set of numbers from the prior two
            Ex. A^RealChallenge1203
            
            Real password has digits of 1203
            pass_set_1 is 0608
            pass_set_2 is 0723
            
            We can generate decoys derived from a common numerical base to hide it better:
                A^RealChallenge1203 --> A*Re@lChal3nge1203 | A^realch@llenge1203 | A^Re4lhallenge1203
                A^RealChallenge0608 --> @^RealCha1lenge0608 | A!RealChallenge0608 | etc.
                A^RealChallenge0723 --> etc.
            
            Note: You are forcing the convert_4_digits to give out numbers which can only be MM/DD valid 
            """
            pass_set_with_real = randint(2, 3)  # 2 or 3
            pass_set_1 = randint(3, 4)  # 3 or 4
            pass_set_2 = AMOUNT_OF_DECOYS - pass_set_with_real - pass_set_1

            decoy_base_1 = convert_4_digits(real_password)
            # Make sure it's not the same digits as the real password
            while decoy_base_1 == real_password is True:
                decoy_base_1 = convert_4_digits(real_password)

            decoy_base_2 = convert_4_digits(real_password)
            # No overlaps
            while decoy_base_2 == real_password or decoy_base_2 == decoy_base_1 is True:
                decoy_base_2 = convert_4_digits(real_password)

            for i in range(0, pass_set_with_real):  # Corrupt the real_password
                # print(f"{real_password} {i + 1}")

                new_decoy = simple_changes(real_password)
                while not _is_new_and_valid(real_password, new_decoy, decoy_passwords):
                    new_decoy = simple_changes(real_password)

                decoy_passwords.append(new_decoy)
                # print(f"Added: {new_decoy}")

            for i in range(0, pass_set_1):  # Corrupt decoy_base_1
                # print(f"{decoy_base_1} {i + 1}")

                new_decoy = simple_changes(decoy_base_1)
                while not _is_new_and_valid(real_password, new_decoy, decoy_passwords):
                    new_decoy = simple_changes(decoy_base_1)

                decoy_passwords.append(new_decoy)
                # print(f"Added: {new_decoy}")

            for i in range(0, pass_set_2):  # Corrupt decoy_base_2
                # print(f"{decoy_base_2} {i + 1}")

                new_decoy = simple_changes(decoy_base_2)
                while not _is_new_and_valid(real_password, new_decoy, decoy_passwords):
                    new_decoy = simple_changes(decoy_base_2)

                decoy_passwords.append(new_decoy)
                # print(f"Added: {new_decoy}")

        else:
            print("Handle Randomly by doing whatever")
            for i in range(0, AMOUNT_OF_DECOYS):
                new_decoy = regular_handler(real_password)
                #print(f"Generated: {new_decoy}")
                counter = 0
                while not _is_new_and_valid(real_password, new_decoy, decoy_passwords):
                    #print("Failed to be good")
                    new_decoy = regular_handler(real_password)
                    #print(f"New Generated: {new_decoy} - {edit_distance(real_password, new_decoy)}")
                    if counter == 1000:
                        print("FAILED")
                        break
                    counter += 1

                decoy_passwords.append(new_decoy)
                print(f"Added: {new_decoy} - L_Distance: {edit_distance(real_password, new_decoy)}")
    # Debugging
    print(*decoy_passwords, sep=' | ')

    # Return the array for the other functions to use
    return decoy_passwords


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

    other = ["HT5p5Py!hZQWxNg", "2oxPnfis$u#NLi"]
    problematic_vailds = [
        "G@rden2!!asdf",
        "Cupc@kes@19s",
        "sharon^smaKer123",
        "ABCD1234@me!",
        "Redditor#nomaidenx3",
        "mr*beastSUX1",
        "ratiop1us%plusL"
    ]
    issues = ["ABCD1234@me!"]
    issues_r = ["ZYx@6z&W%aDb",
                "D32$jr#Q^VpD",
                "9Sk5yRyY2^8D",
                "Cq6#pBkyddv2",
                "QydZx2qB&#Liz@",
                "5Brom2n*J$%Fsz"]
    pass_test = []
    with open("examples/example_valid_passwords.txt") as file:
        for line in file:
            pass_test.append(line.strip())

    for s in pass_test:
        # password_analysis(s, debugging=False)
        try:
            generate_decoy_passwords(s)
        except ValueError:
            print("You can't use this password because it doesn't conform to the policy")

    """try:
        generate_decoy_passwords("BAD PASSWORD")
    except ValueError:
        print("You can't use this password because it doesn't conform to the policy")
    """
