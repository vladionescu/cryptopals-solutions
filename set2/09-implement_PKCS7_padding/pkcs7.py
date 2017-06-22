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

    blocks = Op.get_chunks(string, block_size)
    
    """The last block is the only one that may not be the full block size."""
    padding_size = block_size - len(blocks[-1])

    if padding_size > 0:
        blocks[-1] += chr(padding_size) * padding_size
    
    print "[+] Input: " + string
    print "[+] Block size: " + str(block_size)
    print "[+] Padded blocks: " + str(blocks)

if __name__ == "__main__":
    main()
