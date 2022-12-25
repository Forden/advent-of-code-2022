import typing


def parse_commands(commands: str) -> typing.List[typing.Union[int, str]]:
    cmds = []
    while 'R' in commands or 'L' in commands:
        for ind, i in enumerate(commands):
            if i == 'R':
                # print(commands[:ind - 1])
                if commands[:ind]:
                    cmds.append(int(commands[:ind]))
                cmds.append('R')
                commands = commands[ind + 1:]
                break
            elif i == 'L':
                if commands[:ind]:
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
        s = f'{y + 1:<3} {"".join(map(lambda x: x if x else " ", row))}'
        if visited is not None:
            s = list(s)
            for i in list(reversed(list(reversed(visited))[:100000000000000])):
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
    print(f'position: {current}')
    pass


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
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
    visited = [current_position]
    for cmd in cmds:
        if isinstance(cmd, str):
            if cmd == 'R':
                current_position[2] -= 90
            elif cmd == 'L':
                current_position[2] += 90
            current_position[2] %= 360
        else:
            for cur_step in range(cmd):
                possible, next_position = get_next_position(grid, current_position, '+')
                assert current_position != next_position, (
                    current_position, next_position, print_grid(grid, current_position, visited)
                )
                if possible:
                    current_position = [*next_position]
                    visited.append(current_position)
                else:
                    break
    print(current_position)
    return (current_position[0] + 1) * 4 + (current_position[1] + 1) * 1000 + current_position[2] // 90


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_sector_by_coord(x: int, y: int) -> int:
        terms = [
            all(
                [
                    50 <= x <= 99, 0 <= y <= 49
                ]
            ),
            all(
                [
                    100 <= x <= 149, 0 <= y <= 49
                ]
            ),
            all(
                [
                    50 <= x <= 99, 50 <= y <= 99
                ]
            ),
            all(
                [
                    50 <= x <= 99, 100 <= y <= 149
                ]
            ),
            all(
                [
                    0 <= x <= 49, 100 <= y <= 149
                ]
            ),
            all(
                [
                    0 <= x <= 49, 150 <= y <= 199
                ]
            ),
        ]
        if x == -1:
            print(123, x, y)
        # assert x >= 0 or y >= 0, (x, y)
        return terms.index(True) + 1 if True in terms else -1

    def get_next_position(
            grid: typing.List[typing.List[typing.Optional[str]]],
            current: typing.List[int],
            command: str
    ) -> typing.Tuple[bool, typing.List[int]]:
        result = [*current]
        current_sector = get_sector_by_coord(current[0], current[1])
        if command in ['R', 'L']:
            if command == 'R':
                result[2] -= 90
            else:
                result[2] += 90
            result[2] %= 360
        else:
            if result[1] == 149:
                print(result, current_sector)
            if result[2] == 0:
                if current_sector == 1:
                    if grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 2:
                    if result[0] + 1 == len(grid[0]):
                        if grid[149 - result[1]][99] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 99
                            result[1] = 149 - result[1]
                            result[2] = 180
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 3:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[49][100 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 100 + result[1] % 50
                            result[1] = 49
                            result[2] = 90
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 4:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[49 - result[1] % 50][149] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 149
                            result[1] = 49 - result[1] % 50
                            result[2] = 180
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 5:
                    if grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[149][50 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 50 + result[1] % 50
                            result[1] = 149
                            result[2] = 90
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
            elif result[2] == 90:
                if current_sector == 1:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[150 + result[0] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[1] = 150 + result[0] % 50
                            result[0] = 0
                            result[2] = 0
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 2:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[199][result[0] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = result[0] % 50
                            result[1] = 199
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 3:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 4:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 5:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[50 + result[0] % 50][50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[1] = 50 + result[0] % 50
                            result[0] = 50
                            result[2] = 0
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 6:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
            elif result[2] == 180:
                if current_sector == 1:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[149 - result[1] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 0
                            result[1] = 149 - result[1] % 50
                            result[0] = 0
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 2:
                    if grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 3:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[100][result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 270
                            result[0] = result[1] % 50
                            result[1] = 100
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 4:
                    if grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 5:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[49 - result[1] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 0
                            result[1] = 49 - result[1] % 50
                            result[0] = 50
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[0][49 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 270
                            result[0] = 50 + result[1] % 50
                            result[1] = 0
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                else:
                    print('weird sector', current_sector, result)
            elif result[2] == 270:
                if current_sector == 1:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 2:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[50 + result[0] % 50][99] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 180
                            result[1] = 50 + result[0] % 50
                            result[0] = 99
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 3:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 4:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[150 + result[0] % 50][49] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 180
                            result[1] = 150 + result[0] % 50
                            result[0] = 49
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 5:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[0][100 + result[0] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 100 + result[0] % 50
                            result[1] = 0
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
        # print(f'{current_position=} {result=} {cmd=}')
        new_sector = get_sector_by_coord(result[0], result[1])
        assert new_sector != -1, (current, current_sector, result, new_sector)
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
    # current_position = [100, 0, 0]
    visited = [current_position]
    for cmd in cmds:
        if isinstance(cmd, str):
            if cmd == 'R':
                current_position[2] -= 90
            elif cmd == 'L':
                current_position[2] += 90
            current_position[2] %= 360
        else:
            for cur_step in range(cmd):
                # time.sleep(.01)
                possible, next_position = get_next_position(grid, current_position, '+')
                assert current_position != next_position, (
                    current_position, next_position, possible, print_grid(grid, current_position, visited)
                )
                if possible:
                    current_position = [*next_position]
                    visited.append(current_position)
                    # print_grid(grid, current_position, visited)
                else:
                    break
    print_grid(grid, current_position, visited)
    print(current_position)
    print(get_sector_by_coord(current_position[0], current_position[1]))
    return (current_position[0] + 1) * 4 + (current_position[1] + 1) * 1000 + current_position[2] // 90


def test_2(input_lines: typing.List[str]):
    def get_sector_by_coord(x: int, y: int) -> int:
        terms = [
            all(
                [
                    50 <= x <= 99, 0 <= y <= 49
                ]
            ),
            all(
                [
                    100 <= x <= 149, 0 <= y <= 49
                ]
            ),
            all(
                [
                    50 <= x <= 99, 50 <= y <= 99
                ]
            ),
            all(
                [
                    50 <= x <= 99, 100 <= y <= 149
                ]
            ),
            all(
                [
                    0 <= x <= 49, 100 <= y <= 149
                ]
            ),
            all(
                [
                    0 <= x <= 49, 150 <= y <= 199
                ]
            ),
        ]
        if x == -1:
            print(123, x, y)
        # assert x >= 0 or y >= 0, (x, y)
        return terms.index(True) + 1 if True in terms else -1
        pass

    def get_next_position(
            grid: typing.List[typing.List[typing.Optional[str]]],
            current: typing.List[int],
            command: str
    ) -> typing.Tuple[bool, typing.List[int]]:
        result = [*current]
        current_sector = get_sector_by_coord(current[0], current[1])
        if command in ['R', 'L']:
            if command == 'R':
                result[2] -= 90
            else:
                result[2] += 90
            result[2] %= 360
        else:
            if result[1] == 149:
                print(result, current_sector)
            if result[2] == 0:
                if current_sector == 1:
                    if grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 2:
                    if result[0] + 1 == len(grid[0]):
                        if grid[149 - result[1]][99] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 99
                            result[1] = 149 - result[1]
                            result[2] = 180
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 3:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[49][100 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 100 + result[1] % 50
                            result[1] = 49
                            result[2] = 90
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 4:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[49 - result[1] % 50][149] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 149
                            result[1] = 49 - result[1] % 50
                            result[2] = 180
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 5:
                    if grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0] + 1, result[1]) == -1:
                        if grid[149][50 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 50 + result[1] % 50
                            result[1] = 149
                            result[2] = 90
                    elif grid[result[1]][result[0] + 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] += 1
            elif result[2] == 90:
                if current_sector == 1:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[150 + result[0] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[1] = 150 + result[0] % 50
                            result[0] = 0
                            result[2] = 0
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 2:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[199][result[0] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = result[0] % 50
                            result[1] = 199
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 3:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 4:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 5:
                    if get_sector_by_coord(result[0], result[1] - 1) == -1:
                        if grid[50 + result[0] % 50][50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[1] = 50 + result[0] % 50
                            result[0] = 50
                            result[2] = 0
                    elif grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
                elif current_sector == 6:
                    if grid[result[1] - 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] -= 1
            elif result[2] == 180:
                if current_sector == 1:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[149 - result[1] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 0
                            result[1] = 149 - result[1] % 50
                            result[0] = 0
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 2:
                    if grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 3:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[100][result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 270
                            result[0] = result[1] % 50
                            result[1] = 100
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 4:
                    if grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 5:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[49 - result[1] % 50][0] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 0
                            result[1] = 49 - result[1] % 50
                            result[0] = 50
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0] - 1, result[1]) == -1:
                        if grid[0][49 + result[1] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 270
                            result[0] = 50 + result[1] % 50
                            result[1] = 0
                    elif grid[result[1]][result[0] - 1] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[0] -= 1
                else:
                    print('weird sector', current_sector, result)
            elif result[2] == 270:
                if current_sector == 1:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 2:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[50 + result[0] % 50][99] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 180
                            result[1] = 50 + result[0] % 50
                            result[0] = 99
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 3:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 4:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[150 + result[0] % 50][49] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[2] = 180
                            result[1] = 150 + result[0] % 50
                            result[0] = 49
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 5:
                    if grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
                elif current_sector == 6:
                    if get_sector_by_coord(result[0], result[1] + 1) == -1:
                        if grid[0][100 + result[0] % 50] == '#':
                            return False, [-1, -1, -1]
                        else:
                            result[0] = 100 + result[0] % 50
                            result[1] = 0
                    elif grid[result[1] + 1][result[0]] == '#':
                        return False, [-1, -1, -1]
                    else:
                        result[1] += 1
        # print(f'{current_position=} {result=} {cmd=}')
        new_sector = get_sector_by_coord(result[0], result[1])
        assert new_sector != -1, (current, current_sector, result, new_sector)
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
    inverse_directions = {
        0:   180,
        90:  270,
        180: 0,
        270: 90
    }
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is None:
                continue
            start_sector = get_sector_by_coord(x, y)
            for test_direction in inverse_directions.keys():
                test_loc = [x, y, test_direction]
                print(test_loc)
                _, new_position = get_next_position(grid, test_loc, '+')
                new_sector = get_sector_by_coord(new_position[0], new_position[1])
                if start_sector == new_sector:
                    new_direction = inverse_directions[test_direction]
                else:
                    if start_sector == 1:
                        if new_sector == 6:
                            new_direction = 180
                        elif new_sector == 2:
                            new_direction = 180
                        elif new_sector == 5:
                            new_direction = 180
                        elif new_sector == 3:
                            new_direction = 90
                    elif start_sector == 2:
                        new_direction = {
                            6: 270,
                            1: 0,
                            4: 0,
                            3: 0
                        }[new_sector]
                    elif start_sector == 3:
                        new_direction = {
                            1: 270,
                            2: 270,
                            4: 90,
                            5: 90
                        }[new_sector]
                    elif start_sector == 4:
                        new_direction = {
                            3: 270,
                            5: 0,
                            2: 0,
                            6: 0
                        }[new_sector]
                    elif start_sector == 5:
                        new_direction = {
                            4: 180,
                            3: 180,
                            6: 90,
                            1: 180
                        }[new_sector]
                    elif start_sector == 6:
                        new_direction = {
                            5: 270,
                            4: 270,
                            1: 90,
                            2: 90
                        }[new_sector]
                    else:
                        print('unsorrtper')
                print(new_position)
                inverse_loc = [new_position[0], new_position[1], new_direction]
                _, inverse_new_position = get_next_position(grid, inverse_loc, '+')
                inverse_new_location_sector = get_sector_by_coord(inverse_new_position[0], inverse_new_position[1])
                print(
                    f'start pos: {test_loc} (sector {start_sector}) got {new_position} (sector {new_sector}) inverse direction {inverse_loc} got {inverse_new_position} (sector {inverse_new_location_sector})'
                )
                assert (
                        (
                                inverse_new_position[0] == test_loc[0]
                        ) and (
                                inverse_new_position[1] == test_loc[1]
                        ) and (
                            True  # inverse_new_position[2] == inverse_directions[test_loc[2]]
                        )
                ), (
                    test_loc, new_position, inverse_loc, inverse_new_position
                )


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
        'input.txt'
        # 'test_input.txt'
    ]
    for filename in files_to_run:
        file_content = read_file_lines(filename, strip=True)
        if len(file_content) == 0:
            print(f'nothing in file {filename}, skipping')
            continue
        # print(f'part 1 for {filename}')
        # print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        # print(test_2(file_content.copy()))
        print()
