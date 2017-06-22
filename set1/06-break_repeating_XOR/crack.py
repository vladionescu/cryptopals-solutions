#!/usr/bin/env python
from __future__ import division
from Utils import Op
import binascii, operator

verbose = False

def main():
    b64_mystery_string = ""
    min_keysize = 2
    max_keysize = 40

    """The file contains ASCII armor: newline separated base64'd binary data
    (the ciphertext). Extract it work directly with the binary."""
    with open('6.txt', 'r') as f:
        for line in f:
            b64_mystery_string += line.strip()

    ciphertext = binascii.a2b_base64(b64_mystery_string)

    if verbose:
        print ciphertext

    """For every possible keysize, find the normalized Hamming distance between
    all pairs of adjacent blocks of keysize length in the ciphertext. The
    smallest disatnce is probably the real key length."""
    possible_keysizes = dict()
    for keysize in xrange(min_keysize, max_keysize+1):
        total_blocks = len(ciphertext) // keysize

        avg_normalized_distance = 0.0

        for index in xrange(total_blocks):
            block0 = ciphertext[index*keysize:(index*keysize)+keysize]
            block1 = ciphertext[(index+1)*keysize:((index+1)*keysize)+keysize]
        
            block_distance = Op.string_hamming_distance(block0, block1)
            block_distance /= keysize

            avg_normalized_distance += block_distance

        avg_normalized_distance /= total_blocks
        possible_keysizes.update({ keysize : avg_normalized_distance })

    possible_keysizes = Op.sort_dict_vals(possible_keysizes)

    if verbose:
        print possible_keysizes

    """The keysize with the smallest Hamming distance is probably the correct
    key length. Try to crack the top 3 most likely keysizes."""
    #for keysize,dist in possible_keysizes[:3]:
    """Actually, just take the top candidate."""
    for keysize in [possible_keysizes[0][0]]:
        """Break the ciphertext into key length sized blocks."""
        blocks = Op.get_chunks(ciphertext, keysize)

        if verbose:
            print blocks

        """Transpose the blocks: make a block that is the first byte of every
        block, and a block that is the second byte of every block, and so
        on."""
        transposed_blocks = [""] * keysize
        for block in blocks:
            for index in xrange(len(block)):
                transposed_blocks[index] += block[index]

        if verbose:
            print transposed_blocks

        """Guess the single character XOR key used for each transposed block.
        Getting this right means getting the full length XOR key character by
        character."""
        key_string = ""
        key_decimal = ""
        for block in transposed_blocks:
            candidates = Op.get_xor_candidates(block)
            key_string += chr(candidates[0].key)
            key_decimal += str(candidates[0].key) + " "

        print "Key size: "+str(keysize)+", Key (decimal): "+key_decimal+", Key: '"+key_string+"'"
        print "Decryption attempt: "+binascii.unhexlify(Op.repeating_xor(ciphertext, key_string))

    return

if __name__ == "__main__":
    main()
