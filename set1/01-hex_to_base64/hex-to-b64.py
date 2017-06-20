#!/usr/bin/env python
import sys, binascii

if len(sys.argv) > 1:
    binary = binascii.unhexlify(sys.argv[1])
    print(binascii.b2a_base64(binary))
else:
    print "Usage: " + sys.argv[0] + " [raw hex string]"
