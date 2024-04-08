import ctypes
import secrets
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, AES

rijndael = ctypes.CDLL('./rijndael.so')

key = secrets.token_bytes(16)
c_key = (ctypes.c_ubyte * len(key))(*key)

# Define the argument and return types for the expand_key function
rijndael.expand_key.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.expand_key.restype = ctypes.POINTER(ctypes.c_ubyte)

expanded_key = rijndael.expand_key(c_key)
print("C results: ", ctypes.string_at(expanded_key, 176))

p_AES = AES(key)
p_expanded_key_matrices = p_AES._key_matrices

def matrices2bytes(matrices):
    """ Converts a list of 4x4 matrices into a concatenated byte array. """
    # Flatten each matrix to a single list of bytes, then concatenate
    flattened_array = []
    for matrix in matrices:
        for row in matrix:
            flattened_array.extend(row)
    return bytes(flattened_array)

# print("Python results: ", p_expanded_key_matrices)
python_expanded_key_bytes = matrices2bytes(p_expanded_key_matrices)

print("Python results: ", python_expanded_key_bytes)

print(ctypes.string_at(expanded_key, 176)==python_expanded_key_bytes)

rijndael.free_memory(expanded_key)