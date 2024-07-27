import numpy as np
import math
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from typing import List, Tuple
import pygame
import time
import random

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
        grid.append(list(range(counter, counter + size + row)))
        counter += (size + row)

    # Create the lower part of the hexagon
    for row in range(size - 1):
        grid.append(list(range(counter, counter + 2 * size - row - 2)))
        counter += (2 * size - row - 2)

    return grid

def hex_coord(x, y, size):
    """
    Calculate the 2D coordinates for a hexagon in a hexagonal grid.

    Args:
        x (int): The x-coordinate in the grid.
        y (int): The y-coordinate in the grid.
        size (float): The size of the hexagon.

    Returns:
        Tuple[float, float]: The calculated 2D coordinates for the hexagon.
    """
    return (size * (3 / 2 * x), size * (np.sqrt(3) * (y + 0.5 * (x % 2))))

def draw_hex(surface, x, y, size, facecolor, text, font):
    """
    Draw a hexagon on the Pygame surface.

    Args:
        surface : The Pygame surface to draw on.
        x (int): The x-coordinate in the grid.
        y (int): The y-coordinate in the grid.
        size (float): The size of the hexagon.
        facecolor (str): The color to fill the hexagon.
        text (str): The text to display inside the hexagon.
        font : The font used to render the text.
    """
    xy = hex_coord(x, y, size)
    hexagon = [
        (xy[0] + size * np.cos(np.radians(angle)), xy[1] + size * np.sin(np.radians(angle)))
        for angle in range(30, 360, 60)
    ]
    pygame.draw.polygon(surface, facecolor, hexagon)
    # Render the text inside the hexagon
    text_surf = font.render(text, True, pygame.Color('green'))
    text_rect = text_surf.get_rect(center=xy)
    surface.blit(text_surf, text_rect)

def text_to_matrix(text: str, grid: List[List[int]]) -> List[List[str]]:
    """
    Convert text into a matrix based on the grid's structure.

    Args:
        text (str): The input text.
        grid (List[List[int]]): The hexagonal grid.

    Returns:
        List[List[str]]: The matrix representation of the text.
    """
    flat_grid_length = sum(len(row) for row in grid)
    padded_text = text.ljust(flat_grid_length)  # Pad text to fit into the grid
    chars = iter(padded_text)
    
    matrix = []
    for row in grid:
        matrix.append([next(chars) for _ in row])
    
    return matrix

def permute_grid(grid: List[List[int]], key: bytes) -> List[List[int]]:
    """
    Permute the hexagonal grid using a key.

    Args:
        grid (List[List[int]]): The original hexagonal grid.
        key (bytes): The key used for permutation.

    Returns:
        List[List[int]]: The permuted hexagonal grid.
    """
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

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data using AES encryption (CBC mode).

    Args:
        data (bytes): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The IV followed by the encrypted data.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data, AES_BLOCK_SIZE))
    return cipher.iv + encrypted_data

