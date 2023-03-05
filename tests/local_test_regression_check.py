"""
This shouldn't be used as a production test because it can through a lot of issues
This is just to test if things work more or less.
"""
import pytest

from python_scripts.password_analysis_helper import is_random_string


class TestPasswordAnalysisRegressionCheck:
    @pytest.mark.skip(reason="Don't run this on production")
    def test_real_random_passwords(self):
        random_passwords = []
        with open("../example_passwords/random_passwords.txt") as file:
            for line in file:
                random_passwords.append(line.strip())
        for s in random_passwords:
            assert is_random_string(s) is True

    # This part will likely bug out
    @pytest.mark.skip(reason="This will bug out")
    def test_valid_passwords(self):
        random_passwords = []
        with open("../example_passwords/valid_passwords.txt") as file:
            for line in file:
                random_passwords.append(line.strip())
        for s in random_passwords:
            assert is_random_string(s) is False
