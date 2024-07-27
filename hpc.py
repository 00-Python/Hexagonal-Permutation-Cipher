import random
import math

def create_hexagonal_grid(size):
    """
    Creates a hexagonal grid pattern based on the specified size.
    
    The grid is structured such that the first `size` rows increase in length by 1
    element per row, and the remaining rows decrease in length symmetrically.

    Parameters:
    size (int): The base size of the hexagonal grid.

    Returns:
    list: A list of lists representing the hexagonal grid.
    """
    grid = []
    counter = 1
    # Generate the first `size` rows which increase in length
    for row in range(size):
        grid.append(list(range(counter, counter + size + row)))
        counter += (size + row)
    # Generate the remaining rows which decrease in length
    for row in range(size - 1):
        grid.append(list(range(counter, counter + 2 * size - row - 2)))
        counter += (2 * size - row - 2)
    return grid

def permute_grid(grid, key):
    """
    Permutes the grid based on a key using a pseudorandom shuffle.
    
    The grid is flattened, shuffled, and then reconstructed based on the provided key.

    Parameters:
    grid (list): The hexagonal grid to be permuted.
    key (str): The key used to seed the random number generator.

    Returns:
    tuple: A tuple containing the permuted grid and the permuted flat grid.
    """
    # Flatten the grid into a single list of cells
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)
    # Create a key value by summing the ASCII values of the characters in the key
    key_value = sum(ord(c) for c in key) % size

    random.seed(key_value)
    # Make a copy of the flat grid and shuffle it
    permuted_flat_grid = flat_grid[:]
    random.shuffle(permuted_flat_grid)

    permuted_grid = []
    index = 0
    # Reconstruct the permuted grid from the shuffled flat grid
    for row in grid:
        permuted_grid.append(permuted_flat_grid[index:index + len(row)])
        index += len(row)
    
    print("Key for permutation:", key_value)
    print("Flat grid for permutation:", flat_grid)
    print("Permuted flat grid:", permuted_flat_grid)
    
    return permuted_grid, permuted_flat_grid

def text_to_matrix(text, grid):
    """
    Converts a text string to a matrix based on the hexagonal grid.
    
    The text is padded to fit the grid if necessary, and then each character is
    converted to its ASCII value.

    Parameters:
    text (str): The text to be converted.
    grid (list): The hexagonal grid used to shape the matrix.

    Returns:
    list: A list of lists representing the text as ASCII values in the grid shape.
    """
    flat_grid = [cell for row in grid for cell in row]
    size = len(flat_grid)
    # Pad the text to fit the grid
    text = list(text.ljust(size, ' '))
    # Convert the text to a matrix of ASCII values
    matrix = [[ord(text.pop(0)) for _ in row] for row in grid]

    print("Text after padding:", text)
    print("Matrix created from text:", matrix)
    
    return matrix

def matrix_to_text(matrix):
    """
    Converts a matrix of ASCII values back to a text string.
    
    The matrix is flattened and then each ASCII value is converted back to a character.

    Parameters:
    matrix (list): A list of lists representing the matrix of ASCII values.

    Returns:
    str: The resulting text string.
    """
    # Flatten the matrix into a single list of ASCII values
    flat_matrix = [num for row in matrix for num in row]
    # Convert ASCII values to characters and remove trailing spaces
    text = ''.join(chr(num) for num in flat_matrix).rstrip()

    print("Flat matrix converted to text:", text)
    
    return text

def encrypt(text, key):
    """
    Encrypts a text string using a hexagonal grid and a permutation key.
    
    The text is converted to a matrix, permuted, and then flattened and shuffled
    based on the key.

    Parameters:
    text (str): The plaintext to be encrypted.
    key (str): The key used to seed the random number generator.

    Returns:
    str: The encrypted text.
    """
    # Determine the grid size based on the length of the text
    size = max(1, math.ceil((len(text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    permuted_grid, permuted_flat_grid = permute_grid(grid, key)

    print("Original grid for encryption:", grid)
    print("Permuted grid for encryption:", permuted_grid)

    matrix = text_to_matrix(text, grid)
    flattened_matrix = [cell for row in matrix for cell in row]

    print("Flattened matrix for encryption:", flattened_matrix)

    # Create the encrypted flat list by permuting the flattened matrix
    encrypted_flat = [flattened_matrix[permuted_flat_grid.index(pos + 1)] for pos in range(len(flattened_matrix))]

    encrypted_matrix = []
    index = 0
    # Reconstruct the encrypted matrix from the encrypted flat list
    for row in permuted_grid:
        encrypted_matrix.append(encrypted_flat[index:index + len(row)])
        index += len(row)

    encrypted_text = matrix_to_text(encrypted_matrix)
    return encrypted_text

def decrypt(encrypted_text, key):
    """
    Decrypts an encrypted text string using a hexagonal grid and a permutation key.
    
    The encrypted text is converted back to a matrix, permuted in reverse, and then
    reconstructed into the original text.

    Parameters:
    encrypted_text (str): The encrypted text to be decrypted.
    key (str): The key used to seed the random number generator.

    Returns:
    str: The decrypted (original) text.
    """
    # Determine the grid size based on the length of the encrypted text
    size = max(1, math.ceil((len(encrypted_text) / 3) ** 0.5))
    grid = create_hexagonal_grid(size)
    permuted_grid, permuted_flat_grid = permute_grid(grid, key)

    print("Decryption original grid:", grid)
    print("Decryption permuted grid:", permuted_grid)

    # Create a reverse mapping of the permuted grid
    reverse_permuted = {value: idx for idx, value in enumerate(permuted_flat_grid)}

    print("Reverse Permuted Mapping:", reverse_permuted)

    matrix = text_to_matrix(encrypted_text, permuted_grid)
    flattened_matrix = [cell for row in matrix for cell in row]

    print("Flattened matrix from encrypted text:", flattened_matrix)

    # Reconstruct the original flat list by reversing the permutation
    decrypted_flat = [None] * len(flattened_matrix)
    for idx in range(len(flattened_matrix)):
        original_pos = reverse_permuted[idx + 1]
        decrypted_flat[original_pos] = flattened_matrix[idx]

    decrypted_matrix = []
    index = 0
    # Reconstruct the decrypted matrix from the original flat list
    for row in grid:
        decrypted_matrix.append(decrypted_flat[index:index + len(row)])
        index += len(row)

    decrypted_text = matrix_to_text(decrypted_matrix)
    
    print("Decrypted text before trimming:", decrypted_text)
    
    return decrypted_text

if __name__ == "__main__":
    # Example usage
    plaintext = "This is a unique cryptographic cipher test!"
    key = "SuperSecretKey"

    print("Plaintext:", plaintext)

    # Encrypt the plaintext
    encrypted_text = encrypt(plaintext, key)
    print("Encrypted:", encrypted_text)
    print("Encrypted length:", len(encrypted_text))

    # Decrypt the text
    decrypted_text = decrypt(encrypted_text, key)
    print("Decrypted:", decrypted_text)
    print("Decrypted length:", len(decrypted_text))

    # Verify the decryption matches the original plaintext
    assert plaintext == decrypted_text, "Decryption failed"
