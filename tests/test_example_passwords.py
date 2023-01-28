"""
This just makes sure you haven't added something to the wrong file
"""

from password_checker import password_valid_to_policy_rules


# TODO: THIS WILL BLOW UP ON THE CI IF YOU FORGET YOUR FILES WHICH YOU HAVE IGNORED
class TestPasswordExamples:
	def test_is_valid(self):
		with open("../examples/example_valid_passwords.txt") as file:
			for line in file:
				#print(line.rstrip())
				assert password_valid_to_policy_rules(line.rstrip()) is True

	def test_is_invalid(self):
		with open("../examples/example_invalid_passwords.txt") as file:
			for line in file:
				#print(line.rstrip())
				assert password_valid_to_policy_rules(line.rstrip()) is False
