import typing

import utils


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    min_x, max_x, max_y = 100000, 0, 0
    for path in input_lines:
        for pair in utils.sliding_window(
                list(map(lambda x: (int(x[0]), int(x[1])), map(lambda x: tuple(x.split(',')), path.split(' -> ')))),
                2,
                1
        ):
            if len(pair) == 1:
                continue
            for x, y in pair:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    min_x -= 1
    offset_x = min_x
    grid = [['.' for _ in range(max_x - offset_x)] for _ in range(max_y + 1)]
    for path in input_lines:
        for pair in utils.sliding_window(
                list(map(lambda x: (int(x[0]), int(x[1])), map(lambda x: tuple(x.split(',')), path.split(' -> ')))),
                2,
                1
        ):
            if len(pair) == 1:
                continue
            if pair[0][0] == pair[1][0]:
                if pair[0][1] <= pair[1][1]:
                    for i in range(pair[0][1], pair[1][1]):
                        grid[i][pair[0][0] - offset_x - 1] = '#'
                        pass
                elif pair[0][1] >= pair[1][1]:
                    for i in range(pair[1][1], pair[0][1]):
                        grid[i][pair[0][0] - offset_x - 1] = '#'
            elif pair[0][0] >= pair[1][0]:
                for i in range(pair[1][0], pair[0][0] + 1):
                    grid[pair[0][1]][i - offset_x - 1] = '#'
            elif pair[0][0] < pair[1][0]:
                for i in range(pair[0][0], pair[1][0] + 1):
                    grid[pair[0][1]][i - offset_x - 1] = '#'
            else:
                print(f'weird {pair}')
    sand_pos = (500, 0)
    grid[0][500 - offset_x - 1] = '+'
    # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    resting_count = 0
    while sand_pos != (-1, -1):
        if sand_pos[1] >= max_y:
            break
        # print(sand_pos)
        if grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] == '.':
            grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] = '+'
            grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
            sand_pos = (sand_pos[0], sand_pos[1] + 1)
        elif grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] in ['o', '#']:
            if grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 2] == '.':
                grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 2] = '+'
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
            elif grid[sand_pos[1] + 1][sand_pos[0] - offset_x] == '.':
                grid[sand_pos[1] + 1][sand_pos[0] - offset_x] = '+'
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
            else:
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = 'o'
                resting_count += 1
                sand_pos = (-1, -1)
        if (sand_pos == (-1, -1)) and (resting_count <= 10000):
            grid[0][500 - offset_x - 1] = '+'
            sand_pos = (500, 0)
        # print()
        # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    return resting_count


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    min_x, max_x, max_y = 100000, 0, 0
    for path in input_lines:
        for pair in utils.sliding_window(
                list(map(lambda x: (int(x[0]), int(x[1])), map(lambda x: tuple(x.split(',')), path.split(' -> ')))),
                2,
                1
        ):
            if len(pair) == 1:
                continue
            for x, y in pair:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    max_y += 3
    min_x -= 301
    max_x += 300
    offset_x = min_x
    grid = [['.' for _ in range(max_x - offset_x)] for _ in range(max_y - 1)]
    grid.append(['#' for _ in range(max_x - offset_x)])
    for path in input_lines:
        for pair in utils.sliding_window(
                list(map(lambda x: (int(x[0]), int(x[1])), map(lambda x: tuple(x.split(',')), path.split(' -> ')))),
                2,
                1
        ):
            if len(pair) == 1:
                continue
            if pair[0][0] == pair[1][0]:
                if pair[0][1] <= pair[1][1]:
                    for i in range(pair[0][1], pair[1][1]):
                        grid[i][pair[0][0] - offset_x - 1] = '#'
                        pass
                elif pair[0][1] >= pair[1][1]:
                    for i in range(pair[1][1], pair[0][1]):
                        grid[i][pair[0][0] - offset_x - 1] = '#'
            elif pair[0][0] >= pair[1][0]:
                for i in range(pair[1][0], pair[0][0] + 1):
                    grid[pair[0][1]][i - offset_x - 1] = '#'
            elif pair[0][0] < pair[1][0]:
                for i in range(pair[0][0], pair[1][0] + 1):
                    grid[pair[0][1]][i - offset_x - 1] = '#'
            else:
                print(f'weird {pair}')
    sand_pos = (500, 0)
    # print(f'before, {sand_pos}')
    grid[0][500 - offset_x - 1] = '+'
    # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    resting_count = 0
    while sand_pos != (-1, -1):
        # time.sleep(.05)
        # for y, _ in enumerate(grid):
        #     for x, _ in enumerate(grid[y]):
        #         if grid[y][x] == '+':
        #             sand_pos = (x + offset_x + 1, y)
        if sand_pos[1] >= max_y:
            break
        # print(
        #     f'before, {sand_pos=}, [{sand_pos[1] + 1=}, {sand_pos[0] - offset_x - 1=}] [{grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1]=}]'
        # )
        if grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] == '.':
            grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] = '+'
            grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
            sand_pos = (sand_pos[0], sand_pos[1] + 1)
        elif grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 1] in ['o', '#']:
            if grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 2] == '.':
                grid[sand_pos[1] + 1][sand_pos[0] - offset_x - 2] = '+'
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
                sand_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
            elif grid[sand_pos[1] + 1][sand_pos[0] - offset_x] == '.':
                grid[sand_pos[1] + 1][sand_pos[0] - offset_x] = '+'
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = '.'
                sand_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
            else:
                grid[sand_pos[1]][sand_pos[0] - offset_x - 1] = 'o'
                resting_count += 1
                sand_pos = (-1, -1)
        else:
            print(f'weird {sand_pos}')
        # print(f'after, {sand_pos}')
        if (
                sand_pos == (-1, -1)
        ) and (
                resting_count <= 1000000
        ) and (
                grid[0][500 - offset_x - 1] != 'o'
        ):
            grid[0][500 - offset_x - 1] = '+'
            sand_pos = (500, 0)
            # if resting_count % 250 == 0:
            #     print()
            #     print(*[''.join(map(str, i)) for i in grid], sep='\n')
        # print()
        # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    # print()
    # print(*[''.join(map(str, i)) for i in grid], sep='\n')
    return resting_count


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
