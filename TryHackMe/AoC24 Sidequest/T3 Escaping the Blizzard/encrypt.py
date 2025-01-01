import os

with open("recommended-passwords.txt","r") as f:
        passwords = f.read().split("\n")

for password in passwords:
        os.system(f"./enc {password} >> encrypted_passwords.txt")

