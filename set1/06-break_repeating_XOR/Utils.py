#!/usr/bin/env python
import sys, binascii

class Convert(object):
    @staticmethod
    def hex_b64(hex_string):
        binary = binascii.unhexlify(hex_string)
        return binascii.b2a_base64(binary)

    """Given a string such as 'test' return a list of bytestrings,
    in this case ['01110100', '01100101', '01110011', '01110100']"""
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

if __name__ == "__main__":
    print "This is a module."
