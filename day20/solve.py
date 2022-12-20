import collections
import typing


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    class Number:
        def __init__(self, n):
            self.n = n

    arrangement = collections.deque(map(Number, map(int, input_lines)))

    for i in list(arrangement):
        curr_position = arrangement.index(i)
        arrangement.rotate(-curr_position)
        arrangement.popleft()
        arrangement.rotate(-i.n)
        arrangement.insert(0, i)

    arrangement = list(map(lambda x: x.n, arrangement))

    return sum(arrangement[(arrangement.index(0) + i) % len(arrangement)] for i in [1000, 2000, 3000])


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
