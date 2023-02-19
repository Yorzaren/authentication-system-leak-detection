"""
This code will eventually call all the other scripts for their various functions
- Add user to database
---> Check if username requirements
        On PASS:
            --> generate the passwords
            --> calc where to place the real password
            --> place in database


- Delete user from database
---> Check the user is admin
---> Then check the username exists then delete
            If it doesnt exist return the message that the username doesn't exist

- Log a user in
--> Login requires to check the username exists
----> If the username doesn't exist return that the credentials are incorrect.
            Don't tell them the username doesn't exist
----> If it does exist calculate where the correct password is located.
    --> After the calc check if the username and password are correct
            If correct log them in
            Else check if the password is a decoy
                if not a decoy increase the incorrect counter
                When incorrect counter  == 10 lock the account



It will also be used to connect to the database


"""
RANDOM_NOISE = "1CPj3KSeCpaRlu6FvfG6"  # A string
RANDOM_NUMBER = 383369324388255133968499854491  # An int
NUMBER_OF_PASSWORDS = 11  # An int, N total passwords (1 real + N-1 decoy passwords)


# For this it shouldn't matter what (simple) algorithm we use for the proof of concept
# because any method of hiding it is constrained to the database having N passwords (1 real + N-1 decoy passwords)
# For this to be secure it require that no one gets the code behind the password hiding.
# This will take a string and return an int to be used as the array index
def hide_password(username: str) -> int:
    char_sum = 0
    username = username + RANDOM_NOISE
    for char in username:
        char_sum += ord(char)

    placement = (char_sum * RANDOM_NUMBER) % NUMBER_OF_PASSWORDS

    print(placement)

    return placement
