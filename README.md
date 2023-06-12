# authentication-system-leak-detection

[![GitHub Super-Linter](https://github.com/Yorzaren/authentication-system-leak-detection/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Table of Contents
1. [About](#about)
2. [Contributors](#contributors)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Development Testing/Style Notes](#style--linting--unit-testing)


## About
This is a work in progress.


⚠️ This project is an experimental proof of concept. ⚠️


The goal is to detect a password database breach by hiding the user's password with a bunch of decoy passwords.
If an attacker gets the password database, they should have a hard time figuring out which of the many passwords associated with a single account is the correct password. 
If they use a decoy password while attempting to get into a user's account, it will alert the admin to a possible database leak.


**Project Requirements:**

1. Must use at least 10 false passwords per account.
2. Creation of user account must randomly create associated false passwords in similar format to avoid detection.  
3. Changing of user account password must regenerate associated false passwords in similar format to avoid detection.  
4. Allow for deletion of accounts.
5. Must develop algorithm to uniquely assign valid password in user's account password list.
6. Provide a mechanism of notification if false password is used compared to incorrect entry or simple guess.
7. Runs on Linux.

## Contributors 
This repository is a part of Senior Project where teams are assigned a real world client to create a solution for their problem(s) based off of their requirements.

**Password F.M.** is the name of our team.

### Members
* F. Nice ([Yorzaren](https://github.com/Yorzaren)) - Project Leader/Lead Developer
* J. Hopper ([Mega-Zawesome](https://github.com/Mega-Zawesome))
* M. James ([Mikaylabj98](https://github.com/Mikaylabj98))
* J. Lewis ([jalewis7](https://github.com/jalewis7))

## Installation
The project is intended Linux based systems. 

### Requirements
- Git
- Python
- Pip
- MySQL (or MariaDB)

### Install Git, Pip, MySQL
These instructions are for Ubuntu 22.04.2 LTS but might work for other versions. 

#### Linux - Install Git, Pip, MySQL
You should already have Python3. 

If you don't already have these, install them now:
```cmd
apt install git
```

```cmd
apt install python3-pip
```

```cmd
apt install mysql-server
```
Optional: 

Because there's a bug with MySQL installation, you may also use MariaDB instead. 
If you do, replace mysql command with mariadb.

```cmd
apt install mariadb-server
```

Note: You can quickly set the MariaDB root password using in the MariaDB console: 
```cmd
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password'; flush privileges; exit; 
```

If you want to run this in a venv (virtual environment):
```cmd
apt install python3.10-venv
```

Create venv:
```cmd
python3 -m venv venv
```
Activate venv:
```cmd
. venv/bin/activate
```

#### Windows - Install Git, Pip, MySQL
You need to have Git, Python3, and MySQL on your system if you don't already have them installed.

You can download Git from <https://git-scm.com/download/win>.

You can download Python from <https://www.python.org/>.

**Note:** When you install Python add it to the PATH and install pip.

You can download MySQL from <https://dev.mysql.com/downloads/>. 

The easiest way is to get MySQL Installer. You only need to install the database. When using the installer, you are given a prompt to configure the database with a password. 


**_Make sure you remember the password for later._**


### Clone the repository
```cmd
git clone https://github.com/Yorzaren/authentication-system-leak-detection.git
```

### Install Requirements
```cmd
pip install -r requirements.txt
```

### Set up the Database
Open MySQL / MariaDB as root to change the password.

#### Linux - Set up the Database
MySQL's installation is a bit bugged on Linux.

If you have issues, go [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04).

**_Make sure you remember the password for later._**

See: <https://stackoverflow.com/a/64550826>

#### Windows - Set up the Database
You should have already set up the password for the database when you installed it.

### Initialize the Database

#### Linux - Initialize the Database
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

#### Windows - Initialize the Database
<!-- textlint-disable -->
Find and run the MySQL Command Line Client. 
<!-- textlint-enable -->

Enter the password.

You should see `MariaDB[none]>` or `mysql>`.

Then enter:

```txt
source [path of initialize_database.sql]
```

### Create the .env

In the root of the `authentication-system-leak-detection` folder you need to make a file called `.env`

It should look something like this:
```txt
DB_USER=root
DB_PASSWORD=password
RANDOM_NOISE=somestring
RANDOM_NUMBER=123
FLASK_SECRET=secret
USE_MAILSLURP=False
MAILSLURP_API_KEY=
MAILSLURP_SENDER_EMAIL_ID=
MAILSLURP_RECEIVER_EMAIL_ID=
```
* `DB_PASSWORD` is the password to the database.
* `DB_USER` (optional) It defines the database user. The default is set to `root`. This variable is optional.
* `RANDOM_NOISE` (optional) It is a random string. Do NOT change this value after adding accounts.
* `RANDOM_NUMBER` (optional) It is a random int you can set. It is optional. Do NOT change this value after adding accounts.
  * If you change `RANDOM_NOISE` or `RANDOM_NUMBER` later on, the system will not be able to locate the correct passwords for accounts.
* `FLASK_SECRET` is a random string. It can NOT be left undefined. 
* `USE_MAILSLURP` (optional) See below for more info

The [MailSlurp](https://www.mailslurp.com/) variables are optional. The system automatically sends test emails to the local aiosmtpd server.

If you wish to use MailSlurp, set `USE_MAILSLURP` to `True`. 

MailSlurp can be used to send the test emails.

`MAILSLURP_API_KEY` refers to the 64 character long string. Its marked as `API KEY` on the dashboard.
`MAILSLURP_SENDER_EMAIL_ID` refers to the Inbox ID. `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`
`MAILSLURP_RECEIVER_EMAIL_ID` refers to an Inbox ID. `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`

Because free MailSlurp accounts have 1 permanent Inbox ID, it's easier to set the sender as that ID.
However, it doesn't really matter.

**Note:** Free MailSlurp users can only keep their Inbox IDs for a short duration, so you'll have to update the ID a lot.

### Run aiosmtpd mail server
In a separate terminal or command-line prompt, run:

**Linux:**
```cmd
python3 -m aiosmtpd -n -l localhost:1025
```

**Windows:**
```cmd
python -m aiosmtpd -n -l localhost:1025
```

**Note:** Don't close out of the window. You will see the emails being sent here.

### Run cmdline_driver.py to Test
If you have everything setup, you should be able to run `cmdline_driver.py` to test if the scripts and database are communicating properly.

**Linux:**
```cmd
python3 cmdline_driver.py
```
**Windows:**
```cmd
python cmdline_driver.py
```

### Start Site Using Flask
```cmd
flask --app web run
```

or 

**Windows:**
```cmd
win_start_site.bat
```

or 

**Linux:**
```cmd
lin_start_site.sh
```

The database has one default account to get you started. 

You can access it using the following information:

### Login to the Default Admin Account
Username: `admin`

Password: `password`

You should change the password to admin immediately for security.

Alternatively, you should create a new admin account, test that the new admin account works, then delete the default admin account.

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
