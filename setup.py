from setuptools import setup, find_packages

setup(
    name="Hexagonal-Permutation-Cipher",  # Full package name
    version="1.0.0",  # Version of the package
    description="A tool for encrypting and decrypting text using a hexagonal permutation cipher combined with AES encryption.",
    author="Joseph Webster Colby",
    author_email="rwc.webster@gmail.com",
    url="https://github.com/00-python/Hexagonal-Permutation-Cipher",  # URL to your project's repository
    packages=find_packages(),
    install_requires=[
        # List of dependencies
        "numpy",
        "pycryptodome",
        "pygame",
        "pythreejs"
    ],
    entry_points={
        "console_scripts": [
            "hpc=hexagonal_permutation_cipher.__main__:main",  # Create a console script entry point for "hpc"
        ],
    },
    classifiers=[
        # See: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)