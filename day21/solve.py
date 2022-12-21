import typing
import utils


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    result = 0
    memory = {}
    while 'root' not in memory:
        for i in input_lines:
            monkey, data = i.split(': ')
            if data.isdigit():
                data = int(data)
                memory[monkey] = data
            else:
                first, oper, second = data.split()
                if first in memory and second in memory:
                    if oper == '+':
                        memory[monkey] = memory[first] + memory[second]
                    elif oper == '-':
                        memory[monkey] = memory[first] - memory[second]
                    elif oper == '/':
                        memory[monkey] = memory[first] / memory[second]
                    elif oper == '*':
                        memory[monkey] = memory[first] * memory[second]
                    else:
                        print('weird', monkey, data)

    return memory['root']


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    result = 0
    return result


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
