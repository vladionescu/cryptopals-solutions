#!/usr/bin/env python
from __future__ import division
import binascii, operator, sys

class Convert(object):
    @staticmethod
    def hex_b64(hex_string):
        binary = binascii.unhexlify(hex_string)
        return binascii.b2a_base64(binary)

    """Given a string such as 'test' return a list of bytestrings, in this case
    ['01110100', '01100101', '01110011', '01110100']"""
    @staticmethod
    def string_bytelist(string):
        return ['{0:08b}'.format(ord(char), 'b') for char in string]

    """Takes a file containing ASCII armor: newline separated base64'd binary
    data (the ciphertext). Returns the binary string."""
    @staticmethod
    def unascii_armor(filepath):
        b64_string = ""
        with open(filepath, 'r') as f:
            for line in f:
                b64_string += line.strip()

	return binascii.a2b_base64(b64_string)

    """Accepts a string 'foo=bar&baz=qux' and returns an object
    [['foo', 'bar'], ['baz', 'qux']]."""
    @staticmethod
    def str_obj(string):
	obj = []

	items = string.split('&')
        for item in items:
            parts = item.split('=')
            if len(parts) == 2:
                obj.append([ parts[0], parts[1] ])

	return obj

    """Accepts an object [['foo', 'bar'], ['baz', 'qux']] and returns a string
    'foo=bar&baz=qux'."""
    @staticmethod
    def obj_str(objekt):
	string = ""

	first_pair = True
	#for k,v in objekt.iteritems():
        for parts in objekt:
	    if first_pair:
		string += "{}={}".format(parts[0], parts[1])
		first_pair = False
	    else:
		string += "&{}={}".format(parts[0], parts[1])

	return string

