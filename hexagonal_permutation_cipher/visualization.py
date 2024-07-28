import numpy as np
import pygame
import math
import random
from typing import Tuple
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

def hex_coord(x: int, y: int, size: float) -> Tuple[float, float]:
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

def draw_hex(surface, x: int, y: int, size: float, facecolor: str, text: str, font):
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
        (xy[0] + size * math.cos(math.radians(angle)), xy[1] + size * math.sin(math.radians(angle)))
        for angle in range(30, 360, 60)
    ]
    pygame.draw.polygon(surface, facecolor, hexagon)
    # Render the text inside the hexagon
    text_surf = font.render(text, True, pygame.Color('green'))
    text_rect = text_surf.get_rect(center=xy)
    surface.blit(text_surf, text_rect)

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

def animate_permutation(grid: np.ndarray, key: bytes, width=800, height=600):
    """
    Animate the permutation process of the hexagonal grid.

    Args:
        grid (np.ndarray): The original hexagonal grid.
        key (bytes): The key used for permutation.
        width (int): The width of the Pygame window. Default is 800.
        height (int): The height of the Pygame window. Default is 600.
    """
    # Temporary StringIO objects to suppress the pygame message
    with StringIO() as f, redirect_stdout(f), redirect_stderr(f):  
        pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hexagonal Permutation Animation")

    # Load the retro monospaced/pixel font
    font = pygame.font.Font(pygame.font.match_font('monospace'), 24)
    size = 30

    flat_grid = grid.flatten()
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
        current_grid = np.full(grid_length, None)
        current_grid[current_indices] = flat_grid[current_indices]

        index = 0
        for y, row in enumerate(grid):
            for x, _ in enumerate(row):
                if current_grid[index] is not None:
                    draw_hex(screen, x, y, size, pygame.Color('darkgreen'), str(current_grid[index]), font)
                index += 1

        add_scanlines(screen)
        add_noise(screen)

        pygame.display.flip()
        clock.tick(30)  # Increase frame rate for smoother animation
        frame += 1

    pygame.quit()