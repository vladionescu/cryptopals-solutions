#!/usr/bin/env python
import sys, binascii

class Convert(object):
    @staticmethod
    def hex_b64(hex_string):
        binary = binascii.unhexlify(hex_string)
        return binascii.b2a_base64(binary)

class Op(object):
    @staticmethod
    def xor(hex1, hex2):
        bin1 = binascii.unhexlify(hex1)
        bin2 = binascii.unhexlify(hex2)

        xor = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(bin1, bin2)])

        return binascii.hexlify(xor)

if __name__ == "__main__":
    print "This is a module."

