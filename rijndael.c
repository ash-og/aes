/*
 * Aisling Young - D21127518
 * This code implements AES-128 encryption and decryption algorithms.
 * It includes the following functions:
 * - bytes2matrix: Converts a 16-byte block into a 4x4 matrix
 * - matrix2bytes: Converts a 4x4 matrix into a 16-byte block
 * - sub_bytes: Replaces each byte in the state with another one using the Rijndael S Box
 * - shift_rows: Shifts the rows of the state to the left
 * - xtime: Multiplies a byte by 2, and XORs it with 0x1B if the most significant bit of the byte is 1
 * - mix_single_column: Multiplies a column by 2, 3, 1, 1
 * - mix_columns: A linear transformation of the columns of the state
 * - invert_sub_bytes: Replaces each byte in the state with another one using the inverted Rijndael S Box
 * - invert_shift_rows: Shifts the rows of the state to the right
 * - invert_mix_columns: A linear transformation of the columns of the state
 * - add_round_key: Combines each byte of the state with a round key
 * - free_memory: Frees the memory allocated for the key
 * - expand_key: Expands the given 128-bit cipher key and returns a 176-byte list of 11 round keys
 * - aes_encrypt_block: Encrypts a single block of plaintext using the given key
 * - aes_decrypt_block: Decrypts a single block of ciphertext using the given key * 
 */

#include <stdint.h>
#include <stdlib.h>
#include <string.h> 
#include "rijndael.h"

/* aes sbox and invert-sbox */
static const unsigned char s_box[] = {
/*  0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F  */
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
};

static const unsigned char inv_s_box[] = {
/*  0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F  */
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
};

/* aes rcon box for key expansion */
static const unsigned char r_con[] = {
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
};

void bytes2matrix(unsigned char *block, unsigned char matrix[4][4]) {
    // Convert a 16-byte block into a 4x4 matrix
    for (int i = 0; i < 16; ++i) {
        matrix[i / 4][i % 4] = block[i];
    }
}

void matrix2bytes(unsigned char matrix[4][4], unsigned char* block) {
    // Convert a 4x4 matrix into a 16-byte block
    int index = 0;
    for (int row = 0; row < 4; ++row) {
        for (int col = 0; col < 4; ++col) {
            block[index++] = matrix[row][col];
        }
    }
}

void sub_bytes(unsigned char matrix[4][4]) {
  // Every byte in the state is replaced by another one, using the Rijndael S Box
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            matrix[i][j] = s_box[matrix[i][j]]; // Substitute each byte using the S-box
        }
    }
}

void shift_rows(unsigned char matrix[4][4]) {
    // Shift the rows of the state to the left
    unsigned char temp;
    
    // Row 1: left shift by 1
    // s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]  
    temp = matrix[0][1];
    matrix[0][1] = matrix[1][1];
    matrix[1][1] = matrix[2][1];
    matrix[2][1] = matrix[3][1];
    matrix[3][1] = temp;

    // Row 2: left shift by 2
    // s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    temp = matrix[0][2];
    matrix[0][2] = matrix[2][2];
    matrix[2][2] = temp;
    temp = matrix[1][2];
    matrix[1][2] = matrix[3][2];
    matrix[3][2] = temp;

    // Row 3: left shift by 3 (or right shift by 1)
    // s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
    temp = matrix[0][3];
    matrix[0][3] = matrix[3][3];
    matrix[3][3] = matrix[2][3];
    matrix[2][3] = matrix[1][3];
    matrix[1][3] = temp;
}

unsigned char xtime(unsigned char a) {
  // Create a new byte that is a left shifted version of the input byte, and then XOR it with 0x1B if the most significant bit of the input byte is 1. Otherwise, just return the left shifted version of the input byte.
    return (a & 0x80)?((a << 1) ^ 0x1B) & 0xFF:(a << 1); 
}

void mix_single_column(unsigned char *column) {
  // Uses xtime to multiply the column by 2, 3, 1, 1
    unsigned char t = column[0] ^ column[1] ^ column[2] ^ column[3];
    unsigned char u = column[0];
    column[0] ^= t ^ xtime(column[0] ^ column[1]);
    column[1] ^= t ^ xtime(column[1] ^ column[2]);
    column[2] ^= t ^ xtime(column[2] ^ column[3]);
    column[3] ^= t ^ xtime(column[3] ^ u);
}


void mix_columns(unsigned char matrix[4][4]) {
  // A linear transformation of the columns of state
    for (int i = 0; i < 4; ++i) {
        mix_single_column(matrix[i]);
    }
}

/*
 * Operations used when decrypting a block
 */
void invert_sub_bytes(unsigned char matrix[4][4]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            matrix[i][j] = inv_s_box[matrix[i][j]]; // Substitute each byte using the inverted S-box
        }
    }
}

void invert_shift_rows(unsigned char matrix[4][4]) {

    unsigned char temp;

    // Row 1: right shift by 1 
    //  s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    temp = matrix[3][1];
    matrix[3][1] = matrix[2][1];
    matrix[2][1] = matrix[1][1];
    matrix[1][1] = matrix[0][1];
    matrix[0][1] = temp;

    // Row 2: right shift by 2 
    // s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    temp = matrix[0][2];
    matrix[0][2] = matrix[2][2];
    matrix[2][2] = temp;
    temp = matrix[1][2];
    matrix[1][2] = matrix[3][2];
    matrix[3][2] = temp;

    // Row 3: right shift by 3 
    // s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
    temp = matrix[1][3];
    matrix[1][3] = matrix[2][3];
    matrix[2][3] = matrix[3][3];
    matrix[3][3] = matrix[0][3];
    matrix[0][3] = temp;
}

