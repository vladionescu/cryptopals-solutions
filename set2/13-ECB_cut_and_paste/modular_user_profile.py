#!/usr/bin/env python
from Utils import Convert

def main():
    str1 = "foo=bar&baz=qux&zap=zazzle"
    str2 = "email=foo@bar.com&uid=10&role=user"
    obj1 = Convert.str_obj(str1)
    obj2 = Convert.str_obj(str2)

    print "[+] String -> Object"
    print obj1
    print obj2
    print "[+] Object -> String"
    print Convert.obj_str(obj1)
    print Convert.obj_str(obj2)

if __name__ == "__main__":
    main()
