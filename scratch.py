import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, sub_bytes as p_subbytes, shift_rows as p_shift_rows, mix_columns as p_mix_columns # importing python subbytes

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)

CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()

p_matrix = p_bytes2matrix(buffer)
rijndael.bytes2matrix(block, c_matrix)

temp = c_matrix
print(ctypes.string_at(temp,16))
# Call the C sub_bytes function
rijndael.sub_bytes(c_matrix)
print(ctypes.string_at(temp,16))
rijndael.invert_sub_bytes(c_matrix)

print("C results: ", ctypes.string_at(c_matrix,16))

print(ctypes.string_at(c_matrix,16)==ctypes.string_at(temp,16))

