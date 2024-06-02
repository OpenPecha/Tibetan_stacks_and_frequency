import re
from pathlib import Path


# Tibetan character ranges
CONSONANTS = '\u0F40-\u0F6C'  # ཀ-ཌ, ཎ-ཱ, ི-ུ, ཱུ-ཹ, ེ-ཻ, ོ-ཽ, ཾ-ཿ
VOWELS = '\u0F71-\u0F7E'  # ཱ, ི, ུ, ཱུ, ྲྀ, ཷ, ླྀ, ཹ, ེ, ཻ, ོ, ཽ, ཾ, ཿ
SUBSCRIPTS = '\u0F90-\u0FB8'  # ྐ-ྸ, ླ-ྼ, ྾-྿

NUMBERS = '\u0F20-\u0F33'  # ༠-༳

# Standalone characters broken into ranges and named
MARKS_INITIAL = '\u0F04-\u0F12'  # ༄-༒
MARKS_CLOSING = '\u0F13-\u0F17'  # ༓-༗
MARKS_SECONDARY = '\u0F1A-\u0F34'  # ༚-༴
MARKS_ENCLOSING = '\u0F3A-\u0F3D'  # ༺-༽
MARKS_EXTRA = '\u0FBE-\u0FDA'  # ༾-༚

# Combine all standalone symbols
STANDALONE_SYMBOLS = f'{MARKS_INITIAL}{MARKS_CLOSING}{MARKS_SECONDARY}{MARKS_ENCLOSING}{MARKS_EXTRA}{NUMBERS}'

# Special symbols
SYLLABLES_AND_MARKS = '\u0F00-\u0F03'  # ༀ-༃
MARKS_CARET_AND_OTHERS = '\u0F35-\u0F39'  # ༵-༹
SIGN_RNAM_BCAD = '\u0F7F-\u0F80'  # ཿ-ྀ
MARKS_PALUTA_AND_OTHERS = '\u0F85-\u0F8B'  # ྅-ྋ
SHAD_CHARACTERS = '\u0F08\u0F0C\u0F0D\u0F0E\u0F0F\u0F11\u0F14\u0F15\u0F16\u0F17'  # ༈, ༌, །, ༎, ༏, ༐, ༑, ༒, ༓, ༔, ༕, ༖, ༗

# Combine all special symbols and shad characters
SPECIAL_SYMBOLS = f'{SYLLABLES_AND_MARKS}{MARKS_CARET_AND_OTHERS}{SIGN_RNAM_BCAD}{MARKS_PALUTA_AND_OTHERS}{SHAD_CHARACTERS}'

pattern = rf'''
^
(
    (
        [{CONSONANTS}]([{VOWELS}{SUBSCRIPTS}]*)  # Valid consonant followed by vowels or subscripts
    )|
    (
        [{STANDALONE_SYMBOLS}{NUMBERS}{SPECIAL_SYMBOLS}]                    # Standalone characters, numbers, or special symbols alone
    )
)*
$
'''


def is_valid_tibetan(stack):
    """
    Check if the given Tibetan stack is valid based on defined constraints.
    """
    if re.fullmatch(pattern, stack, re.VERBOSE):
        return True
    else:
        return False
    

def create_csv(csv_path, stacks):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    stacks_sorted = sorted(stacks, key=lambda x: int(x[1]), reverse=True)
    
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("Stack, Frequency\n")
        for stack, frequency in stacks_sorted:
            f.write(f"{stack},{frequency}\n")


def get_stacks_info(data):
    invalid_stacks = []
    valid_stacks = []
    for row in data[1:]:
        text = row.split(",")
        stack = text[0]
        freq = text[1].replace(" ", "")
        if is_valid_tibetan(stack):
            valid_stacks.append([stack,freq])
        else:
            invalid_stacks.append([stack,freq])
    return valid_stacks, invalid_stacks



def main():
    filename = "derge_tenjur.csv"
    freq_dir = Path("./data/frequency/")
    filtered_dir = Path("./data/filtered_stack_freq/")
    csv_file = freq_dir / filename
    with open(csv_file, "r") as f:
        data = f.read().splitlines()
    valid_stacks, invalid_stacks = get_stacks_info(data)
    create_csv(filtered_dir / f"valid_{filename}", valid_stacks)
    create_csv(filtered_dir / f"invalid_{filename}", invalid_stacks)



if __name__ == "__main__":
    main()