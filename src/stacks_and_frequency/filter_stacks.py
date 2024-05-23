import re


CONSONANTS = '\u0F40-\u0F6C'
VOWELS = '\u0F71-\u0F7E'
SUBSCRIPTS = '\u0F90-\u0FB8'
TSHEG = '\u0F0B'
INVALID_PRECEDING = '\u0F00-\u0F3F\u0F70\u0F7F-\u0F8F\u0FBE-\u0FFF'  # Define invalid preceding characters range

# Updated regex pattern
pattern = rf'''
^
(
    (
        [{CONSONANTS}]([{VOWELS}{SUBSCRIPTS}]*[{VOWELS}{SUBSCRIPTS}])*  # Valid consonant followed by vowels or subscripts
    )|
    (
        {TSHEG}                   # Stack with only the character "་"
    )
)*
$

| # Start another set of rules to match valid sequences

(
    (
        [{CONSONANTS}]
        (
            [{VOWELS}]*
            [{SUBSCRIPTS}]*
            [{VOWELS}]*
        )
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
    stacks_sorted = sorted(stacks, key=lambda x: int(x[1]), reverse=True)
    
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("Stack, Frequency\n")
        for stack, frequency in stacks_sorted:
            f.write(f"{stack},{frequency}\n")


def main():
    invalid_stacks = []
    valid_stacks = []
    csv_file = "./data/stack_freq/norbu.csv"
    with open(csv_file, "r") as f:
        data = f.read().splitlines()
        for row in data[1:]:
            text = row.split(",")
            stack = text[0]
            freq = text[1].replace(" ", "")
            if is_valid_tibetan(stack):
                valid_stacks.append([stack,freq])
            else:
                invalid_stacks.append([stack,freq])
    create_csv("./data/filtered_stack_freq/norbuketaka.csv", valid_stacks)
    # create_csv("./filtered_stack_freq/invalid_stacks.csv", invalid_stacks)
    

if __name__ == "__main__":
    main()