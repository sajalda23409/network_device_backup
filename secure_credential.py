"""

Run this program for one time to make your device login credentials secure and encrypted.

"""
from getpass import getpass

import os

import shutil

# User defined class

from DataEncrypt import EncryptProcess

# My key file

keyfile = "key.key"

# Asking for credentials

username = input("Confirm your device login username:")

password = getpass("Confirm your device login password:")

# Planning my path details

myactualpath = os.getcwd()

my_cred_folder_path = myactualpath + "\\Cred"

mytemppath = myactualpath + "\\Cred\\" + username

# Checking if "Cred" dir exists or not, if not, create the directory

if os.path.exists(my_cred_folder_path) == False:

    os.mkdir(my_cred_folder_path)

# Checking if "username" dir exist or not, if exist then delete and create a new one, else create a fresh one

if os.path.exists(mytemppath) == True:

    os.chdir(my_cred_folder_path)

    # Delete the existing username folder and its content

    shutil.rmtree(username)

    os.chdir(myactualpath)

    os.mkdir(mytemppath)

    os.chdir(mytemppath)

elif os.path.exists(mytemppath) == False:

    os.mkdir(mytemppath)

    os.chdir(mytemppath)

# Start securing the password

secure = EncryptProcess(password)

gen_key = secure.createkey()

my_sec_pass = secure.encrypt(gen_key)

# Storing the secret key in key.key file

with open(keyfile, 'wb') as my_key_file:

    my_key_file.write(gen_key)

my_key_file.close()

# Storing the secure credential in the username.txt file

with open(username+".txt", 'wb') as my_cred_file:

        my_cred_file.write(my_sec_pass)

my_cred_file.close()

# Going back to original position of the directory

os.chdir(myactualpath)
