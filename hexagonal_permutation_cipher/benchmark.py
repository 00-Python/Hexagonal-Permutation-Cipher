import time
import statistics
from .encryption import encrypt, decrypt

def benchmark():
    """
    Run benchmark tests for encryption and decryption.
    """
    test_cases = [
        ("Short text", "ShortKey"),
        ("This is a longer unique and even longer test!", "MediumKey"),
        ("This is a much longer text to test the performance of the encryption and decryption algorithms over a significant amount of data.", "AnotherKey"),
        (" " * 1000, "LongKeyInfiniteText"),
    ]

    for plain_text, key in test_cases:
        encryption_times = []
        decryption_times = []

        for _ in range(10):  # Run each test case 10 times
            start_time = time.time()
            encrypted_text = encrypt(plain_text, key)
            encryption_times.append(time.time() - start_time)

            start_time = time.time()
            decrypted_text = decrypt(encrypted_text, key)
            decryption_times.append(time.time() - start_time)

            if plain_text != decrypted_text:
                print(f"Original: {plain_text}")
                print(f"Decrypted: {decrypted_text}")
                raise ValueError("Decryption failed, original and decrypted text do not match.")

        avg_encryption_time = statistics.mean(encryption_times)
        avg_decryption_time = statistics.mean(decryption_times)

        print(f"Test case: {plain_text[:30]}... with key {key}")
        print(f"  Average encryption time: {avg_encryption_time:.6f} seconds")
        print(f"  Average decryption time: {avg_decryption_time:.6f} seconds")