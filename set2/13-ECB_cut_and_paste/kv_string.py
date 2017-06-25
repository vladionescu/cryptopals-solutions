#!/usr/bin/env python

"""Accepts a string 'foo=bar&baz=qux' and returns an object
{'foo':'bar', 'baz':'qux'}."""
def str_obj(string):
    obj = dict()

    items = string.split('&')
    for item in items:
        obj.update([tuple(item.split('='))])

    return obj

"""Accepts an object {'foo':'bar', 'baz':'qux'} and returns a string
'foo=bar&baz=qux'."""
def obj_str(objekt):
    string = ""

    first_pair = True
    for k,v in objekt.iteritems():
        if first_pair:
            string += "{}={}".format(k,v)
            first_pair = False
        else:
            string += "&{}={}".format(k,v)

    return string

def main():
    str1 = "foo=bar&baz=qux&zap=zazzle"
    str2 = "email=foo@bar.com&uid=10&role=user"
    obj1 = str_obj(str1)
    obj2 = str_obj(str2)

    print "[+] String -> Object"
    print obj1
    print obj2
    print "[+] Object -> String"
    print obj_str(obj1)
    print obj_str(obj2)

if __name__ == "__main__":
    main()
