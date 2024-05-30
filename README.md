# Ethereum Seed Phrase Recovery Bruteforcer

## Ethereum Wallet Recovery Tool

This Python script is designed to bruteforce Ethereum wallet addresses using partial seed phrases, checking against an address(es) within a text file (addresses.txt). It utilizes multiprocessing to increase efficiency.

### Features

- **Partial Seed Phrase Input**: Allows inputting parts of a seed phrase, with '?' as a placeholder for missing words.
- **Wordlist**: Loads a wordlist to fill in missing words and generate mnemonics.
- **Address Validation**: Validates generated addresses against a list of known Ethereum addresses.
- **Concurrency**: Utilizes multiprocessing to process combinations concurrently.
- **Progress Tracking**: Tracks progress with a visual display of tried mnemonic combinations.
- **Output**: Saves discovered wallet details to a file called `discovery.txt`.

### Dependencies

- Python 3.x
- `eth_account` library
- `eth_utils` library
- `multiprocessing` module

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/psionyx2311/Ethereum_Seed_Recovery_BF.git
    cd Ethereum_Seed_Recovery_BF
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt

    (pip3 for Linux)
    ```

### Usage

1. Input the number of CPU cores to use (0 for all available cores).
2. Enter the parts of the seed phrase one at a time, using '?' for missing words.
3. The script will check for matches against known Ethereum addresses.
4. If a match is found, wallet details will be saved to `discovery.txt`.

### Configuration

- `words.txt`: File containing the wordlist for filling placeholders.
- `addresses.txt`: File containing known Ethereum addresses for validation.
- `discovery.txt`: File matching key info is saved to.

### Note

- This script is for educational purposes only. Use responsibly and ethically.
- Due to the vast number of possible combinations, running this script may take a considerable amount of time.

### License

This project is licensed under the GPL-3.0 license. See the `LICENSE` file for details.

### Contributions

Contributions are welcome! There is definaly much room for optimization, please share any knowledge you may have!
