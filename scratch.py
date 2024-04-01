import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix 

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)


p_matrix = p_bytes2matrix(buffer)

# Creating a matrix data structure for c_matrix
CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()

# Call the bytes2matrix function
rijndael.bytes2matrix(block, c_matrix)

# Function to make a string of p_ and C_matrix to allow for comparison
def create_mx_str(matrix):
    matrix_string = ''
    for row in matrix:
        for cell in row:
            matrix_string += ' '.join(f', {cell}')
    return matrix_string

# Compare matrices
p_matrix_string = create_mx_str(p_matrix)
c_matrix_string = create_mx_str(c_matrix)
print(p_matrix_string == c_matrix_string)