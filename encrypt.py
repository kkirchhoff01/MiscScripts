from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as po
from base64 import b64decode

def generate_keys(keysize=1024):
    rand_gen = Random.new().read
    key = RSA.generate(1024, rand_gen)

    public_key = key.publickey()
    private_key = key.exportKey()
    return public_key, private_key

def encrypt_message(message, public_key):
    rsa_key = po.new(public_key)
    encrypted_message = rsa_key.encrypt(message)
    return encrypted_message.encode('base64')

def decrypt_message(encrypted_message, private_key):
    rsa_key = RSA.importKey(private_key)
    rsa_key = po.new(rsa_key)
    decrypted_message = rsa_key.decrypt(b64decode(encrypted_message))
    return decrypted_message

if __name__ == "__main__":
    import sys
    msg = sys.argv[1]
    public_key, private_key = generate_keys()
    message = encrypt_message(msg, public_key)
    print 'The public key is: ' + str(public_key.n)
    print decrypt_message(message, private_key)
