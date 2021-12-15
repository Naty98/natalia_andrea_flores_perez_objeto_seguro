from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def __generate_keys():
    modulus_length = 1024

    __key = RSA.generate(modulus_length)
    #print (key.exportKey())

    pub_key = __key.publickey()
    #print (pub_key.exportKey())

    return __key, pub_key

def encrypt_private_key(a_message, __private_key):
    a_message = str.encode(a_message)
    encryptor = PKCS1_OAEP.new(__private_key)
    encrypted_msg = encryptor.encrypt(a_message)
    #print(encrypted_msg)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    #print(encoded_encrypted_msg)
    return encoded_encrypted_msg

def decrypt_public_key(encoded_encrypted_msg, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    #print(decoded_encrypted_msg)
    decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
    #print(decoded_decrypted_msg)
    #return decoded_decrypted_msg

