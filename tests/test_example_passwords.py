"""
This just makes sure you haven't added something to the wrong file

The file used are located in examples folder

For some reason this test never wants to read the files in correctly.

If you use pycharm's built in runner it will have issues.

Running pytest in the root of the project is fine tho.

"""

from password_checker import password_valid_to_policy_rules


class TestPasswordExamples:
    def test_is_valid(self):
        with open("examples/example_valid_passwords.txt") as file:
            for line in file:
                # print(line.rstrip())
                assert password_valid_to_policy_rules(line.rstrip()) is True

    def test_is_invalid(self):
        with open("examples/example_invalid_passwords.txt") as file:
            for line in file:
                # print(line.rstrip())
                assert password_valid_to_policy_rules(line.rstrip()) is False

    def test_is_valid_random_password_list(self):
        with open("examples/example_random_passwords.txt") as file:
            for line in file:
                # print(line.rstrip())
                assert password_valid_to_policy_rules(line.rstrip()) is True
