#!/usr/bin/env python
import binascii
from Utils import Op, Convert
from Crypto.Cipher import AES

def main():
    key = "YELLOW SUBMARINE"
    IV = "\x00" * 16

    ciphertext = Convert.unascii_armor('10.txt')

    """AES-ECB always has a 16 byte block size."""
    block_size = 16
    aes = AES.new(key, AES.MODE_ECB)

    """Get PKCS#7 padded blocks from the ciphertext (not necessary because
    ciphertext, assuming it was produced with a true AES-CBC function, will be
    a multiple of blocks long, but it's safer this way). For each block of
    ciphertext, decrypt it via AES-ECB then take the decrypted result and XOR
    it with the previous block (or the IV if this is the first block we're
    decrypting) to get the plaintext.

    Ref: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29
    """
    plaintext = ""

    blocks = Op.get_chunks(ciphertext, block_size)
    blocks = Op.pkcs7(blocks, block_size)

    for index in xrange(len(blocks)):
        intermediate = aes.decrypt(blocks[index])

        if index == 0:
            plaintext_hex = Op.xor( binascii.hexlify(IV),
                    binascii.hexlify(intermediate) )
        else:
            plaintext_hex = Op.xor( binascii.hexlify( blocks[index-1] ),
                    binascii.hexlify(intermediate) )

        plaintext += binascii.unhexlify(plaintext_hex)

    print plaintext

if __name__ == "__main__":
    main()
