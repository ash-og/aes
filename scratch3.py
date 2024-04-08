import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, shift_rows as p_shift_rows # importing python subbytes

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)


print("Before:", buffer)

CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()


p_matrix = p_bytes2matrix(buffer)
rijndael.bytes2matrix(block, c_matrix)

def print_c_matrix(matrix):
    for row in matrix:
        print(' '.join(f'{cell:02X}' for cell in row))

print("C matrix after bytes2matrix:")
print_c_matrix(c_matrix)

# new_block = ""
# rijndael.matrix2bytes(c_matrix, new_block)

# print("C matrix after matrix2bytes:")
# print(ctypes.string_at(new_block, 16))

# print("Python matrix after matrix2bytes:")
# print(p_new_block)

p_new_block = matrix2bytes(p_matrix)


# Allocate a buffer for the output of matrix2bytes
new_block = (ctypes.c_ubyte * 16)()  # This creates an array of 16 unsigned bytes

# Call matrix2bytes with the correct arguments
rijndael.matrix2bytes(c_matrix, new_block)

# Convert the resulting C array back to a Python bytes object for comparison
new_block_bytes = bytes(new_block)

print("C matrix after matrix2bytes:")
print(new_block_bytes)

print("Python matrix after matrix2bytes:")
print(p_new_block)