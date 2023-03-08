[![GitHub Super-Linter](https://github.com/Yorzaren/authentication-system-leak-detection/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

# Table of Contents
1. [About](#about)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Development Testing/Style Notes](#style--linting--unit-testing)


# About
This is a work in progress.


This project is an experimental proof of concept.


The goal is to detect a password database breach by hiding the users password with a bunch of decoy passwords.
If an attacker gets the password database, they should have a hard time figuring out which of the many passwords associated with a single account is the real password. 
If they use a decoy password while attempting to get into a user's account, it will alert the admin to a possible database leak.


**Project Requirements:**

1. Must use at least 10 false passwords per account.
2. Creation of user account must randomly create associated false passwords in similar format to avoid detection.  
3. Changing of user account password must regenerate associated false passwords in similar format to avoid detection.  
4. Allow for deletion of accounts.
5. Must develop algorithm to uniquely assign valid password in user's account password list.
6. Provide a mechanism of notification if false password is used compared to incorrect entry or simple guess.
7. Runs on Linux.

# Installation
The project is intended Linux based systems. 

## Requirements
- Git
- Python
- Pip
- MySQL (or MariaDB)

## Install Git, Pip, MySQL
These instructions are for Ubuntu 22.04.2 LTS but might work for other versions. 

### Linux
You should already have Python3. 

If you don't already have these, install them now:
```cmd
apt install git
```

```cmd
apt install python3-pip
```

```cmd
sudo apt install mysql-server
```

### Windows
You need to have Git, Python3, and MySQL on your system if you don't already have them installed.

You can download Git from <https://git-scm.com/download/win>.

You can download Python from <https://www.python.org/>.

**Note:** When you install Python add it to the PATH and install pip.

You can download MySQL from <https://dev.mysql.com/downloads/>. 

The easiest way is to get MySQL Installer. You only need to install the database. When using the installer, you are given a prompt to configure the database with a password. 


**_Make sure you remember the password for later._**


## Clone the repository
```cmd
git clone https://github.com/Yorzaren/authentication-system-leak-detection.git
```

## Install Requirements
```cmd
pip install -r requirements.txt
```

## Set up the Database
Open MySQL / MariaDB as root to change the password.

### Linux
MySQL's installation is a bit bugged on Linux.

If you have issues, go [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04).

```cmd
mysql -u root -p
```

Default password is blank, so you should be able to hit enter and login.

```cmd
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpassword');
```

`newpassword` can be set to whatever you want the password to be.

**_Make sure you remember the password for later._**

See: <https://stackoverflow.com/a/64550826>

### Windows
You should have already setup the password for the database when you installed it.

## Initialize the Database

### Linux
Copy the path of `initialize_database.sql` located in the root of the repository

```cmd
readlink -f initialize_database.sql
```

Open MySQL or MariaDB

```cmd
mysql -u root -p
```

You should see `MariaDB[none]>` or `mysql>`.

Initialize the database with the following command:

```cmd
source [path of initialize_database.sql]
```

### Windows
Find and run the MySQL Command Line Client. 

Enter the password.

You should see `MariaDB[none]>` or `mysql>`.

Then enter:

```txt
source [path of initialize_database.sql]
```

## Create the .env

In the root of the `authentication-system-leak-detection` folder you need to make a file called `.env`

It should look something like this:
```txt
DB_PASSWORD=password
RANDOM_NOISE=somestring
RANDOM_NUMBER=123
FLASK_SECRET=secret
```

## Run cmdline_driver.py to Test
If you have everything setup, you should be able to run `cmdline_driver.py` to test if the scripts and database are communicating properly.

**Linux:**
```cmd
python3 cmdline_driver.py
```
**Windows:**
```cmd
python cmdline_driver.py
```

## Start Site Using Flask
```cmd
flask run
```

## Style / Linting / Unit Testing

### Python
[![Tested with Pytest](https://img.shields.io/badge/Tested%20with-Pytest-red?style=for-the-badge)](https://docs.pytest.org/)

Pytest files are found in the `tests` folder.

Run pytest from the root of the project.

You can test for coverage using:
```text
pytest --cov --cov-report=html
```

[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=for-the-badge)](https://github.com/psf/black)


```text
isort --profile black .
black --line-length 120 .
flake8 --append-config=.github/linters/.flake8
```

### JavaScript
[![Tested with QUnit](https://img.shields.io/badge/Tested%20with-QUnit-green?style=for-the-badge)](https://qunitjs.com/)

QUnit tests are located in the `tests` folder.

There is no style guide for the JavaScript code.

### CSS
[![Style: StyleLint](https://img.shields.io/badge/CSS%20Style-StyleLint-333.svg?style=for-the-badge)](https://stylelint.io/)


You can quickly bring the CSS into compliance with <https://stylelint.io/demo> using the settings at [.stylelintrc.json](https://github.com/Yorzaren/authentication-system-leak-detection/blob/main/.github/linters/.stylelintrc.json)
