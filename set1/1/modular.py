#!/usr/bin/env python
import sys, binascii
from Utils import Convert 

if len(sys.argv) > 1:
    print Convert.hex_b64(sys.argv[1])
else:
    print "Usage: " + sys.argv[0] + " [raw hex string]"
