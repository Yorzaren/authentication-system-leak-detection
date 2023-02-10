# authentication-system-leak-detection

[![GitHub Super-Linter](https://github.com/Yorzaren/authentication-system-leak-detection/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)



## About
This is a work in progress.


This project is an experimental proof of concept.


The goal is to detect a password database breach by hiding the users password with a bunch of decoy passwords. 
If an attacker gets the password database, they should have a hard time figuring out which of the many passwords associated with a single account is the real password. 
If they use a decoy password while attempting to get into a user's account, it will alert the admin to a possible database leak.

<details><summary>Project Details</summary>
<p>

**Requirements:**

1. Must use at least 10 false passwords per account.
2. Creation of user account must randomly create associated false passwords in similar format to avoid detection.  
3. Changing of user account password must regenerate associated false passwords in similar format to avoid detection.  
4. Allow for deletion of accounts.
5. Must develop algorithm to uniquely assign valid password in user's account password list.
6. Provide a mechanism of notification if false password is used compared to incorrect entry or simple guess.
</p>
</details>

<details><summary><h2>Style / Linting / Unit Testing</h2></summary>

### Python
[![Tested with Pytest](https://img.shields.io/badge/Tested%20with-Pytest-red?style=for-the-badge)](https://docs.pytest.org/)

Pytest files are found in the `tests` folder.

[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=for-the-badge)](https://github.com/psf/black)


```text
isort --profile black
black --line-length 120
flake8 --max-line-length 120
```

### JavaScript
[![Tested with QUnit](https://img.shields.io/badge/Tested%20with-QUnit-green?style=for-the-badge)](https://qunitjs.com/)

QUnit tests are located in the `tests` folder.

There is no style guide for the JavaScript code.
</details>