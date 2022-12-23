import typing
from collections import deque

import utils


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def print_grid(
            grid: typing.List[typing.List[str]],
            elves_coords: typing.Optional[typing.List[typing.Tuple[int, int]]] = None
    ):
        # print()
        for y, row in enumerate(grid):
            if '#' not in row:
                continue
            s = ['.' for _ in range(len(row))]
            if elves_coords:
                for e_x, e_y in elves_coords:
                    if e_y == y:
                        s[e_x] = '#'
            print(''.join(s))

    elves_coords = []
    grid = []
    for _ in range(20):
        row = ['.' for _ in range(20)]
        row.extend(['.' for _ in range(len(input_lines[0]))])
        row.extend(['.' for _ in range(20)])
        grid.append(row)
    for i in input_lines:
        row = []
        row = ['.' for _ in range(20)]
        row.extend(list(i))
        row.extend(['.' for _ in range(20)])
        grid.append(row)
    for _ in range(20):
        row = ['.' for _ in range(20)]
        row.extend(['.' for _ in range(len(input_lines[0]))])
        row.extend(['.' for _ in range(20)])
        grid.append(row)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                elves_coords.append((x, y))
    # print_grid(grid, elves_coords)
    # print(utils.get_neighbours_in_2d_list(grid, 2, 2))
    for round_id in range(1, 11):
        new_elves_coords = {i: i for i in elves_coords}
        for x, y in elves_coords:
            neighbours = utils.get_neighbours_in_2d_list(grid, y, x)
            neighbours_by_axis = {}
            for nei_x, nei_y in neighbours:
                if nei_x == x and nei_y == y - 1:
                    neighbours_by_axis['N'] = (nei_x, nei_y)
                elif nei_x == x and nei_y == y + 1:
                    neighbours_by_axis['S'] = (nei_x, nei_y)
                elif nei_x == x - 1 and nei_y == y:
                    neighbours_by_axis['W'] = (nei_x, nei_y)
                elif nei_x == x + 1 and nei_y == y:
                    neighbours_by_axis['E'] = (nei_x, nei_y)
                elif nei_x == x - 1 and nei_y == y - 1:
                    neighbours_by_axis['NW'] = (nei_x, nei_y)
                elif nei_x == x - 1 and nei_y == y + 1:
                    neighbours_by_axis['SW'] = (nei_x, nei_y)
                elif nei_x == x + 1 and nei_y == y - 1:
                    neighbours_by_axis['NE'] = (nei_x, nei_y)
                elif nei_x == x + 1 and nei_y == y + 1:
                    neighbours_by_axis['SE'] = (nei_x, nei_y)
            for k in list(neighbours_by_axis.keys()):
                c_x, c_y = neighbours_by_axis[k]
                if grid[c_y][c_x] == '.':
                    del neighbours_by_axis[k]
            # print(
            #     round_id,
            #     x, y,
            #     neighbours_by_axis,
            # )
            terms = deque(
                [
                    ['north', [i not in neighbours_by_axis for i in ['N', 'NE', 'NW']], y - 1 >= 0],
                    ['south', [i not in neighbours_by_axis for i in ['S', 'SE', 'SW']], y + 1 < len(grid)],
                    ['west', [i not in neighbours_by_axis for i in ['W', 'NW', 'SW']], x - 1 >= 0],
                    ['east', [i not in neighbours_by_axis for i in ['E', 'NE', 'SE']], x + 1 < len(grid[0])]
                ]
            )
            terms.rotate(-((round_id - 1) % 4))
            # print(
            #     *list(
            #         terms
            #     ),
            #     sep='\n'
            # )
            if len(neighbours_by_axis) == 0:
                continue
            # print(round_id, x, y, neighbours_by_axis, [i not in neighbours_by_axis for i in ['N', 'NE', 'NW']], y - 1)
            if round_id % 4 == 1:
                if all([i not in neighbours_by_axis for i in ['N', 'NE', 'NW']]) and y - 1 >= 0:
                    # print('north')
                    new_elves_coords[(x, y)] = (x, y - 1)
                elif all([i not in neighbours_by_axis for i in ['S', 'SE', 'SW']]) and y + 1 < len(grid):
                    # print('south')
                    new_elves_coords[(x, y)] = (x, y + 1)
                elif all([i not in neighbours_by_axis for i in ['W', 'NW', 'SW']]) and x - 1 >= 0:
                    # print('west')
                    new_elves_coords[(x, y)] = (x - 1, y)
                elif all([i not in neighbours_by_axis for i in ['E', 'NE', 'SE']]) and x + 1 < len(grid[0]):
                    # print('east')
                    new_elves_coords[(x, y)] = (x + 1, y)
            elif round_id % 4 == 2:
                if all([i not in neighbours_by_axis for i in ['S', 'SE', 'SW']]) and y + 1 < len(grid):
                    # print('south')
                    new_elves_coords[(x, y)] = (x, y + 1)
                elif all([i not in neighbours_by_axis for i in ['W', 'NW', 'SW']]) and x - 1 >= 0:
                    # print('west')
                    new_elves_coords[(x, y)] = (x - 1, y)
                elif all([i not in neighbours_by_axis for i in ['E', 'NE', 'SE']]) and x + 1 < len(grid[0]):
                    # print('east')
                    new_elves_coords[(x, y)] = (x + 1, y)
                elif all([i not in neighbours_by_axis for i in ['N', 'NE', 'NW']]) and y - 1 >= 0:
                    # print('north')
                    new_elves_coords[(x, y)] = (x, y - 1)
            elif round_id % 4 == 3:
                if all([i not in neighbours_by_axis for i in ['W', 'NW', 'SW']]) and x - 1 >= 0:
                    # print('west')
                    new_elves_coords[(x, y)] = (x - 1, y)
                elif all([i not in neighbours_by_axis for i in ['E', 'NE', 'SE']]) and x + 1 < len(grid[0]):
                    # print('east')
                    new_elves_coords[(x, y)] = (x + 1, y)
                elif all([i not in neighbours_by_axis for i in ['N', 'NE', 'NW']]) and y - 1 >= 0:
                    # print('north')
                    new_elves_coords[(x, y)] = (x, y - 1)
                elif all([i not in neighbours_by_axis for i in ['S', 'SE', 'SW']]) and y + 1 < len(grid):
                    # print('south')
                    new_elves_coords[(x, y)] = (x, y + 1)
            elif round_id % 4 == 0:
                if all([i not in neighbours_by_axis for i in ['E', 'NE', 'SE']]) and x + 1 < len(grid[0]):
                    # print('east')
                    new_elves_coords[(x, y)] = (x + 1, y)
                elif all([i not in neighbours_by_axis for i in ['N', 'NE', 'NW']]) and y - 1 >= 0:
                    # print('north')
                    new_elves_coords[(x, y)] = (x, y - 1)
                elif all([i not in neighbours_by_axis for i in ['S', 'SE', 'SW']]) and y + 1 < len(grid):
                    # print('south')
                    new_elves_coords[(x, y)] = (x, y + 1)
                elif all([i not in neighbours_by_axis for i in ['W', 'NW', 'SW']]) and x - 1 >= 0:
                    # print('west')
                    new_elves_coords[(x, y)] = (x - 1, y)
        seen_targets = {}
        for start, target in new_elves_coords.items():
            if target not in seen_targets:
                seen_targets[target] = 0
            seen_targets[target] += 1
        for target in list(seen_targets.keys()):
            if seen_targets[target] == 1:
                del seen_targets[target]
        for start in list(new_elves_coords.keys()):
            if new_elves_coords[start] in seen_targets:
                new_elves_coords[start] = start
        assert len(elves_coords) == len(new_elves_coords)
        for x, y in elves_coords:
            grid[y][x] = '.'
        elves_coords = [*new_elves_coords.values()]
        for x, y in elves_coords:
            grid[y][x] = '#'
        print(round_id)
        print_grid(grid, elves_coords)
    min_x, min_y, max_x, max_y = 1000000000000, 1000000000000, -1, -1
    for x, y in elves_coords:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    print(min_x, min_y, max_x, max_y)
    print(abs(max_x - min_x), abs(max_y - min_y))
    result = (abs(max_x - min_x) + 1) * (abs(max_y - min_y) + 1)
    result -= len(elves_coords)
    # print(max_x - min_x, max_y - max_y)
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
