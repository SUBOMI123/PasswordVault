from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def encrypt(string):
  salt = b'AppleSauce'
  key = PBKDF2(string, salt, dkLen=32)

  data = string.encode('latin-1')

  cipher_encrypt = AES.new(key, AES.MODE_CFB)
  cipher_bytes = cipher_encrypt.encrypt(data)

  iv = cipher_encrypt.iv
  
  encrypted_password = cipher_bytes

  encrypted_password = encrypted_password.decode('latin-1')
  key = key.decode('latin-1')
  iv = iv.decode('latin-1')

  return key, encrypted_password, iv

def decrypt(key, encrypted_password, iv):
  key = key.encode('latin-1')
  iv = iv.encode('latin-1')
  encrypted_password = encrypted_password.encode('latin-1')
  cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=iv)
  decipher_bytes = cipher_decrypt.decrypt(encrypted_password)

  actual_password = decipher_bytes.decode('utf-8')
  return actual_password

