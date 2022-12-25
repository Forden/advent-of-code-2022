import math
import queue
import time
import typing

import utils


def print_map(
        source: typing.List[str],
        blizzards_coords: typing.List[typing.Tuple[int, int, int, int]],
        enter_exit_coords: typing.List[typing.Tuple[int, int]],
        player_position: typing.Optional[typing.Tuple[int, int]] = None
):
    t = time.time()
    output = []
    blizzard_by_coord = {}
    amount_per_cell = {}
    for i in blizzards_coords:
        if (i[0], i[1]) not in blizzard_by_coord:
            blizzard_by_coord[(i[0], i[1])] = []
        blizzard_by_coord[(i[0], i[1])].append(i)
    for x, y in blizzard_by_coord.keys():
        amount_per_cell[(x, y)] = len(blizzard_by_coord[(x, y)])
    for row_y in range(len(source)):
        if row_y == 0:
            s = ['#' for _ in range(len(source[0]))]
            enter_coord = list(filter(lambda a: a[1] == 0, enter_exit_coords))[0]
            s[enter_coord[0]] = '.'
        elif row_y == len(source) - 1:
            s = ['#' for _ in range(len(source[0]))]
            exit_coord = list(filter(lambda a: a[1] != 0, enter_exit_coords))[0]
            s[exit_coord[0]] = '.'
        else:
            s = []
            for cell_x in range(len(source[0])):
                if cell_x == 0:
                    s.append('#')
                    continue
                if cell_x == (len(source[0]) - 1):
                    s.append('#')
                    break
                amount_in = amount_per_cell.get((cell_x, row_y), 0)
                if amount_in == 1:
                    direction = blizzard_by_coord[(cell_x, row_y)][0][2]
                    if direction == 0:
                        s.append('>')
                    elif direction == 90:
                        s.append('^')
                    elif direction == 180:
                        s.append('<')
                    elif direction == 270:
                        s.append('v')
                elif amount_in > 1:
                    s.append(f'{amount_in}')
                else:
                    s.append('.')
        if player_position:
            if row_y == player_position[1]:
                s[player_position[0]] = 'E'
        output.append(''.join(s))
    print(*output, sep='\n')
    print(f'took {round(time.time() - t, 3)} sec to render map')


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_new_blizz_coord(x: int, y: int, direction: int, blizzard_id: int) -> typing.Tuple[int, int, int, int]:
        new_x, new_y = x, y
        if direction == 0:
            if (x + 1) == (len(input_lines[0]) - 1):
                new_x = 1
            else:
                new_x = x + 1
        elif direction == 90:
            if (y - 1) == 0:
                new_y = len(input_lines) - 2
            else:
                new_y = y - 1
        elif direction == 180:
            if (x - 1) == 0:
                new_x = len(input_lines[0]) - 2
            else:
                new_x = x - 1
        elif direction == 270:
            if (y + 1) == len(input_lines) - 1:
                new_y = 1
            else:
                new_y = y + 1
        return new_x, new_y, direction, blizzard_id

    def get_new_coords(
            old_coords: typing.Iterable[typing.Tuple[int, int, int, int]]
    ) -> typing.Dict[typing.Tuple[int, int, int, int], typing.Tuple[int, int, int, int]]:
        new_blizzards_coords: typing.Dict[typing.Tuple[int, int, int, int], typing.Tuple[int, int, int, int]] = {
            i: i for i in old_coords
        }
        for x, y, direction, blizzard_id in old_coords:
            new_blizzards_coords[(x, y, direction, blizzard_id)] = get_new_blizz_coord(x, y, direction, blizzard_id)
        return new_blizzards_coords

    def get_possible_steps(
            grid: typing.List[typing.List[str]],
            player_position: typing.Tuple[int, int]
    ) -> typing.List[typing.Tuple[int, int]]:
        all_neighbours = utils.get_neighbours_in_2d_list(
            grid, player_position[1], player_position[0], allow_diagonal_steps=False
        )
        res = []
        for possible_x, possible_y in all_neighbours:
            if grid[possible_y][possible_x] != '.':
                continue
            res.append((possible_x, possible_y))
        return res

    def get_adjacency_lists(
            grid: typing.List[typing.List[str]]
    ) -> typing.Dict[typing.Tuple[int, int], typing.List[typing.Tuple[int, int]]]:
        res = {}
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                res[x, y] = get_possible_steps(grid, (x, y))
        return res

    def fill_cache(
            blizzards_coords: typing.List[typing.Tuple[int, int, int, int]],
            for_time: int
    ) -> typing.Dict[typing.Tuple[int, int, int], bool]:
        res = {}
        for x, y, _, _ in blizzards_coords:
            res[(x, y, 0)] = True
        for t in range(1, for_time + 1):
            new_blizzards_coords = get_new_coords(blizzards_coords)
            blizzards_coords = [*new_blizzards_coords.values()]
            for x, y, _, _ in blizzards_coords:
                res[(x, y, t)] = True
        return res

    def will_be_occupied(
            cache: typing.Dict[typing.Tuple[int, int, int], bool],
            checking_x: int, checking_y: int, checking_time: int
    ) -> bool:
        return cache.get((checking_x, checking_y, checking_time), False)

    result = 0
    enter_exit_coords: typing.List[typing.Tuple[int, int]] = []
    for x, cell in enumerate(input_lines[0]):
        if cell != '#':
            enter_exit_coords.append((x, 0))
    for x, cell in enumerate(input_lines[-1]):
        if cell != '#':
            enter_exit_coords.append((x, len(input_lines) - 1))
    player_coords = None
    start_coord = list(filter(lambda a: a[1] == 0, enter_exit_coords))[0]
    exit_coord = list(filter(lambda a: a[1] != 0, enter_exit_coords))[0]
    blizzards_coords: typing.List[typing.Tuple[int, int, int, int]] = []
    wall_coords: typing.List[typing.Tuple[int, int]] = []
    for y, row in enumerate(input_lines):
        for x, cell in enumerate(row):
            if cell == 'E':
                player_coords = (x, y)
            elif cell == '#':
                wall_coords.append((x, y))
            elif cell == '.':
                pass
            else:
                if cell == '>':
                    direction = 0
                elif cell == '^':
                    direction = 90
                elif cell == '<':
                    direction = 180
                else:
                    direction = 270
                blizzards_coords.append((x, y, direction, len(blizzards_coords)))
    grid = [['.' for _ in range(len(input_lines[0]))] for _ in range(len(input_lines))]
    for x, y in wall_coords:
        grid[y][x] = '#'
    for x, y, _, _ in blizzards_coords:
        grid[y][x] = 'X'
    grid[player_coords[1]][player_coords[0]] = 'E'

    print_map(input_lines, blizzards_coords, enter_exit_coords, player_coords)

    cache = fill_cache(blizzards_coords, math.lcm(len(grid) - 2, len(grid[0]) - 2))

    moves = [
        [0, 1],
        [1, 0],
        [-1, 0],
        [0, -1]
    ]
    Q = queue.Queue()
    Q.put(
        (player_coords[0], player_coords[1], 0)
    )
    visited = set()
    while not Q.empty():
        checking = Q.get()
        if checking in visited:
            continue
        visited.add(checking)

        x, y, t = checking

        if (x, y) == exit_coord:
            print(t)
            break

        for checking_move_x, checking_move_y in [*moves, [0, 0]]:
            new_x, new_y = x + checking_move_x, y + checking_move_y
            new_location = (new_x, new_y)

            if (
                    (
                            not new_location in [start_coord, exit_coord]
                    ) and not (
                    (
                            1 <= new_x <= len(grid[0]) - 2
                    ) and (
                            1 <= new_y <= len(grid) - 2
                    )
            )
            ):  # not inside walls
                continue

            if will_be_occupied(cache, new_x, new_y, t + 1):  # will be occupied on next minute
                continue

            Q.put(
                (new_x, new_y, t + 1)
            )

            # while player_coords != exit_coord:
    #     time.sleep(.5)
    #     t = time.time()
    #     new_blizzards_coords = get_new_coords(blizzards_coords)
    #     for x, y in wall_coords:
    #         grid[y][x] = '#'
    #     for x, y, _, _ in blizzards_coords:
    #         grid[y][x] = '.'
    #     grid[player_coords[1]][player_coords[0]] = 'E'
    #     blizzards_coords = [*new_blizzards_coords.values()]
    #     for x, y, _, _ in blizzards_coords:
    #         grid[y][x] = 'X'
    #     # print_map(input_lines, list(map(tuple, blizzards_coords)), enter_exit_coords, player_coords)
    #     adjacency_lists = get_adjacency_lists(grid)
    #     _, dists, path_exists = utils.bfs(adjacency_lists, player_coords, exit_coord)
    #     print(path_exists)
    #     print(
    #         *[
    #             f'possible steps: {get_possible_steps(grid, player_coords)}',
    #             f'took {round(time.time() - t, 3)} sec to make round'
    #         ],
    #         sep='\n'
    #     )
    # print(blizzards_coords)
    return result


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
