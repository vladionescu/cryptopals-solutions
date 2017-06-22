#!/usr/bin/env python
import binascii
from Utils import Op

def main():
    """PKCS#7 padding works by padding a block of input with the hexadecimal
    number representing how many bytes of padding need to be added in order to
    make the block complete.

    Ex. For a block size of 8, padding 'testing' results in 'testing\x01'
    because one byte was needed to make the block 8 bytes long. Padding 'test'
    results in 'test\x04\x04\x04\x04' because four padding bytes were
    needed."""
    string = "YELLOW SUBMARINE"
    block_size = 20

    blocks = Op.pkcs7(string, block_size)
    
    print "[+] Input: " + string
    print "[+] Block size: " + str(block_size)
    print "[+] Padded blocks: " + str(blocks)

if __name__ == "__main__":
    main()
