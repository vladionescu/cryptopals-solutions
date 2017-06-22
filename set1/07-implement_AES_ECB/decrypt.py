#!/usr/bin/env python
import binascii
from Crypto.Cipher import AES

def main():
    b64_string = ""
    key = "YELLOW SUBMARINE"

    """The file contains ASCII armor: newline separated base64'd binary data
    (the ciphertext). Extract it work directly with the binary."""
    with open('7.txt', 'r') as f:
        for line in f:
            b64_string += line.strip()

    ciphertext = binascii.a2b_base64(b64_string)

    aes = AES.new(key, AES.MODE_ECB)

    plaintext = aes.decrypt(ciphertext)

    print plaintext

if __name__ == "__main__":
    main()
