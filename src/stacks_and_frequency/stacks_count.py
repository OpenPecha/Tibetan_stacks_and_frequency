from botok.utils.unicode_normalization import normalize_unicode
from botok.utils.lenient_normalization import normalize_graphical
from botok.tokenizers.stacktokenizer import tokenize_in_stacks
from pathlib import Path
from stacks_and_frequency.filter_stacks import get_stacks_info, create_csv

stack_csv = {}
transcript_dir = "./data/transcripts"
freq_dir = "./data/frequency"

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
        if stack in stack_csv:
            stack_csv[stack] += 1
        else:
            stack_csv[stack] = 1
    return stack_csv


def get_stacks_csv(data_path):
    with open(data_path, "r") as f:
        data = f.read().splitlines()
        for row in data[2:]:
            image_name = row.split(",")[0]
            print(image_name)
            text = row.split(",")[-1]
            if text:
                stacks = get_tokenized_stacks(text)
                stack_csv = count_the_stacks(stacks)
    return stack_csv


def write_csv(filename, data):
    with open(filename, "w") as f:
        f.write("Stack, Frequency\n")
        for stack, frequency in data.items():
            f.write(f"{stack},{frequency}\n")


def main():
    csv_name = "LM_etexts.csv"
    transcript_dir = Path("./data/transcripts/")
    freq_dir = Path("./data/frequency/")
    
    data_path = transcript_dir / csv_name
    frequency_path = freq_dir / csv_name

    stack_csv = get_stacks_csv(data_path)
    write_csv(frequency_path, stack_csv)




if __name__ == "__main__":
    main()
