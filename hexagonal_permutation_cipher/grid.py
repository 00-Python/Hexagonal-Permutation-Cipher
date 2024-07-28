import numpy as np
import math
from typing import Tuple


class Matrix:
    """
    A class used to represent and manipulate a matrix constructed from a hexagonal grid.

    Attributes:
    ----------
    grid : np.ndarray
        The hexagonal grid in a 2D numpy array representation.
    flat : np.ndarray
        The flattened version of the hexagonal grid.
    dimensions : tuple
        The dimensions (shape) of the hexagonal grid.

    Methods:
    -------
    to_2d(flat_list: np.ndarray) -> np.ndarray
        Reshape a flat list to match the original grid's shape.
    """

    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.flat = grid.flatten()
        self.dimensions = grid.shape

    def to_2d(self, flat_list: np.ndarray) -> np.ndarray:
        """
        Reshape a flat list to match the original grid's shape.

        Args:
            flat_list (np.ndarray): The flattened list of grid values.

        Returns:
            np.ndarray: The reshaped 2D array.
        """
        return flat_list.reshape(self.dimensions)

def create_hexagonal_grid(size: int) -> np.ndarray:
    """
    Create a hexagonal grid of integers with consistent row lengths.

    Args:
        size (int): The size (radius) of the grid.

    Returns:
        np.ndarray: The hexagonal grid in a 2D numpy array representation.
    """
    max_length = size * 3 - 2
    grid = np.zeros((2 * size - 1, max_length), dtype=int)
    i = 1

    for row in range(size):
        grid[row, :size + row] = np.arange(i, i + size + row)
        i += size + row

    for row in range(size - 1):
        grid[size + row, :2 * size - row - 2] = np.arange(i, i + 2 * size - row - 2)
        i += 2 * size - row - 2

    return grid

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