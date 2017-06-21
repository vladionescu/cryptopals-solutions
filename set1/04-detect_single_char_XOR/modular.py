#!/usr/bin/env python
from __future__ import division
from Utils import Op
import binascii, operator

verbose = False

def main():
    possible_plaintexts = dict()

    # Ciphertext file with many 60 char strings, one of which should decrypt to English
    with open('4.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            binary = binascii.unhexlify(hex_string)

            if verbose:
                print "Encrypted string (hex): " + hex_string
                print "Encrypted string (dec): " + " ".join([str(ord(a)) for a in binary])
            
            possible_plaintexts.update(Op.try_xor_decryptions(binary))

    possible_plaintexts = sorted(possible_plaintexts.items(), key=operator.itemgetter(1))

    if verbose:
        for plaintext, freq in possible_plaintexts:
            print "(" + str(freq) + "): " + plaintext

    print "Best guess: " + possible_plaintexts[0][0]

if __name__ == "__main__":
    main()
