import numpy as np
from .grid import Matrix

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

def text_to_matrix(text: str, grid: np.ndarray) -> np.ndarray:
    """
    Convert text into a matrix based on the grid's structure.

    Args:
        text (str): The input text.
        grid (np.ndarray): The hexagonal grid.

    Returns:
        np.ndarray: The matrix representation of the text.
    """
    flat_grid_length = grid.size
    padded_text = text.ljust(flat_grid_length)  # Pad text to fit into the grid
    return np.array(list(padded_text)).reshape(grid.shape)
