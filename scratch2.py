import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, shift_rows as p_shift_rows # importing python subbytes

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)

CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()

p_matrix = p_bytes2matrix(buffer)
rijndael.bytes2matrix(block, c_matrix)

def print_c_matrix(matrix):
    for row in matrix:
        print(' '.join(f'{cell:02X}' for cell in row))

print("C matrix before shift_rows:")
print_c_matrix(c_matrix)

rijndael.shift_rows(c_matrix)

print("C matrix after shift_rows:")
print_c_matrix(c_matrix)
