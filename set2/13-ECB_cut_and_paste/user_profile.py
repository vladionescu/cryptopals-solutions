#!/usr/bin/env python
import binascii, os
from Crypto.Cipher import AES
from Utils import Convert, Op

key = os.urandom(16)

def profile_for(email):
    sanitized_email = email.replace('&', '').replace('=', '')
    profile_string = "email={}&uid=10&role=user".format(sanitized_email)
    return Convert.str_obj(profile_string)

def encrypt_profile(key, profile):
    aes = AES.new(key, AES.MODE_ECB)
    profile_string = Convert.obj_str(profile)
    to_encrypt = Op.pkcs7_string(profile_string, 16)
    return aes.encrypt(to_encrypt)

def decrypt_profile(key, cipher_hex):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = aes.decrypt(cipher_hex)
    plaintext = Op.unpkcs7_string(decrypted, 16)
    return plaintext

def main():
    """Create a normal profile and return the ciphertext the attacker would
    get."""
    profile = profile_for("foo@bar.com")
    encrypted_profile = encrypt_profile(key, profile)
    decrypted_profile = decrypt_profile(key, encrypted_profile)

    """Attempt to create a mangled ciphertext which decrypts to represent an
    admin user (the decrypted string should end with &role=admin). Try to
    achieve this by crafting a block which starts with &role=admin then make
    that the last block."""
    for fill in xrange(30):
        """Extend the email address until we reach a block boundary and the
        ciphertext gets longer, then we know we are at the beginning of a new
        block and can:
            1. Extend the email by enough bytes (4) to put the value we want to
            change in the last block. In this case the last block should
            contain 'user<padding>'.
            2. Drop the admin string at the beginning of a block we control, so
            put it at the end of the email address ending on a block
            boundary."""
        try_profile = profile_for("foo" + ('A' * fill) + "@bar.com")
        encrypted_try_profile = encrypt_profile(key, try_profile)

        """When the number of bytes needed to start a new block is found."""
        if len(encrypted_profile) < len(encrypted_try_profile):
            """1."""
            role_on_block_boundary_profile = profile_for("foo" + ('A' *
                (fill + 3)) + "@bar.com")
            encrypted_role_profile = encrypt_profile(key, role_on_block_boundary_profile)

            """2."""
            admin_at_start_of_block_profile = profile_for("foo" + ('A' * fill)
                    + "@bar.com" + "admin")
            encrypted_admin_profile = encrypt_profile(key, admin_at_start_of_block_profile)

            """Craft the ciphertext which will decrypt to an admin profile."""
            mangled_profile = encrypted_role_profile[:-(16*1)] + encrypted_admin_profile[16*2:16*3]
            mangled_admin_profile = decrypt_profile(key, mangled_profile)
            break

    print "[+] foo@bar.com's Profile"
    print profile
    print "[+] Encoded Profile"
    print Convert.obj_str(profile)
    print "[+] Encrypted Profile"
    print binascii.hexlify(encrypted_profile)
    print "[+] Decrypted Profile"
    print decrypted_profile
    print "---"
    print "[+] Mangled Admin Profile Encoded"
    print mangled_admin_profile
    print "[+] Mangled Admin Profile"
    print Convert.str_obj(mangled_admin_profile)
    print "[+] Encrypted Mangled Admin Profile"
    print binascii.hexlify(mangled_profile)


if __name__ == "__main__":
    main()
