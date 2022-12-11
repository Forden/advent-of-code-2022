import typing


def part_1(input_lines: typing.List[str]):
    result = 0
    return result


def part_2(input_lines: typing.List[str]):
    result = 0
    return result


def read_file_lines(filename: str, strip: bool = True) -> typing.List[str]:
    with open(filename) as f:
        lines = f.readlines()
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
        if not file_content:
            print(f'nothing in file {filename}, skipping')
        print(f'part 1 for {filename}')
        print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print()
