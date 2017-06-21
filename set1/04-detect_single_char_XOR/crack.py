#!/usr/bin/env python
from __future__ import division
from pprint import pprint
import operator
import binascii

verbose = False

# A-Z and space
english_freqs = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442,
        0.0197881, 0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529,
        0.0331490, 0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606,
        0.0497563, 0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272,
        0.0013692, 0.0145984, 0.0007836, 0.1918182]

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

            '''
                - run through 0-255 (possible keys), XORing the ciphertext with each value
                - store the results in a dict along with each results' freq count
            '''
            for key in xrange(256):
                xored_string = "".join([chr(ord(char) ^ key) for char in binary])
                freq = score_string(xored_string)

                if verbose:
                    print "XORed with " + str(key) + ", ChiSquared " + str(freq) + ": " + xored_string

                possible_plaintexts.update({ xored_string : freq })

    possible_plaintexts = sorted(possible_plaintexts.items(), key=operator.itemgetter(1))

    if verbose:
        for plaintext, freq in possible_plaintexts:
            print "(" + str(freq) + "): " + plaintext

    print "Best guess: " + possible_plaintexts[0][0]

# https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
# This assumes the plaintext is a clean English string
def score_string(string):
    char_counts = [0] * 27
    counted_chars = 0
    str_length = 0

    for char in string.upper():
        str_length += 1
        index = ord(char) - ord('A')

        # Unprintable and control chars indicate a bad decryption
        if ord(char) >= 128 or ord(char) < 10:
            return 9999.99

        if 0 <= index < 26:
            # Count the capital latin letters
            char_counts[index] += 1
            counted_chars += 1
        elif char == ' ':
            # Count the spaces
            char_counts[26] += 1
            counted_chars += 1
        else:
            # Not a character we're counting
            pass

    # Avoid division by zero, in case none of the chars were ones we care about
    if counted_chars == 0:
        counted_chars = 1

    chi_squared_score = 0
    char_freqs = [None] * 27

    # Calculate the score, lower is better (more congruent with English)
    for i in xrange(len(english_freqs)):
        char_freqs[i] = char_counts[i] / counted_chars
        numerator = char_freqs[i] - english_freqs[i]
        chi_squared_score += (numerator * numerator) / english_freqs[i]

    # Weigh by the number of characters we care about (A-Z and space) in the string
    chi_squared_score = chi_squared_score * (1 / (counted_chars / str_length))

    # 1.0 *probably* means no English letters or spaces were found in the text
    # Return an unreasonably high score to ensure this text is marked bad
    if chi_squared_score == 1.0:
        return 9999.99
    else:
        return chi_squared_score

if __name__ == "__main__":
    main()