void invert_mix_columns(unsigned char matrix[4][4]) {
  // A linear transformation of the columns of state
    for (int i = 0; i < 4; ++i) {
        unsigned char u = xtime(xtime(matrix[i][0] ^ matrix[i][2]));
        unsigned char v = xtime(xtime(matrix[i][1] ^ matrix[i][3]));
        matrix[i][0] ^= u;
        matrix[i][1] ^= v;
        matrix[i][2] ^= u;
        matrix[i][3] ^= v;
    }
    mix_columns(matrix);

}


/*
 * This operation is shared between encryption and decryption
 */
void add_round_key(unsigned char matrix[4][4], unsigned char *round_key) {
  // Each byte of the state is combined with a round key, which is a different key for each round and derived from the Rijndael key schedule
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            matrix[i][j] ^= round_key[i * 4 + j];
        }
    }
}


void free_memory(unsigned char *key) {
  // Free the memory allocated for the key
  free(key);
}

unsigned char *expand_key(unsigned char *cipher_key) {

    // Expands the given 128-bit cipher_key and returns a 176-byte list of 11 round keys .
    
    // Allocating the 176 bytes required for the AES-128 expanded key.
    unsigned char *expandedKey =
        (unsigned char *)malloc(sizeof(unsigned char) * KEY_EXP_SIZE);

    // Copying the current cipher key to the first 16 bytes of the expanded key.
    memcpy(expandedKey, cipher_key, 16);

    int current_size = 16;
    unsigned char word[4]; 
    int r_con_i = 1;
    int key_len = 16;

    while (current_size < KEY_EXP_SIZE) { 
        // While the current size of the expanded key is less than 176 bytes do the following:
        // Assign the last 4 bytes of the expanded key to the word variable.
        memcpy(word, &expandedKey[current_size - 4], 4);

        // if the current column is the last one, perform schedule_core
        if (current_size % key_len == 0) {
            // Perform schedule_core (circular shift, s-box sub_bytes, rcon)
            unsigned char t = word[0];
            word[0] = word[1];
            word[1] = word[2];
            word[2] = word[3];
            word[3] = t;

            for (int i = 0; i < 4; i++) {
                word[i] = s_box[word[i]];
            }

            word[0] ^= r_con[r_con_i++];
        }
        // xor word with the word 16 bytes before it
        for (unsigned int i = 0; i < 4; i++) {
            expandedKey[current_size] = expandedKey[current_size - key_len] ^ word[i];
            current_size++;
        }
    }
        return expandedKey;
}


unsigned char *aes_encrypt_block(unsigned char *plaintext, unsigned char *key) {
  // Encrypts a single block of plaintext using the given key

    // Allocating the 16 bytes required for the output.
    unsigned char *output =
        (unsigned char *)malloc(sizeof(unsigned char) * BLOCK_SIZE);

    // Expanding the key
    unsigned char *expanded_key = expand_key(key);

    // Converting the plaintext into a 4x4 matrix
    unsigned char matrix[4][4];
    bytes2matrix(plaintext, matrix);

    // Perform the initial round
    add_round_key(matrix, expanded_key);
    // Perform the 9 rounds
    for (int i = 1; i < 10; i++) {
        sub_bytes(matrix);
        shift_rows(matrix);
        mix_columns(matrix);
        add_round_key(matrix, expanded_key + i * 16);
    }
    // Perform the final round
    sub_bytes(matrix);
    shift_rows(matrix);
    add_round_key(matrix, expanded_key + 160);
    // Free the memory allocated for the expanded key
    free_memory(expanded_key);
    // Convert the 4x4 matrix back into a 16-byte block
    matrix2bytes(matrix, output);
    return output;
}

unsigned char *aes_decrypt_block(unsigned char *ciphertext,
                                 unsigned char *key) {
    // Decrypts a single block of ciphertext using the given key
    unsigned char *output =
        (unsigned char *)malloc(sizeof(unsigned char) * BLOCK_SIZE);

    // Expand the key
    unsigned char *expanded_key = expand_key(key);
    // Convert the ciphertext into a 4x4 matrix
    unsigned char matrix[4][4];
    bytes2matrix(ciphertext, matrix);
    // Perform the initial round
    add_round_key(matrix, expanded_key + 160);
    invert_shift_rows(matrix);
    invert_sub_bytes(matrix);
    // Perform the 9 rounds
    for (int i = 9; i > 0; i--) {
        add_round_key(matrix, expanded_key + i * 16);
        invert_mix_columns(matrix);
        invert_shift_rows(matrix);
        invert_sub_bytes(matrix);
    }
    // Perform the final round
    add_round_key(matrix, expanded_key);
    // free the memory allocated for the expanded key
    free_memory(expanded_key);
    // Convert the 4x4 matrix back into a 16-byte block
    matrix2bytes(matrix, output);
    return output;
}

