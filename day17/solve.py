import typing

import utils


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
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
        return
        if grid == {}:
            return
        for i in range(max(grid.keys()), 0, -1):
            s = f'{i:<2}'
            if i not in grid:
                s += '.' * grid_width
            else:
                s += ''.join(grid[i])
            print(s)
        print()

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
    result = 0
    spawned_figures_amount = 1
    grid_width = 7
    cmd_ind = 0
    grid = {}
    for figure_ind in range(2022):
        current_figure = figures[figure_ind]
        figure_left_edge = 2
        print('before spawning new figure')
        print_grid(grid)
        bottom_edge = 4 if grid == {} else max(filter(lambda x: '#' in grid[x], grid.keys())) + 4
        print(list(grid.keys()), list(filter(lambda x: '#' in grid[x], grid.keys())), bottom_edge)
        if current_figure == '-':
            start_coord = (figure_left_edge, bottom_edge)
        elif current_figure == '+':
            start_coord = (figure_left_edge + 1, bottom_edge + 1)
        elif current_figure == 'L':
            start_coord = (figure_left_edge + 2, bottom_edge + 2)
        elif current_figure == '|':
            start_coord = (figure_left_edge, bottom_edge + 3)
        elif current_figure == '[]':
            start_coord = (figure_left_edge, bottom_edge+1)
        else:
            continue
        figure_coords = get_figure_coords(current_figure, start_coord)
        for x, y in figure_coords:
            if y not in grid:
                grid[y] = ['.' for _ in range(7)]
            grid[y][x] = '@'
        print(f'spawned figure [{current_figure=}]')
        print_grid(grid)
        figure_stopped = False
        while figure_stopped is False:
            cmd = commands[cmd_ind].split()[0]
            print(f'{cmd=} {cmd_ind=}, {current_figure=}')
            if current_figure == '-':
                if cmd == '>':
                    possible_move = True
                    figure_coords_one_step_right = get_figure_coords(
                        current_figure, (start_coord[0] + 1, start_coord[1])
                    )
                    for x, y in figure_coords_one_step_right:
                        if x == grid_width:
                            print(f'move impossible because right limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
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
                            print(f'move impossible because left limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
                        start_coord = (start_coord[0] - 1, start_coord[1])
                        for x, y in figure_coords:
                            grid[y][x] = '.'
                        figure_coords = get_figure_coords(current_figure, start_coord)
            elif current_figure == '+':
                if cmd == '>':
                    possible_move = True
                    figure_coords_one_step_right = get_figure_coords(
                        current_figure, (start_coord[0] + 1, start_coord[1])
                    )
                    for x, y in figure_coords_one_step_right:
                        if x == grid_width:
                            print(f'move impossible because right limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
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
                            print(f'move impossible because left limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
                        start_coord = (start_coord[0] - 1, start_coord[1])
                        for x, y in figure_coords:
                            grid[y][x] = '.'
                        figure_coords = get_figure_coords(current_figure, start_coord)
            elif current_figure == 'L':
                if cmd == '>':
                    possible_move = True
                    figure_coords_one_step_right = get_figure_coords(
                        current_figure, (start_coord[0] + 1, start_coord[1])
                    )
                    for x, y in figure_coords_one_step_right:
                        if x == grid_width:
                            print(f'move impossible because right limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
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
                            print(f'move impossible because left limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
                        start_coord = (start_coord[0] - 1, start_coord[1])
                        for x, y in figure_coords:
                            grid[y][x] = '.'
                        figure_coords = get_figure_coords(current_figure, start_coord)
            elif current_figure == '|':
                if cmd == '>':
                    possible_move = True
                    figure_coords_one_step_right = get_figure_coords(
                        current_figure, (start_coord[0] + 1, start_coord[1])
                    )
                    for x, y in figure_coords_one_step_right:
                        if x == grid_width:
                            print(f'move impossible because right limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
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
                            print(f'move impossible because left limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
                        start_coord = (start_coord[0] - 1, start_coord[1])
                        for x, y in figure_coords:
                            grid[y][x] = '.'
                        figure_coords = get_figure_coords(current_figure, start_coord)
            elif current_figure == '[]':
                if cmd == '>':
                    possible_move = True
                    figure_coords_one_step_right = get_figure_coords(
                        current_figure, (start_coord[0] + 1, start_coord[1])
                    )
                    for x, y in figure_coords_one_step_right:
                        if x == grid_width:
                            print(f'move impossible because right limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
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
                            print(f'move impossible because left limit at {(x, y)=}')
                            possible_move = False
                            break
                        elif grid[y][x] == '#':
                            print(f'move impossible because figure right at {(x, y)=}')
                            possible_move = False
                    if possible_move:
                        print(f'move possible, executing')
                        start_coord = (start_coord[0] - 1, start_coord[1])
                        for x, y in figure_coords:
                            grid[y][x] = '.'
                        figure_coords = get_figure_coords(current_figure, start_coord)
            for x, y in figure_coords:
                if y not in grid:
                    grid[y] = ['.' for _ in range(7)]
                grid[y][x] = '@'
            print(f'after {cmd} new coords: {figure_coords=}')
            print_grid(grid)
            figure_coords_step_down = get_figure_coords(current_figure, (start_coord[0], start_coord[1] - 1))
            print(f'checking coords {figure_coords_step_down=} ')
            for x, y in figure_coords_step_down:
                if y in grid:
                    if grid[y][x] == '#':
                        print(f'found stopped figure at ({x=}, {y=})')
                        for a, b in figure_coords:
                            if b not in grid:
                                grid[b] = ['.' for _ in range(7)]
                            grid[b][a] = '#'
                        figure_stopped = True
                        break
                elif y == 0:
                    print(f'reached y = 0')
                    for a, b in figure_coords:
                        grid[b][a] = '#'
                    figure_stopped = True
                    break
            if not figure_stopped:
                for x, y in figure_coords:
                    grid[y][x] = '.'
                print(
                    f'figure was not stopped, old start_coord: {start_coord=}, new: {(start_coord[0], start_coord[1] - 1)=}'
                )
                start_coord = (start_coord[0], start_coord[1] - 1)
                figure_coords = get_figure_coords(current_figure, start_coord)
                for x, y in figure_coords:
                    if y not in grid:
                        grid[y] = ['.' for _ in range(7)]
                    grid[y][x] = '@'

            print('after move down')
            print_grid(grid)
            cmd_ind += 1
            # time.sleep(.5)
    return max(filter(lambda x: '#' in grid[x], grid.keys()))


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
        # 'sample.txt',
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
