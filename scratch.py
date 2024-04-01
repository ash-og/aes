import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix 

rijndael = ctypes.CDLL('./rijndael.so')

buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)


p_matrix = p_bytes2matrix(buffer)
print("Python matrix: ", p_matrix)



# Creating a matrix data structure for c_matrix
CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
c_matrix = CMatrixType()

# Call the bytes2matrix function
rijndael.bytes2matrix(buffer, c_matrix)

# Function to print the C matrix in a human-readable form
def print_c_matrix(matrix):
    for row in matrix:
        print(' '.join(f'{cell}' for cell in row))

# Print the C matrix
print("C matrix:")
print_c_matrix(c_matrix)