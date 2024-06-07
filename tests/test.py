import io
import csv
from pathlib import Path
from stacks_and_frequency.filter_stacks import get_stacks_info, create_csv
from stacks_and_frequency.stacks_count import get_tokenized_stacks, count_the_stacks


def read_csv_file(file_path):
    with open(file_path, "r") as f:
        data = f.read().splitlines()
    return data

expected_valid_stacks = read_csv_file(Path("./tests/data/filtered_stack_freq/expected_valid_stacks.csv"))
expected_invalid_stacks = read_csv_file(Path(__file__).parent / "data/filtered_stack_freq/expected_invalid_stacks.csv")
expected_stacks_count = read_csv_file(Path(__file__).parent / "data/frequency/expected_stacks.csv")


def test_stacks_count():
    stack_csv = []
    text = "པོ་ཡིད་དགའ་ཞིང་ཡིད་དགའ་ནས། རོ་སྟོད་བསྲང་སྟེ་ལག་པ་གཡས་པ་བརྐྱང་ནས། བདག་གི་ཡུལ་ན་སྨྲ་བའི་ཁྱུ་མཆོག་འདི་ལྟ་བུ་དག་ཡོད་པ་ནི་བདག་གིས་རྙེད་པ་ལེགས་པར་རྙེད་དོ་ཞེས་ཆེད་དུ་བརྗོད་པ་ཆེད་དུ་"
    stacks = get_tokenized_stacks(text)
    stack_dict = count_the_stacks(stacks)
    for stack, frequency in stack_dict.items():
        stack_csv.append([stack, frequency])
    assert len(stack_csv) == len(expected_stacks_count)
    


def test_filter_stacks():
    valid_stacks, invalid_stacks = get_stacks_info(expected_stacks_count)
    create_csv(Path(__file__).parent /'expected_valid_stacks.csv', valid_stacks)
    assert len(valid_stacks) == len(expected_valid_stacks)
    assert len(invalid_stacks) == len(expected_invalid_stacks)

