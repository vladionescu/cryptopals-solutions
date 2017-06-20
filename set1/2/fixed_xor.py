#!/usr/bin/env python
import binascii

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"

bin1 = binascii.unhexlify(hex1)
bin2 = binascii.unhexlify(hex2)

xor = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(bin1, bin2)])

print binascii.hexlify(xor)
