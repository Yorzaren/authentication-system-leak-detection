import password_analysis_helper


class TestPasswordAnalysisHelper:
	def test_starts_with_uppercase_letter(self):
		assert password_analysis_helper.starts_with_uppercase_letter("asdasds") is False
		assert password_analysis_helper.starts_with_uppercase_letter("Asdasds") is True
		assert password_analysis_helper.starts_with_uppercase_letter("@sdasds") is False
		assert password_analysis_helper.starts_with_uppercase_letter("123sdasds") is False
		assert password_analysis_helper.starts_with_uppercase_letter("你$asdasds") is False

	def test_starts_with_lowercase_letter(self):
		assert password_analysis_helper.starts_with_lowercase_letter("asdasds") is True
		assert password_analysis_helper.starts_with_lowercase_letter("Asdasds") is False
		assert password_analysis_helper.starts_with_lowercase_letter("@sdasds") is False
		assert password_analysis_helper.starts_with_lowercase_letter("123sdasds") is False
		assert password_analysis_helper.starts_with_lowercase_letter("你$asdasds") is False

	def test_starts_with_digit(self):
		assert password_analysis_helper.starts_with_digit("asdasds") is False
		assert password_analysis_helper.starts_with_digit("Asdasds") is False
		assert password_analysis_helper.starts_with_digit("@sdasds") is False
		assert password_analysis_helper.starts_with_digit("123sdasds") is True
		assert password_analysis_helper.starts_with_digit("你$asdasds") is False
