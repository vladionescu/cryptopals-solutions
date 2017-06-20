#!/usr/bin/env python
import sys, binascii

class Convert(object):
    @staticmethod
    def hex_b64(hex_string):
        binary = binascii.unhexlify(hex_string)
        return binascii.b2a_base64(binary)

if __name__ == "__main__":
    print "This is a module."
