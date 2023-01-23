"""
This is a pytest to make sure that none of the helper functions in password_checker.py are corrupted
"""

import pytest
import password_checker


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
    # TODO: Pytest for count_symbols