#!/usr/bin/env python
import binascii
from Utils import Op

plaintext = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

ciphertext_verify = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

key = "ICE"

get_chunk = lambda x,y: [ x[i:i+y] for i in range(0, len(x) ,y) ]

xor = ""

for chunk in get_chunk(plaintext, len(key)):
    xor += Op.xor(binascii.hexlify(chunk), binascii.hexlify(key))

print xor
print xor == ciphertext_verify
