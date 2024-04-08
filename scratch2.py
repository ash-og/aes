import ctypes
import secrets
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, shift_rows as p_shift_rows, AES # importing python subbytes

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)

rijndael.aes_encrypt_block.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ubyte)]
rijndael.aes_encrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)

key = secrets.token_bytes(16)
c_key = (ctypes.c_ubyte * len(key))(*key)

c_encrypted_ptr = rijndael.aes_encrypt_block(buffer, c_key)
c_encrypted = ctypes.string_at(c_encrypted_ptr, 16)

rijndael.free_memory(c_encrypted_ptr)

p_AES = AES(key)
p_encrypted = p_AES.encrypt_block(bytes(buffer))

print("C encrypted:", c_encrypted)
print("Python encrypted:", p_encrypted)
print(c_encrypted==p_encrypted)
