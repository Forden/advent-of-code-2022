import time
import typing


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def parse_commands(commands: str) -> typing.List[typing.Union[int, str]]:
        cmds = []
        while 'R' in commands or 'L' in commands:
            for ind, i in enumerate(commands):
                if i == 'R':
                    # print(commands[:ind - 1])
                    cmds.append(int(commands[:ind]))
                    cmds.append('R')
                    commands = commands[ind + 1:]
                    break
                elif i == 'L':
                    cmds.append(int(commands[:ind]))
                    cmds.append('L')
                    commands = commands[ind + 1:]
                    break
        if commands:
            cmds.append(int(commands))
        return cmds

    def print_grid(
            grid: typing.List[typing.List[typing.Optional[str]]],
            current: typing.Optional[typing.List[int]] = None,
            visited: typing.Optional[typing.List[typing.List[int]]] = None
    ):
        res = []

        for div in reversed(range(len(str(len(grid[0]))))):
            s = '    '
            for i in range(len(grid[0])):
                s += ('  ' + str((i + 1)))[-(1 + div)]
            res.append(s)
        for y, row in enumerate(grid):
            s = f'{y + 1:<3} {"".join(map(lambda x: x if x else "+", row))}'
            if visited is not None and False:
                s = list(s)
                for i in visited:
                    if i[1] == y:
                        if i[2] == 0:
                            s[4 + i[0]] = '>'
                        elif i[2] == 90:
                            s[4 + i[0]] = '^'
                        elif i[2] == 180:
                            s[4 + i[0]] = '<'
                        elif i[2] == 270:
                            s[4 + i[0]] = 'v'

            s = ''.join(s)
            if current is not None:
                if current[1] == y:
                    s = list(s)
                    if current[2] == 0:
                        s[4 + current[0]] = '>'
                    elif current[2] == 90:
                        s[4 + current[0]] = '^'
                    elif current[2] == 180:
                        s[4 + current[0]] = '<'
                    elif current[2] == 270:
                        s[4 + current[0]] = 'v'
                    # s[4 + current[0]] = 'O'
                    s = ''.join(s)
            res.append(s)
        print('\n'.join(res))
        print(f'position: {current_position}')
        pass

    def get_next_position(
            grid: typing.List[typing.List[typing.Optional[str]]],
            current: typing.List[int],
            command: str
    ) -> typing.Tuple[bool, typing.List[int]]:
        result = [*current]
        if command in ['R', 'L']:
            if command == 'R':
                result[2] -= 90
            else:
                result[2] += 90
            result[2] %= 360
        else:
            if result[2] == 0:
                if result[0] + 1 == len(grid[0]):
                    first_empty_ind = grid[result[1]].index('.')
                    if first_empty_ind == 0 or grid[result[1]][first_empty_ind - 1] is None:
                        result[0] = first_empty_ind
                    else:
                        return False, [-1, -1, -1]
                elif grid[result[1]][result[0] + 1] is None:
                    first_empty_ind = grid[result[1]].index('.')
                    if first_empty_ind == 0 or grid[result[1]][first_empty_ind - 1] is None:
                        result[0] = first_empty_ind
                    else:
                        return False, [-1, -1, -1]
                elif grid[result[1]][result[0] + 1] == '#':
                    return False, [-1, -1, -1]
                else:
                    result[0] += 1
            elif result[2] == 180:
                if result[0] - 1 == -1:
                    first_dot_ind = len(grid[result[1]]) - 1 - grid[result[1]][::-1].index('.')
                    first_wall_ind = len(grid[result[1]]) - 1 - grid[result[1]][::-1].index('#')
                    if first_wall_ind > first_dot_ind:
                        return False, [-1, -1, -1]
                    else:
                        result[0] = first_dot_ind
                elif grid[result[1]][result[0] - 1] is None:
                    first_dot_ind = len(grid[result[1]]) - 1 - grid[result[1]][::-1].index('.')
                    first_wall_ind = len(grid[result[1]]) - 1 - grid[result[1]][::-1].index('#')
                    if first_wall_ind > first_dot_ind:
                        return False, [-1, -1, -1]
                    else:
                        result[0] = first_dot_ind
                elif grid[result[1]][result[0] - 1] == '#':
                    return False, [-1, -1, -1]
                else:
                    result[0] -= 1
            elif result[2] == 90:
                if result[1] - 1 == -1:
                    for y, row in enumerate(grid):
                        if row[result[0]] == '.':
                            result[1] = y
                elif grid[result[1] - 1][result[0]] is None:
                    for y, row in enumerate(grid):
                        if row[result[0]] == '.':
                            result[1] = y
                elif grid[result[1] - 1][result[0]] == '#':
                    return False, [-1, -1, -1]
                else:
                    result[1] -= 1
            elif result[2] == 270:
                if result[1] + 1 == len(grid):
                    for y, row in enumerate(grid):
                        if row[result[0]] == '#':
                            return False, [-1, -1, -1]
                        if row[result[0]] == '.':
                            result[1] = y
                            break
                elif grid[result[1] + 1][result[0]] is None:
                    for y, row in enumerate(grid):
                        if row[result[0]] == '#':
                            return False, [-1, -1, -1]
                        if row[result[0]] == '.':
                            result[1] = y
                            break
                elif grid[result[1] + 1][result[0]] == '#':
                    return False, [-1, -1, -1]
                else:
                    result[1] += 1
        # print(f'{current_position=} {result=} {cmd=}')
        return True, result

    cmds = parse_commands(input_lines[-1])

    grid_width = max(map(len, input_lines[:-2]))
    grid: typing.List[typing.List[typing.Optional[str]]] = [
        [
            None for _ in range(grid_width)
        ] for _ in range(
            len(input_lines[:-2])
        )
    ]
    for y, row in enumerate(input_lines[:-2]):
        for x, cell in enumerate(row):
            if cell in ['.', '#']:
                grid[y][x] = cell
    current_position = None
    for y, row in enumerate(input_lines[:-2]):
        if current_position is None:
            for x, cell in enumerate(row):
                if cell == '.':
                    current_position = [x, y, 0]
                    break
    # current_position = [grid[y].index('.'), 0, 0]
    # print(y, current_position)
    # print(f'end = ({current_position[1] + 1},{current_position[0] + 1})')
    visited = [current_position]
    # print_grid(grid, current_position)
    for cmd in cmds:
        # print(f'current {cmd=}')
        if isinstance(cmd, str):
            # next_position = get_next_position(grid, current_position, cmd)
            if cmd == 'R':
                current_position[2] -= 90
            elif cmd == 'L':
                current_position[2] += 90
            current_position[2] %= 360
            # print_grid(grid, current_position, visited)
        else:
            for cur_step in range(cmd):
                # time.sleep(.5)
                possible = True
                possible, next_position = get_next_position(grid, current_position, '+')
                # print(f'{possible=}')
                # print(f'{current_position=}, {next_position=}')
                # if next_position == current_position:
                #     possible = False
                assert current_position != next_position, (
                    current_position, next_position, print_grid(grid, current_position, visited)
                )
                # print_grid(grid, current_position, visited)
                # if grid[next_position[1]][next_position[0]] == '#':
                #     possible = False
                if possible:
                    current_position = [*next_position]
                    visited.append(current_position)
                    # print_grid(grid, current_position, visited)
                else:
                    break
        # print_grid(grid, current_position, visited)
        print(f'end = ({current_position[1] + 1},{current_position[0] + 1})')
        # print(
        #     f'{current_position=}, {next_position=}, {cur_step+1=}/{cmd=}, {grid[next_position[1]][next_position[0]]=}'
        # )
    print()
    print()
    print()
    print()
    print('last')
    print_grid(grid, current_position, visited)
    print((current_position[0] + 1), (current_position[1] + 1), current_position[2] // 90)
    return (current_position[0] + 1) * 4 + (current_position[1] + 1) * 1000 + current_position[2] // 90


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
        lines = [i.rstrip('\n') for i in lines]
    return lines.copy()


if __name__ == '__main__':
    files_to_run = [
        # 'sample.txt',
        'input.txt',
        # 'input2.txt'
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
