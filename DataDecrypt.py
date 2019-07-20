"""

This is the function to decrypt sensitive data in a file. This function require "cryptography" library.

"""

import cryptography

from cryptography.fernet import Fernet

class DecryptProcess():

    def __init__(self, mykey, message):

        self.mykey = mykey

        self.message = message

    def decrypt(self):

        # Decrypt the message

        g = Fernet(self.mykey)

        decrypted = g.decrypt(self.message)

        original_password = decrypted.decode()

        return original_password

