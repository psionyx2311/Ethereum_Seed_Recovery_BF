import random
from itertools import product
from eth_account import Account
from eth_utils.exceptions import ValidationError
import multiprocessing
import os

def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [word.strip() for word in file]

def load_addresses(filename):
    with open(filename, 'r') as file:
        return [address.strip().lower() for address in file]

def generate_mnemonic(words):
    # Converts the list of words into a space-separated string
    mnemonic = ' '.join(words)
    return mnemonic

def fill_placeholders(words, wordlist):
    # Fill placeholders with all possible combinations of words from the wordlist
    indices = [i for i, word in enumerate(words) if word == '?']
    combinations = list(product(wordlist, repeat=len(indices)))
    filled_combinations = []

    for combo in combinations:
        temp_words = words[:]
        for idx, word in zip(indices, combo):
            temp_words[idx] = word
        filled_combinations.append(temp_words)

    return filled_combinations

def mnemonic_to_private_key(mnemonic):
    # Generates a private key from the mnemonic
    Account.enable_unaudited_hdwallet_features()
    private_key = Account.from_mnemonic(mnemonic)._private_key.hex()
    return private_key.lower()

def private_key_to_public_key(private_key):
    # Generates a public key from the private key
    public_key = Account.from_key(private_key).address
    return public_key.lower()

def save_discovery(mnemonic, private_key, public_key):
    # Save discovery details to file
    with open('discovery.txt', 'a') as file:  # Use 'a' to append instead of 'w' to overwrite
        file.write(f"Mnemonic: {mnemonic}\n")
        file.write(f"Private key: {private_key}\n")
        file.write(f"Public key: {public_key}\n")

def check_combinations(combinations, addresses, progress, total_combinations, lock):
    for combo in combinations:
        # Generate mnemonic
        mnemonic = generate_mnemonic(combo)

        try:
            # Generate private key
            private_key = mnemonic_to_private_key(mnemonic)

            # Generate public key
            public_key = private_key_to_public_key(private_key)

            # Check if the generated public key matches any in the file
            if public_key in addresses:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n\nMatch found!\n")
                print("Public key:", public_key)
                print("Mnemonic:", mnemonic)
                print("Private key:", private_key)
                print("Details saved to discovery.txt \nIf your finished feel free to close the window, or let the program continue if you have multiple addresses.")
                # Save discovery details to file
                save_discovery(mnemonic, private_key, public_key)
                return True
        except ValidationError:
            # Ignore the error and continue with the next combination
            pass
        finally:
            with lock:
                progress.value += 1
                print(f"{progress.value}/{total_combinations} mnemonic combinations tried.", end='\r')
    return False

if __name__ == '__main__':
    # Input number of cores
    os.system('cls' if os.name == 'nt' else 'clear')
    num_cores = int(input("Enter the number of CPU cores to use (0 for all available cores): "))
    if num_cores == 0:
        num_cores = multiprocessing.cpu_count()

    # Input 12 words
    words = []
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter the parts of the seed phrase that you have, one at a time and in exact order. Use '?' for missing words:")
    for i in range(12):
        word = input(f"Enter word {i+1}: ")
        words.append(word.lower())

    # Load wordlist
    wordlist = load_wordlist('words.txt')

    # Load public keys from file
    addresses = load_addresses('addresses.txt')

    # Calculate the number of possible combinations
    num_placeholders = words.count('?')
    total_combinations = 2048 ** num_placeholders
    print(f"\nTotal possible combinations: {total_combinations}")

    # Fill placeholders with all possible combinations
    filled_combinations = fill_placeholders(words, wordlist)

    # Split combinations into chunks for multiprocessing
    chunk_size = len(filled_combinations) // num_cores
    chunks = [filled_combinations[i:i + chunk_size] for i in range(0, len(filled_combinations), chunk_size)]

    manager = multiprocessing.Manager()
    progress = manager.Value('i', 0)
    lock = manager.Lock()

    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.starmap(check_combinations, [(chunk, addresses, progress, total_combinations, lock) for chunk in chunks])

    if not any(results):
        print("\nNo match found.")
