from python_scripts.alg_redux import generate_decoy_passwords_redux
from python_scripts.password_generator import generate_decoy_passwords
from tabulate import tabulate
import random

table = [[1, 2222, 30, 500], [4, 55, 6777, 1]]
print(tabulate(table))

with open("example_passwords/valid_passwords.txt") as file:
    for line in file:
        password = line.rstrip()  # Normalize it to remove the \n

        # Make the arrays
        array_decoys_gen1 = generate_decoy_passwords(password)
        array_decoys_gen2 = generate_decoy_passwords_redux(password)

        # Append the real password in side of it of the decoy arrays
        array_decoys_gen1.append(password)
        array_decoys_gen2.append(password)

        # Shuffle them
        random.shuffle(array_decoys_gen1)
        random.shuffle(array_decoys_gen2)

        table = [["Original Algorithm", "New Algorithm"]]
        for i in range(len(array_decoys_gen2)):
            row = [array_decoys_gen1[i], array_decoys_gen2[i]]
            table.append(row)

        print(f"----------- {password} -----------")
        print(tabulate(table))
        print("\n")
