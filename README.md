# Hexagonal Permutation Cipher (HPC)

<!-- ![Hexagonal Permutation Cipher](https://your-image-link.com/banner.png) -->

[![GitHub issues](https://img.shields.io/github/issues/00-Python/Hexagonal-Permutation-Cipher.svg)](https://github.com/00-Python/Hexagonal-Permutation-Cipher/issues)
[![GitHub stars](https://img.shields.io/github/stars/00-Python/Hexagonal-Permutation-Cipher.svg)](https://github.com/00-Python/Hexagonal-Permutation-Cipher/stargazers)
[![License](https://img.shields.io/github/license/00-Python/Hexagonal-Permutation-Cipher.svg)](https://github.com/00-Python/Hexagonal-Permutation-Cipher/blob/main/LICENSE)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/00-Python/Hexagonal-Permutation-Cipher)](https://github.com/00-Python/Hexagonal-Permutation-Cipher)

This is a hobbyist project exploring a custom encryption algorithm implemented in Python. **It is not intended for production use** and serves as a fun exploration into cryptography concepts. The algorithm leverages hexagonal grid permutations in conjunction with AES encryption to provide an added layer of security to standard text encryption.

**Note:** This project is a personal exploration and is not intended for production use. Please do not use it for real-world security applications.


## Table of Contents
- [Introduction](#introduction)
    - [Hexagonal Grid Structure](#hexagonal-grid-structure)
    - [Permutation Mechanism](#permutation-mechanism)
    - [AES Encryption](#aes-encryption)
    - [Decryption Process](#decryption-process)
- [Technologies Used](#technologies-used)
- [Installation and Usage](#installation-and-usage)
- [Code Walkthrough](#code-walkthrough)
    - [Creating the Hexagonal Grid](#creating-the-hexagonal-grid)
    - [Permutation of the Grid](#permutation-of-the-grid)
    - [Hex to 2D Conversion](#hex-to-2d-conversion)
    - [AES Encryption and Decryption](#aes-encryption-and-decryption)
    - [Animation of Permutation](#animation-of-permutation)
- [Examples](#examples)
- [Potential Applications](#potential-applications)
- [Additional Notes](#additional-notes)
- [Contributing](#contributing)
- [License](#license)

## Introduction

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

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat&logo=numpy&logoColor=white)
![PyCryptodome](https://img.shields.io/badge/-PyCryptodome-6A5ACD?style=flat&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/-Pygame-4CAF50?style=flat&logo=pygame&logoColor=white)

The project leverages the following Python libraries:
- **NumPy:** For efficient numerical operations and matrix manipulations.
- **PyCryptodome:** For implementing the AES encryption and decryption.
- **Pygame:** For creating the visual representation of the permutation process.

## Installation and Usage

    pip install Hexagonal-Permutation-Cipher==1.0.0

Then just run hpc -h for list of commands.


## Potential Applications

While this project is a hobbyist exploration and **not intended for production use**, it provides insights into cryptographic concepts and can be used for:
- Educational purposes to understand encryption and permutation.
- As a base for creating custom ciphers in academic projects.
- Visual demonstrations of grid-based permutation concepts.

## Additional Notes

- **Padding:** The plaintext is padded with spaces if it doesn't fit perfectly into the grid. This padding is removed during decryption.
- **Byte Conversion:** The matrix data is converted to bytes before encryption and back to characters after decryption for compatibility.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit pull requests with your enhancements or bug fixes. Feel free to open issues to report bugs or suggest new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.