from pathlib import Path
import csv

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        stacks = list(reader)
    return stacks

def get_descending_sorted_dict(stack_dict):
    sorted_stack = {k: v for k, v in sorted(stack_dict.items(), key=lambda item: int(item[1]), reverse=True)}
    return sorted_stack

def get_all_stacks():
    stack_dict = {}
    curr_dict = {}
    stack_paths = list(Path("./data/valid_stacks/").iterdir())
    for stack_path in stack_paths:
        if stack_path.name in ['valid_lithang_kanjur.csv', 'valid_derge_tenjur.csv']:
            continue
        else:
            stacks_csv = read_csv(stack_path)
            for row in stacks_csv[1:]:
                stack = row[0]
                stack_count = row[1]
                if stack in stack_dict.keys():
                    prev_count = stack_dict[stack]
                    freq = str(int(prev_count) + int(stack_count))
                else:
                    freq = stack_count
                curr_dict = {
                    stack: freq
                }
                stack_dict.update(curr_dict)
                curr_dict.clear()
    sorted_stack = get_descending_sorted_dict(stack_dict)
    return sorted_stack


def write_csv(data, file_name):
    with open(f'data/{file_name}', 'w') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])


def main():
    all_stack = get_all_stacks()
    write_csv(all_stack, 'all_stacks.csv')


if __name__ == "__main__":
    main()