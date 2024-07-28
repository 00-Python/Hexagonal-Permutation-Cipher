import numpy as np
from pythreejs import *
from IPython.display import display
import hashlib
from .grid import Matrix
from .utils import permute_grid

def coords_to_hex(x, y, z, size):
    """
    Convert cube coordinates to 3D hexagonal grid coordinates.
    """
    return [(x * size * 3/2, (y - z) * size * np.sqrt(3)/2, 0)]

def create_3d_grid(size, hex_size):
    """
    Create a 3D hexagonal grid as a list of meshes.
    """
    hexagons = []

    for x in range(-size, size + 1):
        for y in range(-size, size + 1):
            for z in range(-size, size + 1):
                if x + y + z == 0:
                    hex_pos = coords_to_hex(x, y, z, hex_size)
                    hex_geometry = CircleGeometry(radius=hex_size, radiusTop=1, radiusBottom=1, height=1, radialSegments=6)
                    hex_color = 'green'
                    hex_material = MeshLambertMaterial(color=hex_color)
                    hexagon = Mesh(geometry=hex_geometry, material=hex_material, position=hex_pos)
                    hexagons.append(hexagon)

    return hexagons

def permute_3d_grid(grid, key, size):
    """
    Permute the hexagonal grid using a key in 3D.
    """
    # Convert grid to a 2D numpy array
    matrix = Matrix(grid)
    flat_grid = matrix.flat
    permuted_grid = permute_grid(flat_grid, key)

    permuted_3d_grid = np.array(permuted_grid).reshape((size, size, size)).tolist()

    return permuted_3d_grid

def animate_permutation_3d(size=3, key="mysecretkey"):
    """
    Animate the 3D permutation process of a hexagonal grid using pythreejs.
    """
    # Convert the key to bytes and create a random number generator
    aes_key = hashlib.sha256(key.encode()).digest()

    # Create the 3D grid
    hex_size = 0.5
    grid = create_3d_grid(size, hex_size)

    # Create scene and add hexagons
    scene = Scene(children=[
        Mesh(geometry=PlaneGeometry(1000, 1000), material=MeshBasicMaterial(color='lightblue'), position=[0, 0, -0.01]),
        AmbientLight(color='#777777')
    ] + grid)

    # Setup camera
    camera = PerspectiveCamera(position=[0, 5, 10], up=[0, 0, 1], children=[
        DirectionalLight(color='white', position=[3, 5, 1], intensity=0.6)
    ])
    camera.lookAt([0, 0, 0])

    # Renderer
    renderer = Renderer(camera=camera, scene=scene, controls=[OrbitControls(controlling=camera)], width=800, height=600)

    # Display the 3D grid
    display(renderer)

    permuted_grid = permute_3d_grid(grid, aes_key, size)

    for hexagon, pos in zip(grid, permuted_grid):
        # Animate individual hexagons to their new permuted positions
        hexagon.position = coords_to_hex(*pos, hex_size)

        # Refresh the renderer
        renderer.render()

# Main function to start the visualization process
if __name__ == "__main__":
    key = "mysecretkey"
    animate_permutation_3d(size=3, key=key)
