import typing

import utils


def get_figure_coords(figure_type: str, start_coord: typing.Tuple[int, int]) -> typing.List[typing.Tuple[int, int]]:
    if figure_type == '-':
        return [(start_coord[0] + i, start_coord[1]) for i in range(4)]
    elif figure_type == '+':
        return [
            (start_coord[0], start_coord[1]),
            (start_coord[0], start_coord[1] + 1),
            (start_coord[0] + 1, start_coord[1]),
            (start_coord[0], start_coord[1] - 1),
            (start_coord[0] - 1, start_coord[1])
        ]
    elif figure_type == 'L':
        return [
            (start_coord[0], start_coord[1]),
            (start_coord[0], start_coord[1] - 1),
            (start_coord[0], start_coord[1] - 2),
            (start_coord[0] - 1, start_coord[1] - 2),
            (start_coord[0] - 2, start_coord[1] - 2),
        ]
    elif figure_type == '|':
        return [
            (start_coord[0], start_coord[1]),
            (start_coord[0], start_coord[1] - 1),
            (start_coord[0], start_coord[1] - 2),
            (start_coord[0], start_coord[1] - 3),
        ]
    elif figure_type == '[]':
        return [
            (start_coord[0], start_coord[1]),
            (start_coord[0], start_coord[1] - 1),
            (start_coord[0] + 1, start_coord[1]),
            (start_coord[0] + 1, start_coord[1] - 1),
        ]
    else:
        raise Exception(f'weird figure: {figure_type} {start_coord}')


