"""
This shouldn't be used as a production test because it can through a lot of issues
This is just to test if things work more or less.
"""

"""
from password_analysis_helper import is_random_string


class TestPasswordAnalysisRegressionCheck:
    def test_real_random_passwords(self):
        random_passwords = []
        with open("examples/example_random_passwords.txt") as file:
            for line in file:
                random_passwords.append(line.strip())
        for s in random_passwords:
            assert is_random_string(s) is True

    def test_valid_passwords(self):
        random_passwords = []
        with open("examples/example_valid_passwords.txt") as file:
            for line in file:
                random_passwords.append(line.strip())
        for s in random_passwords:
            assert is_random_string(s) is False
"""