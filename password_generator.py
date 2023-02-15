import password_checker
from password_analysis_helper import is_random_string, split_uppercase_strings, split_lowercase_strings, \
    split_capital_strings, split_digit_strings, contains_very_common_string
from password_generator_helper import (
    change_case,
    random_date,
    random_4_numbers,
    leet_letters,
    anti_leet_letters,
    convert_4_digits, random_corruption,
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


def password_analysis(real_password, debugging=False) -> bool:
    """
    is_random_string returns a boolean based off a score, but has both false
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

        length_ratio = int(length_password/3) - 1

        #print(f"{length_ratio} {count_uppercase_strings} {Fore.BLACK}{count_uppercase_strings >= length_ratio}{Style.RESET_ALL}")

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
        print(f"{Fore.RED}{Back.BLACK}[FINAL]{Style.RESET_ALL} ANALYSIS_SCORE: {Fore.GREEN}{ANALYSIS_SCORE}{Style.RESET_ALL}")

    if ANALYSIS_SCORE > 0:
        is_random = True

    if debugging is True:
        print(f"IsRandom: {is_random}")

        print("\n|******************************************************************|\n")

    return is_random


def generate_fakes(real_password, amount=10):  # Returns an array
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
        raise ValueError  # Catch this with try-except block when you call the generate_fakes just incase.

    # If the string is random, it doesn't matter what we do to it.
    if password_analysis(real_password, debugging=False) is True:
        print(f"Real Password: {Back.BLACK}{real_password}{Style.RESET_ALL}")
        # Generate X amount of decoys - The string is assumed to be very random.
        # Therefore, we can just generate the max amount of decoys requested.
        for i in range(0, amount):
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

    other = ["HT5p5Py!hZQWxNg" , "2oxPnfis$u#NLi"]
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
    with open("examples/example_random_passwords.txt") as file:
        for line in file:
            pass_test.append(line.strip())

    for s in pass_test:
        #password_analysis(s, debugging=False)
        generate_fakes(s)
    try:
        generate_fakes("BAD PASSWORD")
    except ValueError:
        print("You can't use this password because it doesn't conform to the policy")
