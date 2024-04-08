import unittest
import ctypes
import os
import secrets
from aes.aes import bytes2matrix as p_bytes2matrix, matrix2bytes as p_matrix2bytes, sub_bytes as p_sub_bytes, shift_rows as p_shift_rows, mix_columns as p_mix_columns, inv_sub_bytes as p_inv_sub_bytes, inv_shift_rows as p_inv_shift_rows, inv_mix_columns as p_inv_mix_columns, add_round_key as p_add_round_key, AES



class TestAes(unittest.TestCase):
    def setUp(self):
        # Load the shared library
        self.rijndael = ctypes.CDLL('./rijndael.so')
        # prepare they keys
        self.keys = [secrets.token_bytes(16) for i in range(3)]
        # self.buffers = [os.urandom(16) for i in range(3)] 
        # self.blocks = [ctypes.create_string_buffer(buffer) for buffer in self.buffers]

        # Prepare the inputs
    def generate_inputs(self):
        """Generate 3 random inputs for testing."""
        return [os.urandom(16) for i in range(3)]
    
    def create_matrices(self, buffer):
        """Convert a buffer to a 4x4 matrix."""
        block = ctypes.create_string_buffer(buffer)
        CMatrixType = (ctypes.c_ubyte * 4) * 4
        c_matrix = CMatrixType()

        # Call the bytes2matrix function
        p_matrix = p_bytes2matrix(buffer)
        self.rijndael.bytes2matrix(block, c_matrix)
        return c_matrix, p_matrix

    def test_bytes2matrix(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrix data structure for c_matrix
                #print(buffer)
                block = ctypes.create_string_buffer(buffer)
                CMatrixType = (ctypes.c_ubyte * 4) * 4
                c_matrix = CMatrixType()

                # Call the bytes2matrix function
                p_matrix = p_bytes2matrix(buffer)
                self.rijndael.bytes2matrix(block, c_matrix)

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
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                # Call the C sub_bytes function
                self.rijndael.sub_bytes(c_matrix)
                p_sub_bytes(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))

    def test_shift_rows(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                # Call the C shift_rows function
                self.rijndael.shift_rows(c_matrix)
                p_shift_rows(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))

    def test_mix_columns(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                # Call the C shift_rows function
                self.rijndael.mix_columns(c_matrix)
                p_mix_columns(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))

    def test_expand_add_round_keys(self):
        for key in self.keys:
            with self.subTest(key=key):
                # Define the argument and return types for the expand_key function
                self.rijndael.expand_key.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
                self.rijndael.expand_key.restype = ctypes.POINTER(ctypes.c_ubyte)

                c_key = (ctypes.c_ubyte * len(key))(*key)
                expanded_key = self.rijndael.expand_key(c_key)

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
                
                python_expanded_key_bytes = matrices2bytes(p_expanded_key_matrices)
                self.assertEqual(ctypes.string_at(expanded_key, 176), python_expanded_key_bytes)

                buffer = b'\x00\x01\x02\x03\x04\x05\x06\x07'
                buffer += b'\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
                c_matrix, p_matrix = self.create_matrices(buffer)
                self.rijndael.add_round_key(c_matrix, expanded_key)
                p_add_round_key(p_matrix, p_expanded_key_matrices[0])
                
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))
                self.rijndael.free_memory(expanded_key)

    def test_invert_subbytes(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                self.rijndael.sub_bytes(c_matrix)
                self.rijndael.invert_sub_bytes(c_matrix)
                p_sub_bytes(p_matrix)
                p_inv_sub_bytes(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))

    def test_invert_shiftrows(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                self.rijndael.shift_rows(c_matrix)
                self.rijndael.invert_shift_rows(c_matrix)
                p_shift_rows(p_matrix)
                p_inv_shift_rows(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))

    def test_invert_mixcolumns(self):
        for buffer in self.generate_inputs():
            with self.subTest(buffer=buffer):
                # Creating a matrices for c_matrix, p_matrix
                c_matrix, p_matrix = self.create_matrices(buffer)

                self.rijndael.mix_columns(c_matrix)
                self.rijndael.invert_mix_columns(c_matrix)
                p_mix_columns(p_matrix)
                p_inv_mix_columns(p_matrix)
                self.assertEqual(ctypes.string_at(c_matrix,16), p_matrix2bytes(p_matrix))
    def test_encryption_decryption(self):
        for key in self.keys:
            for buffer in self.generate_inputs():
                with self.subTest(buffer=buffer):
                    self.rijndael.aes_encrypt_block.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ubyte)]
                    self.rijndael.aes_encrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)
                    c_key = (ctypes.c_ubyte * len(key))(*key)
                    c_encrypted_ptr = self.rijndael.aes_encrypt_block(buffer, c_key)
                    c_encrypted = ctypes.string_at(c_encrypted_ptr, 16)
                    self.rijndael.free_memory(c_encrypted_ptr)
                    p_AES = AES(key)
                    p_encrypted = p_AES.encrypt_block(bytes(buffer))
                    self.assertEqual(c_encrypted, p_encrypted)

                    self.rijndael.aes_decrypt_block.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
                    self.rijndael.aes_decrypt_block.restype = ctypes.POINTER(ctypes.c_ubyte)
                    ciphertext = (ctypes.c_ubyte * 16)(*c_encrypted)
                    c_decrypted_ptr = self.rijndael.aes_decrypt_block(ciphertext, c_key)
                    c_decrypted = ctypes.string_at(c_decrypted_ptr, 16)
                    self.rijndael.free_memory(c_decrypted_ptr)
                    p_decrypted = p_AES.decrypt_block(p_encrypted)
                    self.assertEqual(c_decrypted, p_decrypted)

if __name__ == "__main__":
    unittest.main()