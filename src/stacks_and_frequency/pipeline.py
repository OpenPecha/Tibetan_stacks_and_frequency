from botok.utils.unicode_normalization import normalize_unicode
from botok.utils.lenient_normalization import normalize_graphical
from botok.tokenizers.stacktokenizer import tokenize_in_stacks
from pathlib import Path

stack_dict = {}

def normalise_text(text):
    unicode_normalised = normalize_unicode(text)
    normalised_text = normalize_graphical(unicode_normalised)
    return normalised_text

def get_tokenized_stacks(text):
    normalised_text = normalise_text(text)
    stacks = tokenize_in_stacks(normalised_text)
    return stacks


def count_the_stacks(stacks):
    for stack in stacks:
        if stack in stack_dict:
            stack_dict[stack] += 1
        else:
            stack_dict[stack] = 1
    return stack_dict

def write_csv(filename):
    with open(filename, "w") as f:
        f.write("Stack, Frequency\n")
        for stack, frequency in stack_dict.items():
            f.write(f"{stack}, {frequency}\n")

def get_stacks_csv(data_path):
    with open(data_path, "r") as f:
        data = f.read().splitlines()
        for row in data[1:]:
            text = row.split(",")[-1]
            stacks = get_tokenized_stacks(text)
            count_the_stacks(stacks)


def main():
    data_paths = list(Path("./data/").iterdir())
    for data_path in data_paths:
        get_stacks_csv(data_path)
    write_csv(filename="google_books.csv")

if __name__ == "__main__":
    main()