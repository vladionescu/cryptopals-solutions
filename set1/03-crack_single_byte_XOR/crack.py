#!/usr/bin/env python
from __future__ import division
import operator
import binascii

verbose = True

# A-Z and space
english_freqs = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442,
        0.0197881, 0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529,
        0.0331490, 0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606,
        0.0497563, 0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272,
        0.0013692, 0.0145984, 0.0007836, 0.1918182]

# Ciphertext
hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def main():
    binary = binascii.unhexlify(hex_string)

    if verbose:
        print "Encrypted string (hex): " + hex_string
        print "Encrypted string (dec): " + " ".join([str(ord(a)) for a in binary])

    '''
        - run through 0-255 (possible keys), XORing the ciphertext with each value
        - store the results in a dict along with each results' freq count
        - get the top 3 freqs and display the results
    '''
    possible_plaintexts = dict()

    for key in xrange(256):
#    for key in [88]: # The correct XOR key, just to test
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
def score_string(string):
    char_counts = [0] * 27
    total_chars = 0

    for char in string.upper():
        index = ord(char) - ord('A')

        if 0 <= index < 26:
            # Count the capital latin letters
            char_counts[index] += 1
            total_chars += 1
        elif char == ' ':
            # Count the spaces
            char_counts[26] += 1
            total_chars += 1
        else:
            # Not a character we're counting
            pass

    # Avoid division by zero, in case none of the chars were ones we care about
    if total_chars == 0:
        total_chars = 1

    chi_squared_score = 0
    char_freqs = [None] * 27

    # Calculate the score, lower is better (more congruent with English)
    for i in xrange(len(english_freqs)):
        char_freqs[i] = char_counts[i] / total_chars
        numerator = char_freqs[i] - english_freqs[i]
        chi_squared_score += (numerator * numerator) / english_freqs[i]

    # 1.0 means no English letters or spaces were found in the text
    # Return an unreasonably high score to ensure this text is marked bad
    if chi_squared_score == 1.0:
        return 9999.99
    else:
        return chi_squared_score

if __name__ == "__main__":
    main()
