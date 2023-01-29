import password_checker


# The starts_with and ends_with functions return booleans

def starts_with_uppercase_letter(string):
	return string[0].isupper()


def starts_with_lowercase_letter(string):
	return string[0].islower()


def starts_with_digit(string):
	return string[0].isdigit()


def starts_with_symbol(string):
	return string[0] in password_checker.ALLOWED_SPECIAL_CHAR


def ends_with_uppercase_letter(string):
	return string[-1].isupper()


def ends_with_lowercase_letter(string):
	return string[-1].islower()


def ends_with_digits(string):
	return string[-1].isdigit()


def ends_with_symbols(string):
	return string[-1] in password_checker.ALLOWED_SPECIAL_CHAR
