"""

This is the function to encrypt sensitive data in a file. This function require "cryptography" library.

"""

import cryptography

from cryptography.fernet import Fernet


class EncryptProcess():

    def __init__(self, message):

        self.message = message

    def createkey(self):

        # Generating a key

        mykey = Fernet.generate_key()

        return mykey

    def encrypt(self, getkey):

        # Encode the message

        encoded = self.message.encode()

        # Encrypt the message

        f = Fernet(getkey)

        encrypted = f.encrypt(encoded)

        return encrypted










