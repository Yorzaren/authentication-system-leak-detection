"""
This script should check that the username conforms to the username policy
"""

import string as alphabet_string

# CONFIG VARS
MIN_USERNAME_LENGTH = 5
MAX_USERNAME_LENGTH = 50


# This checks if the user meets the username string policy.
# The unique username requirement is checked in the same function which will call this one.
def is_valid_username(username: str) -> bool:
    # Check this to see if it has letters that aren't A-Z or a digit
    arr = list(username)
    for char in range(len(arr)):
        test_char = username[char]
        # Don't use isalpha() because it will accept chars that aren't A-Z
        if not (
            test_char in alphabet_string.ascii_lowercase
            or test_char in alphabet_string.ascii_uppercase
            or test_char.isdigit()
        ):
            # print(test_char)
            return False
    # Length check
    if not MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH:
        return False
    # If it makes it here is the correct length and does not contain forbidden characters
    return True
