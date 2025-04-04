import sys

class InvalidCellLetterError(Exception):
    pass

def cell_to_num(cell_in_letters: str) -> int:
    number = 0
    for idx, letter in enumerate(reversed(cell_in_letters)):
        letter_to_num = ord(letter) - 64
        # letter value * 26^
        number += letter_to_num * pow(26, idx)
    
    return number - 1 # -1 for 0 indexing

if __name__  == "__main__":
    cell_in_letters = sys.argv[1] if len(sys.argv) else "A"

    print(cell_to_num(cell_in_letters.upper()))