class Op(object):
    """Sort a dict by the values instead of the keys"""
    @staticmethod
    def sort_dict_vals(unsorted_dict):
        return sorted(unsorted_dict.items(), key=operator.itemgetter(1))

    @staticmethod
    def xor(hex1, hex2):
        bin1 = binascii.unhexlify(hex1)
        bin2 = binascii.unhexlify(hex2)

        xor = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(bin1, bin2)])

        return binascii.hexlify(xor)

    @staticmethod
    def repeating_xor(plaintext, key_string):
        xor_hex = ""

        for chunk in Op.get_chunks(plaintext, len(key_string)):
            xor_hex += Op.xor(binascii.hexlify(chunk), binascii.hexlify(key_string))

        return xor_hex

    @staticmethod
    def get_chunks(string, chunk_size):
        return [ string[ i : i+chunk_size ] for i in range(0, len(string), chunk_size) ]

    """Calculate the Hamming distance between two strings"""
    @staticmethod
    def string_hamming_distance(string1, string2):
        distance = 0

        for x,y in zip(Convert.string_bytelist(string1), Convert.string_bytelist(string2)):
            distance += Op.bitstring_hamming_distance(x, y)

        return distance

    """Calculate the Hamming distance between two strings of bits
    Ex: x_str = '1010', y_str = '1111', count = 2
    https://stackoverflow.com/a/31007941"""
    @staticmethod
    def bitstring_hamming_distance(x_str, y_str):
        assert len(x_str) == len(y_str)
        x, y = int(x_str, 2), int(y_str, 2)
        count, z = 0, x ^ y
        while z:
            count += 1
            z &= z - 1  # magic!
        return count

    """Calculate the Chi Squared score for a given string to determine how
    closely it resembles an English string based on letter (and space)
    frequency. Lower scores are best, high scores indicate the string is not
    very English-like and may not contain many Latin characters.

    This assumes the plaintext is a clean English string
    
    https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
    """
    @staticmethod
    def score_english_string(string):
        # A-Z and space
        english_freqs = [0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442,
                0.0197881, 0.0158610, 0.0492888, 0.0558094, 0.0009033,
                0.0050529, 0.0331490, 0.0202124, 0.0564513, 0.0596302,
                0.0137645, 0.0008606, 0.0497563, 0.0515760, 0.0729357,
                0.0225134, 0.0082903, 0.0171272, 0.0013692, 0.0145984,
                0.0007836, 0.1918182]

        char_counts = [0] * 27
        counted_chars = 0
        str_length = 0

        for char in string.upper():
            str_length += 1
            index = ord(char) - ord('A')

            # Unprintable and control chars indicate a bad decryption
            if ord(char) >= 128 or ord(char) < 10:
                return 9999.99

            if 0 <= index < 26:
                # Count the capital latin letters
                char_counts[index] += 1
                counted_chars += 1
            elif char == ' ':
                # Count the spaces
                char_counts[26] += 1
                counted_chars += 1
            else:
                # Not a character we're counting
                pass

        # Avoid division by zero, in case none of the chars were ones we care about
        if counted_chars == 0:
            counted_chars = 1

        chi_squared_score = 0
        char_freqs = [None] * 27

        # Calculate the score, lower is better (more congruent with English)
        for i in xrange(len(english_freqs)):
            char_freqs[i] = char_counts[i] / counted_chars
            numerator = char_freqs[i] - english_freqs[i]
            chi_squared_score += (numerator * numerator) / english_freqs[i]

        # Weigh by the number of characters we care about (A-Z and space) in the string
        chi_squared_score = chi_squared_score * (1 / (counted_chars / str_length))

        # 1.0 *probably* means no English letters or spaces were found in the text
        # Return an unreasonably high score to ensure this text is marked bad
        if chi_squared_score == 1.0:
            return 9999.99
        else:
            return chi_squared_score

    """Run through 0-255 (possible keys), XORing the ciphertext with each
    value.
    
    Returns the results as a sorted dict containing each results' freq
    count in the format { plaintext : ChiSquared , ... } with the most
    likely result (lowest ChiSquared score, indicating it is most likely
    English text) first."""
    @staticmethod
    def try_xor_decryptions(ciphertext_string):
        possible_plaintexts = dict()
        
        for key in xrange(256):
            xored_string = "".join([chr(ord(char) ^ key) for char in ciphertext_string])
            freq = Op.score_english_string(xored_string)

            possible_plaintexts.update({ xored_string : freq })

        return Op.sort_dict_vals(possible_plaintexts)

    """Run through 0-255 (possible keys), XORing the ciphertext with each
    value.
    
    Returns the results as a sorted list of Candidate objects with the most
    likely result (lowest ChiSquared score, indicating it is most likely
    English text) first."""
    @staticmethod
    def get_xor_candidates(ciphertext_string):
        candidates = []
        
        for key in xrange(256):
            candidate = Candidate()

            xored_string = "".join([chr(ord(char) ^ key) for char in ciphertext_string])
            freq = Op.score_english_string(xored_string)

            candidate.original = ciphertext_string
            candidate.result = xored_string
            candidate.score = freq
            candidate.key = key

            candidates.append(candidate)

        return Candidate.sort(candidates)

    """PKCS#7 padding works by padding a block of input with the hexadecimal
    number representing how many bytes of padding need to be added in order to
    make the block complete.

    Accepts either a string or a list of blocks (from Op.get_chunks() for
    example).

    Returns a list of binary blocks.

    Ex. For a block size of 8, padding 'testing' results in 'testing\x01'
    because one byte was needed to make the block 8 bytes long. Padding 'test'
    results in 'test\x04\x04\x04\x04' because four padding bytes were
    needed."""
    @staticmethod
    def pkcs7(input_object, block_size):
        if isinstance(input_object, basestring):
            blocks = Op.get_chunks(input_object, block_size)
        elif isinstance(input_object, list):
            blocks = input_object
        else:
            """No proper error handling, that's a deep rabbit hole."""
            return None
        
        """Last block is the only one that may not be the full block size."""
        padding_size = block_size - len(blocks[-1])

        if padding_size > 0:
            blocks[-1] += chr(padding_size) * padding_size
        
        return blocks

    """Returns a string."""
    @staticmethod
    def pkcs7_string(input_object, block_size):
        blocks = Op.pkcs7(input_object, block_size)
        return "".join(blocks)

    """Remove PKCS#7 padding from a given list of blocks or a string.
    If the input is PKCS#7 padded, return a list of unpadded blocks.
    If no PKCS#7 padding is detected, return the input unmodified."""
    @staticmethod
    def unpkcs7(input_object, block_size):
        if isinstance(input_object, basestring):
            blocks = Op.get_chunks(input_object, block_size)
        elif isinstance(input_object, list):
            blocks = input_object
        else:
            """No proper error handling, that's a deep rabbit hole."""
            return None
        
        """Last block is the only one that will contain padding."""
        padded_block = blocks[-1]

        """Last byte of last block will be the padding value."""
        padding_value = padded_block[-1]

        """Remove the suspected padding bytes and verify they are PKCS#7
        padding."""
        padding = padded_block[-ord(padding_value):]

        for char in padding:
            if char != padding_value:
                """If any bytes of the supposed padding is not the value of the
                number of padded bytes, this is not PKCS#7."""
                return blocks
        
        """Return the input blocks minus the padding in the last block."""
        return blocks[:-1] + [ blocks[-1:][0][:-ord(padding_value)] ]

    """Returns a string."""
    @staticmethod
    def unpkcs7_string(input_object, block_size):
        blocks = Op.unpkcs7(input_object, block_size)
        return "".join(blocks)

    """Check whether there are any duplicate blocks in the ciphertext binary by
    seeing if the number of unique blocks is the same as the number of total
    blocks for that ciphertext."""
    @staticmethod
    def is_ecb_mode(binary, block_size=16):
        blocks = Op.get_chunks(binary, block_size)

        if len(set(blocks)) != len(blocks):
            return True

        return False

    """For every possible keysize, find the normalized Hamming distance between
    all pairs of adjacent blocks of keysize length in the ciphertext. The
    smallest disatnce is probably the real key length."""
    @staticmethod
    def guess_keysizes(ciphertext):
	min_keysize = 2
	max_keysize = 40
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
        return possible_keysizes

class Candidate(object):
    original = ""
    result = ""
    score = -0.0
    key = -1

    """Sort a list of Candidates by their score."""
    @staticmethod
    def sort(unsorted_list):
        return sorted(unsorted_list, key=lambda x: x.score)

if __name__ == "__main__":
    print "This is a module."