def print_grid(grid: typing.Dict[int, typing.List[str]]):
    if grid == {}:
        return
    grid_width = len(list(grid.values())[0])
    for i in range(max(grid.keys()), 0, -1):
        s = f'{i:<2}'
        if i not in grid:
            s += '.' * grid_width
        else:
            s += ''.join(grid[i])
        print(s)
    print()


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    figures = utils.RepeatingSequence(
        [
            '-', '+', 'L', '|', '[]', '-'
        ]
    )
    commands = utils.RepeatingSequence(
        [
            *[f'{i} {i_ind}' for i_ind, i in enumerate(input_lines[0])], f'{input_lines[0][0]} 0'
        ]
    )
    grid_width = 7
    cmd_ind = 0
    grid = {}
    for figure_ind in range(2022):
        current_figure = figures[figure_ind]
        figure_left_edge = 2
        bottom_edge = 4 if grid == {} else max(filter(lambda x: '#' in grid[x], grid.keys())) + 4
        if current_figure == '-':
            start_coord = (figure_left_edge, bottom_edge)
        elif current_figure == '+':
            start_coord = (figure_left_edge + 1, bottom_edge + 1)
        elif current_figure == 'L':
            start_coord = (figure_left_edge + 2, bottom_edge + 2)
        elif current_figure == '|':
            start_coord = (figure_left_edge, bottom_edge + 3)
        elif current_figure == '[]':
            start_coord = (figure_left_edge, bottom_edge + 1)
        else:
            continue
        figure_coords = get_figure_coords(current_figure, start_coord)
        for x, y in figure_coords:
            if y not in grid:
                grid[y] = ['.' for _ in range(7)]
            grid[y][x] = '@'
        figure_stopped = False
        while figure_stopped is False:
            cmd = commands[cmd_ind].split()[0]
            if cmd == '>':
                possible_move = True
                figure_coords_one_step_right = get_figure_coords(
                    current_figure, (start_coord[0] + 1, start_coord[1])
                )
                for x, y in figure_coords_one_step_right:
                    if x == grid_width:
                        possible_move = False
                        break
                    elif grid[y][x] == '#':
                        possible_move = False
                if possible_move:
                    start_coord = (start_coord[0] + 1, start_coord[1])
                    for x, y in figure_coords:
                        grid[y][x] = '.'
                    figure_coords = get_figure_coords(current_figure, start_coord)
            elif cmd == '<':
                possible_move = True
                figure_coords_one_step_right = get_figure_coords(
                    current_figure, (start_coord[0] - 1, start_coord[1])
                )
                for x, y in figure_coords_one_step_right:
                    if x == -1:
                        possible_move = False
                        break
                    elif grid[y][x] == '#':
                        possible_move = False
                if possible_move:
                    start_coord = (start_coord[0] - 1, start_coord[1])
                    for x, y in figure_coords:
                        grid[y][x] = '.'
                    figure_coords = get_figure_coords(current_figure, start_coord)
            for x, y in figure_coords:
                if y not in grid:
                    grid[y] = ['.' for _ in range(7)]
                grid[y][x] = '@'
            figure_coords_step_down = get_figure_coords(current_figure, (start_coord[0], start_coord[1] - 1))
            for x, y in figure_coords_step_down:
                if y in grid:
                    if grid[y][x] == '#':
                        for a, b in figure_coords:
                            if b not in grid:
                                grid[b] = ['.' for _ in range(7)]
                            grid[b][a] = '#'
                        figure_stopped = True
                        break
                elif y == 0:
                    for a, b in figure_coords:
                        grid[b][a] = '#'
                    figure_stopped = True
                    break
            if not figure_stopped:
                for x, y in figure_coords:
                    grid[y][x] = '.'
                start_coord = (start_coord[0], start_coord[1] - 1)
                figure_coords = get_figure_coords(current_figure, start_coord)
                for x, y in figure_coords:
                    if y not in grid:
                        grid[y] = ['.' for _ in range(7)]
                    grid[y][x] = '@'
            cmd_ind += 1
    return max(filter(lambda x: '#' in grid[x], grid.keys()))


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    mult = [
        33, 40, 37, 36, 39, 36, 42, 37, 41, 42, 38, 36, 40, 33, 35, 44, 41, 33, 35, 42, 30, 37, 34, 41, 33, 34, 39,
        41, 39, 35, 36, 39, 36, 29, 40, 32, 43, 38, 32, 44, 32, 39, 42, 30, 45, 32, 42, 36, 40, 35, 35, 32, 34, 32,
        36, 41, 43, 34, 41, 40, 44, 45, 33, 33, 35, 40, 43, 48, 38, 34, 40, 38, 35, 41, 46, 34, 36, 44, 35, 37, 41,
        38, 30, 38, 47, 37, 37, 37, 31, 36, 36, 35, 35, 37, 37, 39, 42, 41, 32, 34, 40, 30, 38, 36, 39, 39, 34, 38,
        36, 38, 39, 32, 43, 36, 40, 43, 31, 38, 34, 34, 36, 34, 30, 37, 43, 40, 40, 44, 36, 45, 39, 29, 39, 39, 37,
        46, 45, 34, 41, 37, 34, 40, 39, 44, 32, 45, 38, 40, 33, 44, 32, 32, 50, 36, 36, 33, 40, 32, 35, 37, 37, 35,
        36, 40, 38, 44, 32, 36, 38, 33, 35, 36, 35, 42, 38, 34, 39, 38, 40, 33, 35, 43, 37, 42, 31, 40, 37, 33, 32,
        34, 32, 36, 42, 44, 32, 43, 39, 46, 42, 31, 38, 34, 38, 45, 51, 33, 38, 39, 36, 40, 36, 47, 32, 39, 41, 41,
        35, 38, 37, 33, 39, 44, 37, 34, 40, 31, 33, 38, 41, 32, 34, 39, 43, 37, 38, 32, 39, 37, 30, 38, 35, 42, 38,
        34, 38, 36, 40, 39, 32, 45, 34, 39, 38, 36, 39, 33, 35, 30, 33, 37, 36, 44, 39, 37, 45, 41, 45, 34, 33, 36,
        39, 39, 49, 42, 34, 38, 38, 36, 40, 43, 39, 32, 47, 35, 38, 38, 41, 31, 33, 51, 36, 38, 33, 35, 36, 31, 39,
        36, 37, 36, 38, 44, 40, 32, 35, 38, 31, 37, 33, 42, 36, 41, 35, 36, 39, 36, 36, 40, 40, 35, 43, 30, 41, 32,
        37, 32, 35, 31, 39, 41, 42, 34, 47, 34, 47, 42, 28, 37, 37, 40, 43, 51
    ]
    x = 349
    for ch in utils.chunks(range(225, 1000000000000, 25), len(mult)):
        for i, a in enumerate(ch):
            x += mult[i]
    return x


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
