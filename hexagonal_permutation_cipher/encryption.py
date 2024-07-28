from hashlib import sha256
import base64
import math
import numpy as np  # Import the numpy library
from .grid import create_hexagonal_grid, text_to_matrix, Matrix
from .aes import aes_encrypt, aes_decrypt

def permute_grid(grid: np.ndarray, key: bytes) -> np.ndarray:
    """
    Permute the hexagonal grid using a key.

    Args:
        grid (np.ndarray): The original hexagonal grid.
        key (bytes): The key used for permutation.

    Returns:
        np.ndarray: The permuted hexagonal grid.
    """
    matrix = Matrix(grid)
    flat_grid = matrix.flat
    size = len(flat_grid)

    # Create a random number generator with the provided key as seed
    seed = int.from_bytes(key, byteorder='big')
    rng = np.random.default_rng(seed)

    # Generate permuted indices for the flat grid
    permuted_indices = rng.permutation(size)
    
    # Create a new flat grid with permuted values
    permuted_flat_grid = flat_grid[permuted_indices]

    # Convert the flat permuted grid back to 2D numpy array representation
    return matrix.to_2d(permuted_flat_grid)

def encrypt(text: str, key: str) -> str:
    """
    Encrypt text using hexagonal permutation and AES encryption.

    Args:
        text (str): The plaintext to encrypt.
        key (str): The encryption key.

    Returns:
        str: The encrypted text (Base64 encoded).
    """
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)

    # Derive AES key from the provided key
    aes_key = sha256(key.encode()).digest()
    permuted_grid = permute_grid(grid, aes_key)

    matrix = text_to_matrix(text, permuted_grid)
    flattened_matrix = matrix.flatten()

    # Join the characters into a single string and then convert to bytes
    data_bytes = ''.join(flattened_matrix).encode('utf-8')

    encrypted_data = aes_encrypt(data_bytes, aes_key)

    # Encode encrypted data to Base64 to ensure safe transmission
    encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_text

def decrypt(encrypted_text: str, key: str) -> str:
    """
    Decrypt text encrypted using hexagonal permutation and AES encryption.

    Args:
        encrypted_text (str): The encrypted text (Base64 encoded).
        key (str): The decryption key.

    Returns:
        str: The decrypted text.
    """
    # Decode the Base64 encoded string to bytes
    encrypted_data = base64.b64decode(encrypted_text)

    # Derive AES key from the provided key
    aes_key = sha256(key.encode()).digest()

    # Decrypt AES-encrypted data
    decrypted_data = aes_decrypt(encrypted_data, aes_key)

    # Convert byte data to string for further processing
    decrypted_text = decrypted_data.decode('utf-8')

    # Determine grid size
    total_chars = len(decrypted_text)
    grid_size = max(1, math.ceil((total_chars / 3) ** 0.5))

    grid = create_hexagonal_grid(grid_size)
    permuted_grid = permute_grid(grid, aes_key)

    # Create matrix from the decrypted text
    decrypted_matrix = text_to_matrix(decrypted_text, permuted_grid)

    # Ensure the decrypted text is trimmed to match original text length without padding
    final_decrypted_text = ''.join(decrypted_matrix.flatten()).rstrip()

    return final_decrypted_text