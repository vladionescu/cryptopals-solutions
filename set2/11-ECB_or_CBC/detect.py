#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto.Random import random
import os
from Utils import Op

def main():
    plaintext = "A" * 90

    """The chosen plaintext will have 5-10 random bytes added before and after
    it and then it will be encrypted with a random unknown key in either ECB or
    CBC mode (chosen randomly)."""
    key = os.urandom(16)
    prepend = os.urandom( random.randint(5, 10) )
    append = os.urandom( random.randint(5, 10) )

    to_encrypt = Op.pkcs7_string(prepend + plaintext + append, 16)

    if random.randint(0, 1):
        print "[+] Mode: CBC"
        IV = os.urandom(16)
        aes = AES.new(key, AES.MODE_CBC, IV)
    else:
        print "[+] Mode: ECB"
        aes = AES.new(key, AES.MODE_ECB)

    ciphertext = aes.encrypt(to_encrypt)

    print "[+] Plaintext: " + plaintext
    print "[+] Key: " + key
    print "[+] To Encrypt: " + to_encrypt 
    print "[+] Ciphertext: " + ciphertext
    print "[+] ECB? " + str(Op.is_ecb_mode(ciphertext))

if __name__ == "__main__":
    main()
