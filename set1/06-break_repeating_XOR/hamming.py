#!/usr/bin/env python

string1 = "this is a test"
string2 = "wokka wokka!!!"
distance_verify = 37

def main():
    byte_list = lambda string: ['{0:08b}'.format(ord(char), 'b') for char in string]

    distance = 0

    for x,y in zip(byte_list(string1), byte_list(string2)):
        distance += hamming(x, y)

    print distance
    print distance == distance_verify

# https://stackoverflow.com/a/31007941
def hamming(x_str, y_str):
    """Calculate the Hamming distance between two strings of bits"""
    assert len(x_str) == len(y_str)
    x, y = int(x_str, 2), int(y_str, 2)
    count, z = 0, x ^ y
    while z:
        count += 1
        z &= z - 1  # magic!
    return count

if __name__ == "__main__":
    main()
