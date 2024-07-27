Welcome to the **Hexagonal Permutation Cipher (HPC)**! This is a hobbyist project exploring a custom encryption algorithm implemented in Python. **It is not intended for production use** and serves as a fun exploration into cryptography concepts. The algorithm leverages hexagonal grid permutations in conjunction with AES encryption to provide an added layer of security to standard text encryption. 

**Note:** This project is a personal exploration and is not intended for production use. Please do not use it for real-world security applications.

## Table of Contents
- [Features](#features)
- [Understanding the Algorithm](#understanding-the-algorithm)
    - [Hexagonal Grid Structure](#hexagonal-grid-structure)
    - [Permutation Mechanism](#permutation-mechanism)
    - [AES Encryption](#aes-encryption)
    - [Decryption Process](#decryption-process)
- [Technologies Used](#technologies-used)
- [Installation and Usage](#installation-and-usage)
- [Usage Guide](#usage-guide)
    - [Encrypting Text](#encrypting-text)
    - [Decrypting Text](#decrypting-text)
    - [Visualizing Permutations](#visualizing-permutations)
- [Security Considerations](#security-considerations)
- [Potential Applications](#potential-applications)
- [Additional Notes](#additional-notes)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

- **Hexagonal Grid Permutation:** The positions of characters are shuffled based on a key, using a hexagonal grid structure for the permutation.
- **AES Encryption:** The permuted data is further encrypted using the strong AES algorithm in CBC mode.
- **Key-Based Encryption:** Encryption and decryption rely on a secret key, hashed for added security.
- **Visualization:** Includes a `animate_permutation` function to visualize the permutation process using Pygame.
- **Retro Effects:** Added scanlines and noise to the visualization for a retro monitor effect.

## Understanding the Algorithm

### Hexagonal Grid Structure

The core of the algorithm is a hexagonal grid, a two-dimensional structure with interconnected hexagonal cells. The grid's size adapts dynamically to the length of the input text.

### Permutation Mechanism

1. **Key Hashing:** The user-provided key is hashed using SHA256 to generate a random number generator seed and the AES encryption key.
2. **Index Permutation:** A random permutation of indices is created based on the seed, dictating the order in which the grid cells are shuffled.
3. **Matrix Transformation and Permutation:** The plaintext is converted into a matrix conforming to the grid's shape, and then this matrix is permuted according to the generated indices.

### AES Encryption

The permuted data is then encrypted using AES in CBC (Cipher Block Chaining) mode with PKCS7 padding. The same hashed key used for permutation ensures consistency in encryption and decryption.

### Decryption Process

The decryption process is the inverse of encryption:

1. The encrypted text is converted back into a matrix.
2. The inverse permutation is applied to the matrix.
3. AES decryption is used to recover the original plaintext.

## Technologies Used

The project leverages the following Python libraries:

- **NumPy:** For efficient numerical operations and matrix manipulations.
- **PyCryptodome:** For implementing the AES encryption and decryption.
- **Pygame:** For creating the visual representation of the permutation process.

## Installation and Usage

To get started with the Hexagonal Permutation Cipher, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/00-Python/Hexagonal-Permutation-Cipher.git
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```sh
   python hpc.py
   ```

## Usage Guide

### Encrypting Text

To encrypt text using the Hexagonal Permutation Cipher:

1. **Provide the plaintext and the key:**
    ```python
    plaintext = "This is a test message!"
    key = "SuperSecretKey"
    ```

2. **Call the `encrypt` function:**
    ```python
    encrypted_text = encrypt(plaintext, key)
    print("Encrypted:", encrypted_text)
    ```

### Decrypting Text

To decrypt text using the Hexagonal Permutation Cipher:

1. **Provide the encrypted text and the key:**
    ```python
    encrypted_text = "...."  # The encrypted string
    key = "SuperSecretKey"
    ```

2. **Call the `decrypt` function:**
    ```python
    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)
    ```

### Visualizing Permutations

To visualize the permutation process using Pygame:

1. **Generate the hexagonal grid:**
    ```python
    text = "This is a test message!"
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    key = "SuperSecretKey"
    aes_key = hashlib.sha256(key.encode()).digest()
    ```

2. **Call the `animate_permutation` function:**
    ```python
    animate_permutation(grid, aes_key)
    ```

## Security Considerations

As this project is a hobbyist and exploratory project, several security considerations are highlighted:

- **Not Production Ready:** This project is not suitable for production use.
- **No Security Audits:** The algorithm has not undergone any security audits or rigorous testing.
- **Experimental:** It is an experimental project meant for educational purposes and to spur curiosity about cryptography.

## Potential Applications

While not suited for production use, some potential exploratory applications include:

- **Educational Tool:** Teaching principles of cryptography and permutations.
- **Creative Projects:** Integrating the encryption algorithm into art or performance pieces.
- **Visualization:** Creating engaging visualizations to illustrate encryption/decryption processes.

## Additional Notes

- **Padding:** The plaintext is padded with spaces if it doesn't fit perfectly into the grid. This padding is removed during decryption.
- **Byte Conversion:** The matrix data is converted to bytes before encryption and back to characters after decryption for compatibility.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit pull requests with your enhancements or bug fixes. Feel free to open issues to report bugs or suggest new features.

## Contact

If you have any questions or suggestions, feel free to reach me:

- **GitHub:** [00-Python](https://github.com/00-Python)