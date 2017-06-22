#!/usr/bin/env python
import binascii
from Utils import Op

def main():
    ciphertexts = []
    block_size = 16

    """The file contains hex-encoded ciphertexts, one of which is AES ECB.
    Extract them and work directly with the binary."""
    with open('8.txt', 'r') as f:
        for line in f:
            ciphertexts.append( binascii.unhexlify( line.strip() ) )

    """For each ciphertext, split it into 16 byte blocks, and check whether
    there are any duplicate blocks in the ciphertext by seeing if the number of
    unique blocks is the same as the number of total blocks for that
    ciphertext."""
    for ciphertext in ciphertexts:
        blocks = Op.get_chunks(ciphertext, block_size)

        if len(set(blocks)) != len(blocks):
            print "[+] Possible ECB:\n" + binascii.hexlify(ciphertext)
            print "[+] ASCII Blocks:"

            for block in blocks:
                print block

            print "[---]"

if __name__ == "__main__":
    main()
