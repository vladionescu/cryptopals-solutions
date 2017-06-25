#!/usr/bin/env python
from __future__ import division
from Crypto.Cipher import AES
from Crypto.Random import random
from collections import Counter
from math import ceil
import binascii, os
from Utils import Op

key = os.urandom(16)

secret_plaintext  = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
secret_plaintext += "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
secret_plaintext += "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
secret_plaintext += "YnkK"

aes = AES.new(key, AES.MODE_ECB)

def main():
    """First, find out the block mode and block size by prepending the unknown
    string that is being encrypted with a set of known text we control."""
    keysizes = []
    ecb_modes = []
    for size in xrange(100):
        controlled_plaintext = "A" * size

        ciphertext = oracle(controlled_plaintext)

        """Detect the keysize, even though we know it is 16."""
        possible_keysizes = Op.guess_keysizes(ciphertext)
        keysizes.append(possible_keysizes[0][0])

        """Detect whether we're using ECB mode, even though we know."""
        ecb_modes.append(Op.is_ecb_mode(ciphertext))

    ecb_mode = Counter(ecb_modes).most_common()[0][0]
    keysize = Counter(keysizes).most_common()[0][0]
    print "[+] Is ECB Mode? " + str(ecb_mode)
    print "[+] Guessed Block Size: " + str(keysize)

    """Determine number of blocks the secret string takes up."""
    ciphertext_secret_string = oracle("")
    nr_secret_blocks = int( ceil( len(ciphertext_secret_string) / keysize ) )
    print "[+] Secret blocks: {}".format(nr_secret_blocks)

    """Crack the secret string."""
    cracked_secret = ""
    cracked_block = ['A'] * keysize
    for block in xrange(nr_secret_blocks):
        """Count down from [keysize-1] to 0, in order to address each byte in
        the block we're trying to crack, starting at the end and working
        towards the first byte."""
        for target_byte in xrange(keysize-1, -1, -1):
            """Encrypt a block of chosen plaintext (start with all A's) that is
            one byte short of a complete block, this will make the last byte of
            this block contain the first byte of the secret plaintext. Then
            compare the resulting ciphertext for this block with a dictionary
            of known plaintext to ciphertext mappings and determine what that
            last byte is, therefore revealing the plaintext first byte of the
            secret string. Repeat this with the block being two bytes short,
            then three, and so on until we have revealed the whole first block.
            Then repeat it starting from one byte short with the second block
            of the secret."""

            short_block = ['A'] * target_byte

            """Get the first block of the ciphertext."""
            start_block = keysize * block
            end_block = (keysize * block) + keysize
            encrypted_oracle = oracle( list_str(short_block) )
            encrypted_oracle_block = encrypted_oracle[start_block:end_block]

            """Knowing the ciphertext, craft plaintext blocks until one of them
            encrypts to match the known ciphertext (encrypted oracle block).
            When that is found, the oracle block's plaintext has been
            revealed."""
            for char in xrange(256):
                lookup_block = cracked_block[1:] + [chr(char)]
                lookup_cipher = aes.encrypt( list_str(lookup_block) )

                if lookup_cipher in encrypted_oracle_block:
                    cracked_block = lookup_block
                    break

        """A block was cracked! Add it to the result."""
        cracked_secret += list_str(cracked_block)

    print "[+] Cracked secret string: \n{}".format(cracked_secret)

"""The controlled_plaintext will have secret_plaintext appended to it and then
it will be encrypted with a random unknown key in ECB mode."""
def oracle(chosen_plaintext):
    plaintext = chosen_plaintext + binascii.a2b_base64(secret_plaintext)
    to_encrypt = Op.pkcs7_string(plaintext, 16)

    return aes.encrypt(to_encrypt)

def list_str(list_obj):
    return "".join(list_obj)

if __name__ == "__main__":
    main()
