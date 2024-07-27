# Hexagonal Permutation Cipher (HPC)

Welcome to the Hexagonal Permutation Cipher (HPC) repository! HPC is a unique cryptographic algorithm that utilizes hexagonal grid permutations combined with AES encryption for secure text encryption and decryption.

## Overview

The Hexagonal Permutation Cipher (HPC) is designed to provide a novel approach to cryptography by:
- Using a hexagonal grid for permutation-based encryption.
- Leveraging AES encryption for secure data handling.
- Combining permutation and AES for enhanced security.

## Features

- **Unique Encryption Algorithm**: A novel approach that leverages hexagonal grids for permutation and AES for encryption.
- **Secure AES Encryption**: Uses AES encryption in CBC mode with PKCS7 padding for robust security.
- **Key-Based Encryption**: Uses a hashed secret key to configure permutation and AES operations.
- **Efficient Numpy Integration**: Utilizes numpy for efficient grid operations and matrix manipulations.
- **Improved Performance**: Enhanced performance through optimized matrix operations using numpy arrays.
- **Pure Python Implementation**: Implemented in Python with minimal external dependencies.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Examples](#examples)
- [Contributing](#contributing)

## Installation

To get started with HPC, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/00-Python/Hexagonal-Permutation-Cipher.git
cd Hexagonal-Permutation-Cipher
pip install -r requirements.txt
```

## Usage

### Encrypting Text

To encrypt text using the HPC algorithm, use the `encrypt` function:

```python
from hpc import encrypt

plaintext = "This is a unique cryptographic cipher test!"
key = "SuperSecretKey"

encrypted_text = encrypt(plaintext, key)
print("Encrypted:", encrypted_text)
```

### Decrypting Text

To decrypt text, use the `decrypt` function:

```python
from hpc import decrypt

decrypted_text = decrypt(encrypted_text, key)
print("Decrypted:", decrypted_text)
```

## Algorithm Details

### Hexagonal Grid Permutation

- **Hexagonal Grid**: A 2D grid with hexagonal cells is used for permutation operations, now implemented using numpy arrays for efficient manipulation.
- **Permutation Function**: Permutations are applied based on key-derived values to shuffle the grid cells using numpy's permutation functions.

### Encryption Process

1. **Convert Text to Matrix**: Convert plaintext into a numpy array matrix based on the hexagonal grid.
2. **Apply Permutations**: Permute the matrix using a seeded random number generator derived from the hashed key.
3. **AES Encryption**: Encrypt the permuted data using AES with the hashed key.
4. **Convert to Encrypted Text**: Convert the encrypted byte data to text.

### Decryption Process

1. **AES Decryption**: Decrypt the encrypted data using AES with the hashed key.
2. **Convert Encrypted Text to Matrix**: Convert the decrypted byte data into a numpy array matrix.
3. **Reverse Permutations**: Reverse the permutation process using the key.
4. **Convert Back to Original Text**: Convert the matrix back to plaintext.

## Examples

### Example Code

Here’s a complete example showing both encryption and decryption:

```python
from hpc import encrypt, decrypt

plaintext = "This is a unique cryptographic cipher test!"
key = "SuperSecretKey"

# Encrypt the plaintext
encrypted_text = encrypt(plaintext, key)
print("Encrypted:", encrypted_text)

# Decrypt the encrypted text
decrypted_text = decrypt(encrypted_text, key)
print("Decrypted:", decrypted_text)
```

## Contributing

We welcome contributions to the HPC project! If you have suggestions, bug reports, or would like to contribute code, please follow these steps:

1. **Fork the Repository**: Create your own fork of the repository on GitHub.
2. **Create a Branch**: Create a new branch for your changes.
3. **Commit Changes**: Make your changes and commit them to your branch.
4. **Push and Pull Request**: Push your changes and create a pull request for review.

Please adhere to the best practices and ensure your changes are thoroughly tested.
