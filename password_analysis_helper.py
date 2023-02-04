import password_checker
import re
from password_generator_helper import anti_leet_letters
import nltk  # Used to detect if something is a dictionary word
from nltk.corpus import words
from nostril import nonsense

# Import the real words for later
nltk.download('words')
set_of_words = set(words.words())

# The starts_with and ends_with functions return booleans


def starts_with_uppercase_letter(string: str) -> bool:
    return string[0].isupper()


def starts_with_lowercase_letter(string: str) -> bool:
    return string[0].islower()


def starts_with_digit(string: str) -> bool:
    return string[0].isdigit()


def starts_with_symbol(string: str) -> bool:
    return string[0] in password_checker.ALLOWED_SPECIAL_CHAR


def ends_with_uppercase_letter(string: str) -> bool:
    return string[-1].isupper()


def ends_with_lowercase_letter(string: str) -> bool:
    return string[-1].islower()


def ends_with_digits(string: str) -> bool:
    return string[-1].isdigit()


def ends_with_symbols(string: str) -> bool:
    return string[-1] in password_checker.ALLOWED_SPECIAL_CHAR


def split_letter_strings(string: str):
    return re.findall(r'[a-zA-Z]+', string)  # Returns an array


def split_uppercase_strings(string: str):
    return re.findall(r'[A-Z]+', string)  # Returns an array


def split_uppercase_strings(string: str):

    return re.findall(r'[a-z]+', string)  # Returns an array


def split_digit_strings(string: str):
    return re.findall(r'\d+', string)  # Returns an array


def split_symbols_strings(string: str):
    return re.findall(r'[!@#$%^&*]+', string)  # Returns an array


def convert_from_leet(string: str) -> str:
    new_string = ""
    for char in string:
        new_string = new_string + anti_leet_letters(char)
    return new_string


# TODO: I haven't found a foolproof way to calc it, consider other methods.
# The goal of this function is to detect if the string is random letters, symbols, and numbers
# You already tried https://github.com/casics/nostril
# which will fail if the sample is too small or gives both false positives and negatives.
def is_random_string(string: str) -> bool:
    randomness_score = 0
    unleeted_string = convert_from_leet(string)
    string_array = split_letter_strings(string)
    unleeted_array = split_letter_strings(unleeted_string)
    size_string_array = len(string_array)
    size_unleeted_array = len(unleeted_array)

    max_len_string_array = max(string_array, key=len)
    max_len_unleeted_array = max(unleeted_array, key=len)

    print('Original String: ' + string)
    print('Unleet: ' + unleeted_string)
    print('Strings (' + str(size_string_array) + '): ' + str(string_array))
    print('Strings After Unleeting (' + str(size_unleeted_array) + '): ' + str(unleeted_array))
    print('Max Length String Array: ' + str(max_len_string_array))
    print('Max Length Unleeted Array: ' + str(max_len_unleeted_array))

    if size_string_array == size_unleeted_array:
        # If the array sizes don't change its probably random.
        print("-->Didn't Shrink")
        randomness_score += 2
    if len(max_len_unleeted_array) >= len(string)/2:
        # If the unleeted_string is half or more it's not really random... ?
        print("-->The string seems to be too long, so prob not random")
        randomness_score -= 2

    for x in string_array + unleeted_array:  # Check both arrays
        if len(x) >= 2:  # Skip words
            potential_word = x.lower()
            # print(potential_word)

            # Use nltk to check for the array for dictionary words
            if potential_word in set_of_words:  # Means it likely not random
                print("-->Real word?: " + potential_word)
                randomness_score -= 1
            else:
                randomness_score += 0.2
            # End nltk check
            # Use nostril check randomness - it does have false pos and false negs tho.
            try:
                print("Nostril: " + str(nonsense(x)) )
            except:
                pass

    print("Is LargeNostrilNonsense: " + str(nonsense(unleeted_string)))

    print("Random Score: " + str(randomness_score) )
    print("IsRandom: " + str(randomness_score >= 0) )
    print('\n-----------------\n')



    """for x in split_letter_strings(anti_leet_string):
        try:
            print((x))
            print(print('{}: {}'.format(s, 'nonsense' if nonsense(x) else 'real')))
        except ValueError:
            pass"""





pass_test = ["1Am4Gr8C0d3r",
             "D32$jr#Q^VpD",
             "sdfsdfsWEW34!",
             "D0g!is!great!p3t",
             "sundayPizz4Party!",
             "Iamtheendandthebeginning!1"]
with open("examples/example_random_passwords.txt") as file:
    for line in file:
        pass_test.append(line.strip())
for s in pass_test:
    is_random_string(s)

