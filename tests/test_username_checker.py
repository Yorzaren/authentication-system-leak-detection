"""
This is a pytest to make sure that none of the helper functions in username_checker.py are corrupted
"""

import username_checker


class TestUsernameCheckerFunctions:
    def test_is_valid_username(self):
        assert username_checker.is_valid_username("asda") is False  # Too few letters
        assert username_checker.is_valid_username("asdaa") is True  # Meets the min
        assert (
            username_checker.is_valid_username("asdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaa") is True
        )  # Meets the max
        assert (
            username_checker.is_valid_username("asdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaaasdaaa") is False
        )  # Max + 1
        assert username_checker.is_valid_username("asfj1212") is True
        assert username_checker.is_valid_username("1sdf234") is True
        assert username_checker.is_valid_username("1sdf2_34") is False  # Only digits and A-Z
        assert username_checker.is_valid_username("1sdf2你34") is False  # Only digits and A-Z
