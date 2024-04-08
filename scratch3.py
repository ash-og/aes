 int current_size = 0;
  int rconIteration = 1;
  int i;
  unsigned char word;

    // Copy the initial cipher key into the expanded key
    for (i = 0; i < BLOCK_SIZE; i++) {
        expandedKey[i] = cipher_key[i];
    }

    // Key expansion loop
    while (current_size < KEY_EXP_SIZE) {

        // Assign the value of the previous four bytes
        word = (expandedKey + current_size - 4);

        // If the current_size is a multiple of the block size, perform a key schedule core operation
        if (current_size % BLOCK_SIZE == 0) {
          word = rotWord(word);
        }
    } int current_size = 0;
  int rconIteration = 1;
  int i;
  unsigned char word;

    // Copy the initial cipher key into the expanded key
    for (i = 0; i < BLOCK_SIZE; i++) {
        expandedKey[i] = cipher_key[i];
    }

    // Key expansion loop
    while (current_size < KEY_EXP_SIZE) {

        // Assign the value of the previous four bytes
        word = (expandedKey + current_size - 4);

        // If the current_size is a multiple of the block size, perform a key schedule core operation
        if (current_size % BLOCK_SIZE == 0) {
          word = rotWord(word);
        }
    }