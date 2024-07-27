# Hexagonal Permutation Cipher (HPC)

Welcome to the Hexagonal Permutation Cipher (HPC) repository! HPC is a unique, dependency-free cryptographic algorithm that utilizes hexagonal grid permutations combined with modular arithmetic for secure text encryption and decryption.

## Overview

The Hexagonal Permutation Cipher (HPC) is designed to provide a novel approach to cryptography by:
- Using a hexagonal grid for permutation-based encryption.
- Employing modular arithmetic to manage values.
- Avoiding external dependencies for maximum portability.

## Features

- **Unique Encryption Algorithm**: A novel approach that leverages hexagonal grids for encryption.
- **Dependency-Free**: Implemented in pure Python with no external libraries.
- **Modular Arithmetic**: Ensures all values remain within a manageable range.
- **Key-Based Encryption**: Uses a secret key to configure permutation operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Examples](#examples)
- [Contributing](#contributing)

## Installation

To get started with HPC, simply clone the repository:

```bash
git clone https://github.com/00-Python/Hexagonal-Permutation-Cipher.git
cd Hexagonal-Permutation-Cipher
```

No additional dependencies are required beyond standard Python libraries.

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

- **Hexagonal Grid**: A 2D grid with hexagonal cells is used for permutation operations.
- **Permutation Function**: Permutations are applied based on key-derived values to shuffle the grid cells.

### Encryption Process

1. **Convert Text to Matrix**: Convert plaintext into a matrix of integers.
2. **Apply Permutations**: Permute the matrix based on the hexagonal grid and key.
3. **Convert Back to Text**: Convert the permuted matrix back to text.

### Decryption Process

1. **Convert Encrypted Text to Matrix**: Convert the encrypted text into a matrix.
2. **Reverse Permutations**: Reverse the permutation process using the key.
3. **Convert Back to Original Text**: Convert the matrix back to plaintext.

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
