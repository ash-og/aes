import ctypes
from aes.aes import bytes2matrix, matrix2bytes, sub_bytes as python_sub_bytes # importing python subbytes

# Load the shared library
rijndael = ctypes.CDLL('./rijndael.so')


# Prepare the input buffer
buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
block = ctypes.create_string_buffer(buffer)

# Call the C sub_bytes function
rijndael.sub_bytes(block)


# Prepare the same input for the Python implementation
p_block = bytes2matrix(buffer)
# result_p = python_sub_bytes(bytes(p_block))
python_sub_bytes(p_block)
# Prepare the output for comparison
p_result = matrix2bytes(p_block)

print("C results: ", ctypes.string_at(block,16))
print("Python results: ", p_result)
