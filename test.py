import unittest
import ctypes
from aes import sub_bytes as python_sub_bytes

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)

rijndael.sub_bytes(block)

result_c = ctypes.string_at(
    rijndael.aes_encrypt_block(plaintext, key), 16
)

result_p = python_sub_bytes(block)

print("c results: ", result_c)
print("python results: ", result_p)