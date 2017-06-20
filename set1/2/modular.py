#!/usr/bin/env python
from Utils import Op 

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"

print Op.xor(hex1, hex2)
