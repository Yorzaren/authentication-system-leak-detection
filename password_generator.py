import password_checker
from password_generator_helper import change_case, random_date, random_4_numbers, leet_letters, anti_leet_letters, convert_4_digits
from password_checker import count_uppercase, count_lowercase, count_digits, count_special_char

"""
Type of passwords:
- Passwords that wont be remembered
- Passwords with social engineering weakness (dates/pet names/important life people)
- Passwords of immaturity (69, 420)
- Passwords on keys patterns (probably wont be addressing this)
- Passwords of fandom/pop culture

"""


def password_analysis(real_password):
    upper_count = count_uppercase(real_password)
    lower_count = count_lowercase(real_password)
    digit_count = count_digits(real_password)
    special_char_count = count_special_char(real_password)
    print(
        "password: " + real_password + "\n" +
        "upper_count: " + str(upper_count) + "\n" +
        "lower_count: " + str(lower_count) + "\n" +
        "digit_count: " + str(digit_count) + "\n" +
        "special_char_count: " + str(special_char_count)
    )
    print("------------")
    print(
        "policy diff upper_count: " + str(upper_count - password_checker.MIN_UPPERCASE_LETTERS) + "\n" +
        "policy diff lower_count: " + str(lower_count - password_checker.MIN_LOWERCASE_LETTERS) + "\n" +
        "policy diff digit_count: " + str(digit_count - password_checker.MIN_AMOUNT_DIGITS) + "\n" +
        "policy diff special_char_count: " + str(special_char_count - password_checker.MIN_AMOUNT_SPECIAL_CHAR) + "\n"
    )



def generate_fakes(real_password="", amount=10):
    for i in range(0, amount):
        password_analysis(real_password)
        #convert_4_digits(real_password)


"""
for i in range(0, 1000):
    #print(random_date())
    print(randint(0, 1))
"""
"""
password_convert("THis!i5AnAlert0963")
password_convert("sdfjkhuih3240")
password_convert("3423!6561")
password_convert("ifh3499mlerm@0346")
password_convert("marrywe1299")
password_convert("123mar3rywe1299")
password_convert("1234!Cc1234")"""


#convert_4_digits("45dsifji34")


#generate_fakes("45dsifji34")
generate_fakes("THis!i5AnAlert0963", 2)
generate_fakes("1234!Cc1234", 2)
