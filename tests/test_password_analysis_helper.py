import password_analysis_helper


class TestPasswordAnalysisHelper:
	# starts_with test
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

	def test_starts_with_symbol(self):
		assert password_analysis_helper.starts_with_symbol("asdasds") is False
		assert password_analysis_helper.starts_with_symbol("Asdasds") is False
		assert password_analysis_helper.starts_with_symbol("@sdasds") is True
		assert password_analysis_helper.starts_with_symbol("123sdasds") is False
		assert password_analysis_helper.starts_with_symbol("你$asdasds") is False

	# ends_with tests
	def test_ends_with_uppercase_letter(self):
		assert password_analysis_helper.ends_with_uppercase_letter("SJRHerisdf") is False
		assert password_analysis_helper.ends_with_uppercase_letter("ajsdfh(213U") is True
		assert password_analysis_helper.ends_with_uppercase_letter("dsfsdf34*") is False
		assert password_analysis_helper.ends_with_uppercase_letter("kljko@sdg1") is False
		assert password_analysis_helper.ends_with_uppercase_letter("sdikfj32(2jJ好") is False

	def test_ends_with_lowercase_letter(self):
		assert password_analysis_helper.ends_with_lowercase_letter("SJRHerisdf") is True
		assert password_analysis_helper.ends_with_lowercase_letter("ajsdfh(213U") is False
		assert password_analysis_helper.ends_with_lowercase_letter("dsfsdf34*") is False
		assert password_analysis_helper.ends_with_lowercase_letter("kljko@sdg1") is False
		assert password_analysis_helper.ends_with_lowercase_letter("sdikfj32(2jJ好") is False

	def test_ends_with_digits(self):
		assert password_analysis_helper.ends_with_digits("SJRHerisdf") is False
		assert password_analysis_helper.ends_with_digits("ajsdfh(213U") is False
		assert password_analysis_helper.ends_with_digits("dsfsdf34*") is False
		assert password_analysis_helper.ends_with_digits("kljko@sdg1") is True
		assert password_analysis_helper.ends_with_digits("sdikfj32(2jJ好") is False

	def test_ends_with_symbols(self):
		assert password_analysis_helper.ends_with_symbols("SJRHerisdf") is False
		assert password_analysis_helper.ends_with_symbols("ajsdfh(213U") is False
		assert password_analysis_helper.ends_with_symbols("dsfsdf34*") is True
		assert password_analysis_helper.ends_with_symbols("kljko@sdg1") is False
		assert password_analysis_helper.ends_with_symbols("sdikfj32(2jJ好") is False
