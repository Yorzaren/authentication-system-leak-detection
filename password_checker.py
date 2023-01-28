import string as alphabet_string

# CONFIG VARS
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 32
MIN_UPPERCASE_LETTERS = 1
MIN_LOWERCASE_LETTERS = 1
MIN_AMOUNT_NUMBERS = 1
MIN_AMOUNT_SPECIAL_CHAR = 1
# Bitwarden generator and https://www.ibm.com/support/pages/password-policy-and-passwords-special-characters
ALLOWED_SPECIAL_CHAR = "!@#$%^&*"  # Remember to manually update the pytest to match the new count


# TODO: Finish finding which special character will be allowed by the policy


# --------------------------------------
# ---------- Helper functions ----------
# --------------------------------------
# Return the count of uppercase letters in a string
def count_uppercase(string):
    return sum(1 for c in string if c.isupper())


# Return the count of lower letters in a string
def count_lowercase(string):
    return sum(1 for c in string if c.islower())


# Return the count of digits in a string
def count_digits(string):
    return sum(1 for c in string if c.isdigit())


# Return the count of special characters which match ALLOWED_SPECIAL_CHAR in a string
def count_special_char(string):
    count = 0
    for char in string:
        if char in ALLOWED_SPECIAL_CHAR:
            count += 1
    return count


def has_forbidden_characters(string):
    arr = list(string)
    for char in range(len(arr)):
        test_char = string[char]
        # Don't use isalpha() because it will accept chars that aren't A-Z
        if not (
            test_char in alphabet_string.ascii_lowercase
            or test_char in alphabet_string.ascii_uppercase
            or test_char.isdigit()
            or test_char in ALLOWED_SPECIAL_CHAR
        ):
            # print(test_char)
            return True
    # If it makes it here it's shouldn't have forbidden characters
    return False


"""
Check that the password conforms to the policy defined in the CONFIG VARS

Parameters:
-------------
password : string
    the password to check

Returns:
-------------
boolean
    true : valid password format
    false : invalid password format
"""


def password_valid_to_policy_rules(password):
    # It a bit weirdly written, but we only need to return FALSE on a fail so there's no need for an else
    # Basically, read each statement after the "not" as the requirement to understand what is being compared
    # And remember we only fail on it not meeting req so the "not" is there to flip it, and we return false

    # Check the length is between the min and max allowed by the password policy
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        print("Invalid length")
        return False
    # Check if there's enough uppercase letters to match the password policy
    if not count_uppercase(password) >= MIN_UPPERCASE_LETTERS:
        print("Not enough uppercase letter(s)")
        return False
    # Check if there's enough lowercase letters to match the password policy
    if not count_lowercase(password) >= MIN_LOWERCASE_LETTERS:
        print("Not enough lowercase letter(s)")
        return False
    # Check if there's enough digits to match the password policy
    if not count_digits(password) >= MIN_AMOUNT_NUMBERS:
        print("Not enough digit(s)")
        return False
    # Check if there's enough special characters to match the password policy
    if not count_digits(password) >= MIN_AMOUNT_SPECIAL_CHAR:
        print("Not enough special character(s)")
        return False
    # Check for bad characters which break policy
    if has_forbidden_characters(password) is True:
        print("Includes forbidden character(s)")
        return False
    # If it makes it here it has passed the checks
    return True




"""
test = [
    "123#%Txrte2323yrtyhrtyhrtyrtyrty3",  # 33 chars
    "sdfkjsdkf398njdssdifu83!@#ds",  # No cap
    "32SDJF9JDH29N0",  # no lower
    "1234567"  # too short
    "你好213AD!sxd"
]

for i in range(len(test)):
    password_valid_to_policy_rules(test[i])
"""