import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes as p_matrix2bytes, sub_bytes as p_sub_bytes, shift_rows as p_shift_rows, mix_columns as p_mix_columns, inv_sub_bytes as p_inv_sub_bytes, inv_shift_rows as p_inv_shift_rows, inv_mix_columns as p_inv_mix_columns, add_round_key as p_add_round_key, AES

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)


print("Before:", buffer)

CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()


p_matrix = p_bytes2matrix(buffer)
rijndael.bytes2matrix(block, c_matrix)

rijndael.mix_columns(c_matrix)
p_mix_columns(p_matrix)
print("C matrix:", ctypes.string_at(c_matrix, 16))
print("Python matrix:", p_matrix2bytes(p_matrix))
print(ctypes.string_at(c_matrix, 16)==p_matrix2bytes(p_matrix))
rijndael.invert_mix_columns(c_matrix)
p_inv_mix_columns(p_matrix)
print("C matrix:", ctypes.string_at(c_matrix, 16))
print("Python matrix:", p_matrix2bytes(p_matrix))
print(ctypes.string_at(c_matrix, 16)==p_matrix2bytes(p_matrix))
