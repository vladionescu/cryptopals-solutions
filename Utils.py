#!/usr/bin/env python
from __future__ import division
import binascii, operator, sys

class Convert(object):
    @staticmethod
    def hex_b64(hex_string):
        binary = binascii.unhexlify(hex_string)
        return binascii.b2a_base64(binary)

    """Given a string such as 'test' return a list of bytestrings, in this case
    ['01110100', '01100101', '01110011', '01110100']"""
    @staticmethod
    def string_bytelist(string):
        return ['{0:08b}'.format(ord(char), 'b') for char in string]

class Op(object):
    @staticmethod
    def xor(hex1, hex2):
        bin1 = binascii.unhexlify(hex1)
        bin2 = binascii.unhexlify(hex2)

        xor = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(bin1, bin2)])

        return binascii.hexlify(xor)

    @staticmethod
    def repeating_xor(plaintext, key_string):
        get_chunk = lambda x,y: [ x[i:i+y] for i in range(0, len(x) ,y) ]

        xor_hex = ""

        for chunk in get_chunk(plaintext, len(key_string)):
            xor_hex += Op.xor(binascii.hexlify(chunk), binascii.hexlify(key_string))

        return xor_hex

    """Calculate the Hamming distance between two strings"""
    @staticmethod
    def string_hamming_distance(string1, string2):
        distance = 0

        for x,y in zip(Convert.string_bytelist(string1), Convert.string_bytelist(string2)):
            distance += Op.bitstring_hamming_distance(x, y)

        return distance

    """Calculate the Hamming distance between two strings of bits
    Ex: x_str = '1010', y_str = '1111', count = 2
    https://stackoverflow.com/a/31007941"""
    @staticmethod
    def bitstring_hamming_distance(x_str, y_str):
        assert len(x_str) == len(y_str)
        x, y = int(x_str, 2), int(y_str, 2)
        count, z = 0, x ^ y
        while z:
            count += 1
            z &= z - 1  # magic!
        return count

    """Calculate the Chi Squared score for a given string to determine how
    closely it resembles an English string based on letter (and space)
    frequency. Lower scores are best, high scores indicate the string is not
    very English-like and may not contain many Latin characters.

    This assumes the plaintext is a clean English string
    
    https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
    """
    @staticmethod
    def score_english_string(string):
        # A-Z and space
        english_freqs = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442,
                0.0197881, 0.0158610, 0.0492888, 0.0558094, 0.0009033,
                0.0050529, 0.0331490, 0.0202124, 0.0564513, 0.0596302,
                0.0137645, 0.0008606, 0.0497563, 0.0515760, 0.0729357,
                0.0225134, 0.0082903, 0.0171272, 0.0013692, 0.0145984,
                0.0007836, 0.1918182]

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

    """Run through 0-255 (possible keys), XORing the ciphertext with each
    value.
    
    Returns the results as a sorted dict containing each results' freq
    count in the format { plaintext : ChiSquared , ... } with the most
    likely result (lowest ChiSquared score, indicating it is most likely
    English text) first."""
    @staticmethod
    def try_xor_decryptions(ciphertext_string):
        possible_plaintexts = dict()
        
        for key in xrange(256):
            xored_string = "".join([chr(ord(char) ^ key) for char in ciphertext_string])
            freq = Op.score_english_string(xored_string)

            possible_plaintexts.update({ xored_string : freq })

        possible_plaintexts = sorted(possible_plaintexts.items(), key=operator.itemgetter(1))

        return possible_plaintexts

if __name__ == "__main__":
    print "This is a module."
