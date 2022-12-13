import functools
import json
import typing


def chunks(list_to_split, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i:i + chunk_size]


def compare(first, second):
    if isinstance(first, int) and isinstance(second, int):
        if first < second:
            return 1
        elif first == second:
            return 0
        else:
            return -1
    elif isinstance(first, list) and isinstance(second, list):
        for i in range(min(len(first), len(second))):
            compare_res = compare(first[i], second[i])
            if compare_res == 1:
                return 1
            elif compare_res == -1:
                return -1
        if len(first) < len(second):
            return 1
        elif len(first) > len(second):
            return -1
        else:
            return 0
    elif isinstance(first, int) and isinstance(second, list):
        return compare([first], second)
    else:
        return compare(first, [second])


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    result = 0
    for pair_ind, pair in enumerate(chunks(input_lines, 3)):
        first, second, _ = pair
        first = json.loads(first)
        second = json.loads(second)
        if compare(first, second) == 1:
            result += pair_ind + 1
    return result


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    data = [[2], [6]]
    for pair_ind, pair in enumerate(chunks(input_lines, 3)):
        first, second, _ = pair
        first = json.loads(first)
        second = json.loads(second)
        data.extend([first, second])
    data = sorted(data, key=functools.cmp_to_key(lambda a, b: compare(a, b)), reverse=True)
    result = 1
    for ind, i in enumerate(data):
        if i == [2]:
            result *= ind + 1
        elif i == [6]:
            result *= ind + 1
    return result


# noinspection PyBroadException
def read_file_lines(file_to_read: str, strip: bool = True) -> typing.List[str]:
    try:
        with open(file_to_read) as f:
            lines = f.readlines()
    except:
        return []
    if strip:
        lines = [i.strip() for i in lines]
    return lines.copy()


if __name__ == '__main__':
    files_to_run = [
        'sample.txt',
        'input.txt'
    ]
    for filename in files_to_run:
        file_content = read_file_lines(filename, strip=True)
        if len(file_content) == 0:
            print(f'nothing in file {filename}, skipping')
            continue
        print(f'part 1 for {filename}')
        print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print()