def aes_decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt AES-encrypted data (CBC mode).

    Args:
        encrypted_data (bytes): The encrypted data (IV followed by ciphertext).
        key (bytes): The decryption key.

    Returns:
        bytes: The decrypted data.
    """
    iv = encrypted_data[:AES_BLOCK_SIZE]
    encrypted_data = encrypted_data[AES_BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), AES_BLOCK_SIZE)

def encrypt(text: str, key: str) -> str:
    """
    Encrypt text using hexagonal permutation and AES encryption.

    Args:
        text (str): The plaintext to encrypt.
        key (str): The encryption key.

    Returns:
        str: The encrypted text.
    """
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    
    # Derive AES key from the provided key
    aes_key = hashlib.sha256(key.encode()).digest()
    permuted_grid = permute_grid(grid, aes_key)
    
    matrix = text_to_matrix(text, grid)
    flattened_matrix = [cell for row in matrix for cell in row]
    data_bytes = bytes(ord(char) for char in flattened_matrix)  # Convert chars to their ASCII values
    encrypted_data = aes_encrypt(data_bytes, aes_key)
    encrypted_text = ''.join(chr(byte) for byte in encrypted_data)
    return encrypted_text

def decrypt(encrypted_text: str, key: str) -> str:
    """
    Decrypt text encrypted using hexagonal permutation and AES encryption.

    Args:
        encrypted_text (str): The encrypted text.
        key (str): The decryption key.

    Returns:
        str: The decrypted text.
    """
    size = max(1, math.ceil((len(encrypted_text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    
    # Derive AES key from the provided key
    aes_key = hashlib.sha256(key.encode()).digest()
    permuted_grid = permute_grid(grid, aes_key)
    encrypted_data = bytes(ord(char) for char in encrypted_text)
    decrypted_data = aes_decrypt(encrypted_data, aes_key)
    decrypted_text = ''.join(chr(byte) for byte in decrypted_data).rstrip()
    decrypted_matrix = text_to_matrix(decrypted_text, grid)
    return decrypted_text

def add_scanlines(surface):
    """
    Add scanlines to the surface to create a retro monitor effect.

    Args:
        surface : The surface to draw on.
    """
    width, height = surface.get_size()
    for y in range(0, height, 2):  # Adding horizontal lines at every alternate row
        pygame.draw.line(surface, pygame.Color('darkgreen'), (0, y), (width, y))

def add_noise(surface, amount=0.02):
    """
    Add noise to the surface to create a retro monitor effect.

    Args:
        surface : The surface to draw on.
        amount (float): The amount of noise to add. Default is 0.02.
    """
    width, height = surface.get_size()
    noise_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for _ in range(int(width * height * amount)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        color = (0, random.randint(50, 255), 0, random.randint(50, 100))  # Greenish noise
        noise_surf.set_at((x, y), color)
    surface.blit(noise_surf, (0, 0))

def animate_permutation(grid: List[List[int]], key: bytes, width=800, height=600):
    """
    Animate the permutation process of the hexagonal grid.

    Args:
        grid (List[List[int]]): The original hexagonal grid.
        key (bytes): The key used for permutation.
        width (int): The width of the Pygame window. Default is 800.
        height (int): The height of the Pygame window. Default is 600.
    """
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hexagonal Permutation Animation")

    # Load the retro monospaced/pixel font
    font = pygame.font.Font(pygame.font.match_font('monospace'), 24)
    size = 30

    flat_grid = [cell for row in grid for cell in row]
    grid_length = len(flat_grid)

    # Create a random number generator with the provided key as seed
    seed = int.from_bytes(key, byteorder='big')
    rng = np.random.default_rng(seed)
    permuted_indices = rng.permutation(grid_length)

    clock = pygame.time.Clock()
    running = True
    frame = 0

    while running and frame <= grid_length:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Dark background for retro look

        current_indices = permuted_indices[:frame + 1]
        current_grid = [flat_grid[idx] if idx in current_indices else None for idx in range(grid_length)]

        index = 0
        for y, row in enumerate(grid):
            for x, _ in enumerate(row):
                if current_grid[index] is not None:
                    draw_hex(screen, x, y, size, pygame.Color('darkgreen'), str(current_grid[index]), font)
                index += 1

        add_scanlines(screen)
        add_noise(screen)

        pygame.display.flip()
        clock.tick(10)
        frame += 1

    pygame.quit()

if __name__ == "__main__":
    plaintext = "This is a longer unique and even longer Tru Encryption cryptographic cipher test!"
    key = "SuperSecretKey"

    print("Plaintext:", plaintext)

    encrypted_text = encrypt(plaintext, key)
    print("Encrypted:", encrypted_text)
    print("Encrypted length:", len(encrypted_text))

    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)
    print("Decrypted length:", len(decrypted_text))

    assert plaintext == decrypted_text, "Decryption failed"

    size = max(1, math.ceil((len(plaintext) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    aes_key = hashlib.sha256(key.encode()).digest()
    animate_permutation(grid, aes_key)