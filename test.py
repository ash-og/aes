import unittest
import ctypes
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes, sub_bytes as p_sub_bytes # importing python subbytes



class TestAes(unittest.TestCase):
    def setUp(self):
        # Load the shared library
        self.rijndael = ctypes.CDLL('./rijndael.so')
                # Prepare the input buffer
        self.buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
        self.buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        self.block = ctypes.create_string_buffer(self.buffer)

    def test_bytes2matrix(self):
        # Creating a matrix data structure for c_matrix
        CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
        c_matrix = CMatrixType()

        # Call the bytes2matrix function
        p_matrix = p_bytes2matrix(self.buffer)
        self.rijndael.bytes2matrix(self.block, c_matrix)

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
        self.assertEqual(p_matrix_string, c_matrix_string)

    def test_sub_bytes(self):
        # Creating a matrix data structure for c_matrix
        CMatrixType = (ctypes.c_ubyte * 4) * 4  # Defines a 4x4 matrix of unsigned bytes
        c_matrix = CMatrixType()

        p_matrix = p_bytes2matrix(self.buffer)
        self.rijndael.bytes2matrix(self.block, c_matrix)

        # Call the C sub_bytes function
        self.rijndael.sub_bytes(c_matrix)
        p_sub_bytes(p_matrix)
        self.assertEqual(ctypes.string_at(c_matrix,16), matrix2bytes(p_matrix))


if __name__ == "__main__":
    unittest.main()