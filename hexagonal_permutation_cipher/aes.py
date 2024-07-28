from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import concurrent.futures

# Constants for AES encryption
AES_BLOCK_SIZE = 16

def encrypt_aes_block(data: bytes, key: bytes) -> bytes:
    """
    Encrypt a block of data using AES encryption (CBC mode).
    
    Args:
        data (bytes): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted data with IV prepended.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data, AES_BLOCK_SIZE))
    return cipher.iv + encrypted_data

def decrypt_aes_block(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt a block of AES-encrypted data (CBC mode).
    
    Args:
        encrypted_data (bytes): The encrypted data (IV followed by ciphertext).
        key (bytes): The decryption key.

    Returns:
        bytes: The decrypted data.
    """
    iv = encrypted_data[:AES_BLOCK_SIZE]
    encrypted_part = encrypted_data[AES_BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_part), AES_BLOCK_SIZE)

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data using AES encryption (CBC mode) with parallelization.

    Args:
        data (bytes): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The IV followed by the encrypted data.
    """
    # Split data into chunks
    chunk_size = AES_BLOCK_SIZE * 16  # Each chunk keeping consistent with block size
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        encrypted_chunks = list(executor.map(encrypt_aes_block, chunks, [key] * len(chunks)))

    # Combine the IV and encrypted chunks
    return b''.join(encrypted_chunks)

def aes_decrypt(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt AES-encrypted data (CBC mode) with parallelization.

    Args:
        encrypted_data (bytes): The encrypted data (IV followed by ciphertext).
        key (bytes): The decryption key.

    Returns:
        bytes: The decrypted data.
    """
    # Split encrypted data into chunks with IV
    chunk_size = AES_BLOCK_SIZE * 17  # 16 bytes for IV + actual block size
    chunks = [encrypted_data[i:i + chunk_size] for i in range(0, len(encrypted_data), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        decrypted_chunks = list(executor.map(decrypt_aes_block, chunks, [key] * len(chunks)))

    return b''.join(decrypted_chunks)