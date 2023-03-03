"""
This is a pytest to make sure that none of the helper functions in password_checker.py are corrupted
"""

import password_checker

# Each test string is testing for one particular thing for the functionality.
# It is not necessary for them to match the password policy.


class TestPasswordCheckerFunctions:
    def test_count_uppercase(self):
        assert password_checker.count_uppercase("ttTU4hUa") == 3
        assert password_checker.count_uppercase("kNLa6V!@") == 3
        assert password_checker.count_uppercase("-SL(ddY*") == 3
        assert password_checker.count_uppercase("M.*X!(zi") == 2
        assert password_checker.count_uppercase("-?rC5z}*") == 1
        assert password_checker.count_uppercase("khvmThrG") == 2
        assert password_checker.count_uppercase("M,F*hkRa") == 3
        assert password_checker.count_uppercase("C]uqQ!=i") == 2
        assert password_checker.count_uppercase("!{.h]SSG") == 3
        assert password_checker.count_uppercase("rUPhQBFN") == 6
        assert password_checker.count_uppercase("SDF213DSDF") == 7

    def test_count_lowercase(self):
        assert password_checker.count_lowercase("ttTU4hUa") == 4
        assert password_checker.count_lowercase("kNLa6V!@") == 2
        assert password_checker.count_lowercase("-SL(ddY*") == 2
        assert password_checker.count_lowercase("M.*X!(zi") == 2
        assert password_checker.count_lowercase("-?rC5z}*") == 2
        assert password_checker.count_lowercase("khvmThrG") == 6
        assert password_checker.count_lowercase("M,F*hkRa") == 3
        assert password_checker.count_lowercase("C]uqQ!=i") == 3
        assert password_checker.count_lowercase("!{.h]SSG") == 1
        assert password_checker.count_lowercase("rUPhQBFN") == 2
        assert password_checker.count_lowercase("SDF213DSDF") == 0

    def test_count_digits(self):
        assert password_checker.count_digits("AS9SDK1") == 2
        assert password_checker.count_digits("12345678") == 8
        assert password_checker.count_digits("sdafjksdhfjksdfhsdukfhsisdfssdfsd") == 0
        assert password_checker.count_digits("sdgKJKJKJjuuhbmhJHUGBHNBkjk") == 0
        assert password_checker.count_digits("-?rC5z}*") == 1
        assert password_checker.count_digits("SDF213DSDF") == 3

    def test_count_special_char(self):
        assert password_checker.count_special_char("-?rC5z}*") == 1  # Only thing allowed is *
        assert password_checker.count_special_char("!@#$%^&*") == 8  # Matches all the allowed special chars
        assert password_checker.count_special_char("!@#E3b$%^&*") == 8  # Matches all the allowed special chars

    def test_has_forbidden_characters(self):
        assert password_checker.has_forbidden_characters("你123123DS好ca2@$%@346,.") is True  # 你
        assert password_checker.has_forbidden_characters("sdfkjsdēf398njdssdifu83!@#ds") is True  # ē
        assert password_checker.has_forbidden_characters("32SDJАF9JDH29N0") is True  # А is a cyrillic letter A
        assert password_checker.has_forbidden_characters("123.4567") is True  # dot is not in the list
        assert password_checker.has_forbidden_characters("213AD!sxd你") is True  # 你
        assert password_checker.has_forbidden_characters("123#%Txrte2323yrtyhrtyhrtyrtyrty3") is False  # This is fine

    def test_against_password_policy(self):
        test = [
            "123#%Txrte2323yrtyhrtyhrtyrtyrty3",  # 33 chars
            "sdfkjsdkf398njdssdifu83!@#ds",  # No cap
            "32SDJF9JDH29N0",  # no lower
            "SDJFasdaJDHN",  # no digits
            "Us!4567",  # too short
            "Us004567",  # no special characters
            "你好213AD!s12xd",  # has forbidden characters
        ]

        for i in range(len(test)):
            outcome = password_checker.password_valid_to_policy_rules(test[i], debugging=True)
            assert outcome is False  # All the passwords in test are going to fail

        # This is from valid_passwords.txt
        assert password_checker.password_valid_to_policy_rules("KeyboardW@rr10r") is True
