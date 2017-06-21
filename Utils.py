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

    @staticmethod
    def repeating_xor(plaintext, key_string):
        get_chunk = lambda x,y: [ x[i:i+y] for i in range(0, len(x) ,y) ]

        xor_hex = ""

        for chunk in get_chunk(plaintext, len(key_string)):
            xor_hex += Op.xor(binascii.hexlify(chunk), binascii.hexlify(key_string))

        return xor_hex

if __name__ == "__main__":
    print "This is a module."

