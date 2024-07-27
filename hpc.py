import random
import math

def create_hexagonal_grid(size):
    grid = []
    counter = 1
    for row in range(size):
        grid.append(list(range(counter, counter + size + row)))
        counter += (size + row)
    for row in range(size - 1):
        grid.append(list(range(counter, counter + 2 * size - row - 2)))
        counter += (2 * size - row - 2)
    return grid

def permute_grid(grid, key):
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)
    key_value = sum(ord(c) for c in key) % size

    random.seed(key_value)
    permuted_flat_grid = flat_grid[:]
    random.shuffle(permuted_flat_grid)

    permuted_grid = []
    index = 0
    for row in grid:
        permuted_grid.append(permuted_flat_grid[index:index + len(row)])
        index += len(row)
    
    print("Key for permutation:", key_value)
    print("Flat grid for permutation:", flat_grid)
    print("Permuted flat grid:", permuted_flat_grid)
    
    return permuted_grid, permuted_flat_grid

def text_to_matrix(text, grid):
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)
    text = list(text.ljust(size, ' '))  # Ensure text is padded to fit the grid
    matrix = [[ord(text.pop(0)) for _ in row] for row in grid]

    print("Text after padding:", text)
    print("Matrix created from text:", matrix)
    
    return matrix

def matrix_to_text(matrix):
    flat_matrix = [num for row in matrix for num in row]
    text = ''.join(chr(num) for num in flat_matrix).rstrip()  # Remove trailing padding

    print("Flat matrix converted to text:", text)
    
    return text

def encrypt(text, key):
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    permuted_grid, permuted_flat_grid = permute_grid(grid, key)

    print("Original grid for encryption:", grid)
    print("Permuted grid for encryption:", permuted_grid)

    matrix = text_to_matrix(text, grid)
    flattened_matrix = [cell for row in matrix for cell in row]

    print("Flattened matrix for encryption:", flattened_matrix)

    encrypted_flat = [flattened_matrix[permuted_flat_grid.index(pos + 1)] for pos in range(len(flattened_matrix))]

    encrypted_matrix = []
    index = 0
    for row in permuted_grid:
        encrypted_matrix.append(encrypted_flat[index:index + len(row)])
        index += len(row)

    encrypted_text = matrix_to_text(encrypted_matrix)
    return encrypted_text

def decrypt(encrypted_text, key):
    size = max(1, math.ceil((len(encrypted_text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    permuted_grid, permuted_flat_grid = permute_grid(grid, key)

    print("Decryption original grid:", grid)
    print("Decryption permuted grid:", permuted_grid)

    reverse_permuted = {value: idx for idx, value in enumerate(permuted_flat_grid)}

    print("Reverse Permuted Mapping:", reverse_permuted)

    matrix = text_to_matrix(encrypted_text, permuted_grid)
    flattened_matrix = [cell for row in matrix for cell in row]

    print("Flattened matrix from encrypted text:", flattened_matrix)

    decrypted_flat = [None] * len(flattened_matrix)
    for idx in range(len(flattened_matrix)):
        original_pos = reverse_permuted[idx + 1]
        decrypted_flat[original_pos] = flattened_matrix[idx]

    decrypted_matrix = []
    index = 0
    for row in grid:
        decrypted_matrix.append(decrypted_flat[index:index + len(row)])
        index += len(row)

    decrypted_text = matrix_to_text(decrypted_matrix)
    
    print("Decrypted text before trimming:", decrypted_text)
    
    return decrypted_text

if __name__ == "__main__":
    plaintext = "This is a unique cryptographic cipher test!"
    key = "SuperSecretKey"

    print("Plaintext:", plaintext)

    encrypted_text = encrypt(plaintext, key)
    print("Encrypted:", encrypted_text)
    print("Encrypted length:", len(encrypted_text))

    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)
    print("Decrypted length:", len(decrypted_text))

    assert plaintext == decrypted_text, "Decryption failed"
