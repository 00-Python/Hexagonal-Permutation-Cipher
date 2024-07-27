import numpy as np
import math
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from typing import List, Tuple

# Constants for AES encryption
AES_BLOCK_SIZE = 16

def create_hexagonal_grid(size: int) -> List[List[int]]:
    """
    Create a hexagonal grid of integers.

    Args:
        size (int): The size of the grid.

    Returns:
        List[List[int]]: The hexagonal grid in a 2D list representation.
    """
    grid = []
    counter = 1

    # Create the upper part of the hexagon (including the middle row)
    for row in range(size):
        # Append a row of increasing integers
        grid.append(list(range(counter, counter + size + row)))
        counter += (size + row)

    # Create the lower part of the hexagon
    for row in range(size - 1):
        # Append a row of decreasing integers
        grid.append(list(range(counter, counter + 2 * size - row - 2)))
        counter += (2 * size - row - 2)

    return grid

def permute_grid(grid: List[List[int]], key: bytes) -> List[List[int]]:
    """
    Permute the hexagonal grid using a key.

    Args:
        grid (List[List[int]]): The original hexagonal grid.
        key (bytes): The key used for permutation.

    Returns:
        List[List[int]]: The permuted hexagonal grid.
    """
    # Flatten the grid to a 1D list
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)

    # Create a random number generator with the provided key as seed
    seed = int.from_bytes(key, byteorder='big')
    rng = np.random.default_rng(seed)

    # Generate permuted indices for the flat grid
    permuted_indices = rng.permutation(size)
    
    # Create a new flat grid with permuted values
    permuted_flat_grid = [flat_grid[i] for i in permuted_indices]

    # Convert the flat permuted grid back to 2D list representation
    permuted_grid = []
    index = 0
    for row in grid:
        permuted_grid.append(permuted_flat_grid[index:index + len(row)])
        index += len(row)
    
    return permuted_grid

def text_to_matrix(text: str, grid: List[List[int]]) -> List[List[int]]:
    """
    Convert text into a matrix based on the provided grid.

    Args:
        text (str): The text to convert.
        grid (List[List[int]]): The grid layout to use for the matrix.

    Returns:
        List[List[int]]: The text represented as a matrix of integers.
    """
    # Flatten the grid to get the total size
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)

    # Pad the text so its length matches the size of the grid
    text_padded = list(text.ljust(size, ' '))

    # Convert the padded text into a matrix
    matrix = [[ord(text_padded.pop(0)) for _ in row] for row in grid]
    return matrix

def matrix_to_text(matrix: List[List[int]]) -> str:
    """
    Convert a matrix back to text.

    Args:
        matrix (List[List[int]]): The matrix to convert.

    Returns:
        str: The resulting text.
    """
    # Flatten the matrix to a 1D list
    flat_matrix = [num for row in matrix for num in row]

    # Convert the integers back to characters and remove any padding
    text = ''.join(chr(num) for num in flat_matrix).rstrip()
    return text

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data using AES encryption.

    Args:
        data (bytes): The data to encrypt.
        key (bytes): The key for encryption.

    Returns:
        bytes: The encrypted data with the IV prepended.
    """
    cipher = AES.new(key, AES.MODE_CBC)  # Create a new AES cipher object in CBC mode
    encrypted_data = cipher.encrypt(pad(data, AES_BLOCK_SIZE))  # Encrypt the data with padding
    return cipher.iv + encrypted_data  # Prepend the IV to the encrypted data

def aes_decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt data using AES encryption.

    Args:
        encrypted_data (bytes): The encrypted data with the IV prepended.
        key (bytes): The key for decryption.

    Returns:
        bytes: The decrypted data without padding.
    """
    iv = encrypted_data[:AES_BLOCK_SIZE]  # Extract the IV from the encrypted data
    encrypted_data = encrypted_data[AES_BLOCK_SIZE:]  # Extract the actual encrypted data
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Create a new AES cipher object with the extracted IV
    return unpad(cipher.decrypt(encrypted_data), AES_BLOCK_SIZE)  # Decrypt and unpad the data

def encrypt(text: str, key: str) -> str:
    """
    Encrypt a given text using hexagonal permutation and AES encryption.

    Args:
        text (str): The plaintext to encrypt.
        key (str): The key used for encryption.

    Returns:
        str: The encrypted text.
    """
    # Determine the size of the hexagonal grid
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    
    # Hash the key to get a fixed-length AES key
    aes_key = hashlib.sha256(key.encode()).digest()

    # Permute the grid based on the AES key
    permuted_grid = permute_grid(grid, aes_key)
    
    # Convert the text to a matrix based on the original grid
    matrix = text_to_matrix(text, grid)
    
    # Flatten the matrix to a 1D list of integers
    flattened_matrix = [cell for row in matrix for cell in row]
    
    # Convert the list of integers to bytes
    data_bytes = bytes(flattened_matrix)
    
    # Encrypt the data bytes using AES
    encrypted_data = aes_encrypt(data_bytes, aes_key)
    
    # Convert the encrypted bytes to a string
    encrypted_text = ''.join(chr(byte) for byte in encrypted_data)
    return encrypted_text

def decrypt(encrypted_text: str, key: str) -> str:
    """
    Decrypt the given encrypted text using hexagonal permutation and AES decryption.

    Args:
        encrypted_text (str): The encrypted text to decrypt.
        key (str): The key used for decryption.

    Returns:
        str: The decrypted plaintext.
    """
    # Determine the size of the hexagonal grid
    size = max(1, math.ceil((len(encrypted_text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    
    # Hash the key to get a fixed-length AES key
    aes_key = hashlib.sha256(key.encode()).digest()

    # Permute the grid based on the AES key
    permuted_grid = permute_grid(grid, aes_key)

    # Convert the encrypted text to bytes
    encrypted_data = bytes(ord(char) for char in encrypted_text)
    
    # Decrypt the data bytes using AES
    decrypted_data = aes_decrypt(encrypted_data, aes_key)

    # Convert the decrypted byte data back to text
    decrypted_text = ''.join(chr(byte) for byte in decrypted_data).rstrip()
    
    # Convert the decrypted text to a matrix based on the original grid
    decrypted_matrix = text_to_matrix(decrypted_text, grid)
    
    return decrypted_text

# The main block to test the encryption and decryption
if __name__ == "__main__":
    plaintext = "This is a longer unique and evecccccccccccccccn longer cryptographic cipher test !"
    key = "SuperSecretKey"

    print("Plaintext:", plaintext)

    # Encrypt the plaintext
    encrypted_text = encrypt(plaintext, key)
    print("Encrypted:", encrypted_text)
    print("Encrypted length:", len(encrypted_text))

    # Decrypt the encrypted text
    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)
    print("Decrypted length:", len(decrypted_text))

    # Assert that the decryption correctly restores the original plaintext
    assert plaintext == decrypted_text, "Decryption failed"