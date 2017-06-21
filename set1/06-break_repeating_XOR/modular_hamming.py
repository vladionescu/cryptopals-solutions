#!/usr/bin/env python
from Utils import Op

string1 = "this is a test"
string2 = "wokka wokka!!!"
distance_verify = 37

def main():
    distance = Op.string_hamming_distance(string1, string2)

    print distance
    print distance == distance_verify

if __name__ == "__main__":
    main()
