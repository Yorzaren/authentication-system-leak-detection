import password_checker
import re
from password_generator_helper import anti_leet_letters
import nltk  # Used to detect if something is a dictionary word
from nltk.corpus import words
from nostril import nonsense
from collections import Counter

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


def split_lowercase_strings(string: str):
    return re.findall(r'[a-z]+', string)  # Returns an array


def split_capital_strings(string: str):
    return re.findall(r'[A-Z][^A-Z]*', string)  # Returns an array


def split_digit_strings(string: str):
    return re.findall(r'\d+', string)  # Returns an array


def split_symbols_strings(string: str):
    return re.findall(r'[!@#$%^&*]+', string)  # Returns an array


def split_at_symbols(string: str):
    return re.split(r'[!@#$%^&*]+', string) # Returns an array


def convert_from_leet(string: str) -> str:
    new_string = ""
    for char in string:
        new_string = new_string + anti_leet_letters(char)
    return new_string


# TODO: I haven't found a foolproof way to calc it, consider other methods.
# The goal of this function is to detect if the string is random letters, symbols, and numbers
# This use https://github.com/casics/nostril as an import and nltk
# Nostril will fail if the sample is too small or gives both false positives and negatives.
# This still have false positives. (It will sometimes say a string is random when it isn not)
def is_random_string(string: str, debugging=False) -> bool:
    RANDOMNESS_THRESHOLD = 0  # Default is 0
    VIEW_SCOREING = False  # This is for super debugging, so I can track the where the score is coming from.
    randomness_score = 0
    unleeted_string = convert_from_leet(string)
    capital_split_array = split_capital_strings(string)
    pp_capital_split_array_unleeted = []  # Hold strings after capital split + unleet
    pp_symbols_capital_split_array = []  # Hold strings after capital split + unleet + symbols split

    # This is to deal with C@pta1nC@veM4n like strings because they will be seen as  C@pta1n C@ve M4n and not words
    for entry in capital_split_array:
        basic_unleet = anti_leet_letters(entry)

        # Be a bit more thorough
        more_unleet = basic_unleet.replace('@', 'A').replace('1', 'I').replace('3', 'E')

        # Don't double add an entry to the array
        if basic_unleet != more_unleet:
            pp_capital_split_array_unleeted.append(more_unleet)

        pp_capital_split_array_unleeted.append(anti_leet_letters(entry))

    # Process it again to remove other undesirables
    for entry in pp_capital_split_array_unleeted:
        split_string = re.split(r'[!@#$%^&*]+', entry)
        for x in split_string:
            pp_symbols_capital_split_array.append(x)

    if debugging is True:
        print('\n---- Start Array Info ----')
        print("capital_split_array : " + str(capital_split_array))
        print("pp_capital_split_array_unleeted : " + str(pp_capital_split_array_unleeted))
        print("pp_symbols_capital_split_array : " + str(pp_symbols_capital_split_array))
        print('----  End Array Info  ----\n')


    string_array = split_letter_strings(string)
    unleeted_array = split_letter_strings(unleeted_string)
    size_string_array = len(string_array)
    size_unleeted_array = len(unleeted_array)

    max_len_string_array = max(string_array, key=len)
    max_len_unleeted_array = max(unleeted_array, key=len)

    if debugging is True:
        print('Original String: ' + string)
        print('Unleet: ' + unleeted_string)

        print('Strings (' + str(size_string_array) + '): ' + str(string_array))
        print('Strings After Unleeting (' + str(size_unleeted_array) + '): ' + str(unleeted_array))
        print('Max Length String Array: ' + str(max_len_string_array))
        print('Max Length Unleeted Array: ' + str(max_len_unleeted_array))

    if size_string_array == size_unleeted_array:
        # If the array sizes don't change its probably random.
        if debugging is True:
            print("-->Didn't Shrink")
        randomness_score += 2
        if VIEW_SCOREING is True:
            print("+2")

    if len(max_len_unleeted_array) >= len(string)/2:
        # If the unleeted_string is half or more it's not really random... ?
        if debugging is True:
            print("-->The string seems to be too long, so prob not random")
        randomness_score -= 2
        if VIEW_SCOREING is True:
            print("-2")

    # Combine arrays
    merged_array = []
    for elem in string_array + unleeted_array + capital_split_array + pp_capital_split_array_unleeted + pp_symbols_capital_split_array:
        normalize_case = elem.lower()
        if normalize_case not in merged_array:
            merged_array.append(normalize_case)

    #print(str(merged_array))

    # Check the array
    for x in merged_array:
        potential_word = x.lower()
        if len(potential_word) > 2:  # Skip words less than 2-letters long

            # Use nltk to check for the array for dictionary words
            if potential_word in set_of_words:
                if debugging is True:
                    print("-->Real word?: " + potential_word)

                word_length = len(potential_word)

                if word_length == 2:
                    randomness_score -= 1
                    if VIEW_SCOREING is True:
                        print("-1")
                elif word_length == 3 or word_length == 4:
                    randomness_score -= 2
                    if VIEW_SCOREING is True:
                        print("-2")
                else:  # more than 5-letter word that can't be random mistake
                    randomness_score -= 5
                    if VIEW_SCOREING is True:
                        print("-5")
            else:
                randomness_score += 0.2
                if VIEW_SCOREING is True:
                    print("+0.2")
            # End nltk check

    # This seems to have more of an impact on random strings
    # Use nostril check randomness - it does have false pos and false negs tho.
    try:
        if nonsense(unleeted_string):
            if debugging is True:
                print("Is NostrilNonsense: " + str(nonsense(unleeted_string)))
            randomness_score += 2
            if VIEW_SCOREING is True:
                print("+2")
    except:  # Have this here, so it doesn't blow up when the string is too short.
        pass

    if debugging is True:
        print("Random Score: " + str(randomness_score))
        print("IsRandom: " + str(randomness_score >= RANDOMNESS_THRESHOLD))
        print('\n-----------------\n')

    return randomness_score >= RANDOMNESS_THRESHOLD






if __name__ == '__main__':
    pass_s = [
        "9Sk5yRyY2^8D",
        "PoLHrs#jG!a#zaU!zXPbfSCk%an4#6yx",
        "M8wyg5sYg8P^L9",
        "WDcrQBnAtfDtn4Tg$#W96At86tJh%t3F"
    ]
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
        if is_random_string(s) is False:
            print(s)


