import string
import typing

import utils


def get_dot_height(value: str):
    return string.ascii_letters.index(value) + 1


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_all_connections(grid, x, y):
        x_to_check = [x]
        y_to_check = [y]
        if x == 0:
            x_to_check.append(x + 1)
        elif x == len(grid[0]) - 1:
            x_to_check.append(x - 1)
        else:
            x_to_check.append(x + 1)
            x_to_check.append(x - 1)
        if y == 0:
            y_to_check.append(y + 1)
        elif y == len(grid) - 1:
            y_to_check.append(y - 1)
        else:
            y_to_check.append(y + 1)
            y_to_check.append(y - 1)
        current_value = grid[y][x]
        res = []

        for checking_x in x_to_check:
            for checking_y in y_to_check:
                if checking_y == y and checking_x == x:
                    continue
                if checking_x != x and checking_y != y:
                    continue
                if grid[checking_y][checking_x] <= current_value + 1:
                    res.append((checking_x, checking_y))
        return res

    def add_connection(arr, source, dest):
        if source not in arr:
            arr[source] = []
        if dest not in arr[source]:
            arr[source].append(dest)

    def get_shortest_path_length(arr, source, dest):
        _, dist, path_exists = utils.bfs(connections_list=arr, start=source, target=dest)
        if not path_exists:
            print('path not found')
        return dist[dest]

    current = (0, 0)
    target = (0, 0)
    for y, _ in enumerate(input_lines):
        for x, _ in enumerate(input_lines[y]):
            if input_lines[y][x] == 'S':
                current = (x, y)
            elif input_lines[y][x] == 'E':
                target = (x, y)
    input_lines[current[1]] = input_lines[current[1]][:current[0]] + 'a' + input_lines[current[1]][current[0] + 1:]
    input_lines[target[1]] = input_lines[target[1]][:target[0]] + 'z' + input_lines[target[1]][target[0] + 1:]
    grid = [[get_dot_height(i) for i in row] for row in input_lines]
    graph_short = []
    for y, _ in enumerate(grid):
        for x, _ in enumerate(grid[y]):
            graph_short.append((x, y))
    coords_to_short = {}
    for ind, i in enumerate(graph_short):
        coords_to_short[str(i)] = ind
    connections = {}
    counter = 0
    for b, _ in enumerate(input_lines):
        for a, _ in enumerate(input_lines[b]):
            for i in get_all_connections(grid, a, b):
                add_connection(connections, counter, coords_to_short[str(i)])
            counter += 1

    result = get_shortest_path_length(
        connections, coords_to_short[str(current)], coords_to_short[str(target)]
    )

    return result


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_all_connections(grid, x, y):
        x_to_check = [x]
        y_to_check = [y]
        if x == 0:
            x_to_check.append(x + 1)
        elif x == len(grid[0]) - 1:
            x_to_check.append(x - 1)
        else:
            x_to_check.append(x + 1)
            x_to_check.append(x - 1)
        if y == 0:
            y_to_check.append(y + 1)
        elif y == len(grid) - 1:
            y_to_check.append(y - 1)
        else:
            y_to_check.append(y + 1)
            y_to_check.append(y - 1)
        current_value = grid[y][x]
        res = []

        for checking_x in x_to_check:
            for checking_y in y_to_check:
                if checking_y == y and checking_x == x:
                    continue
                if checking_x != x and checking_y != y:
                    continue
                if grid[checking_y][checking_x] <= current_value + 1:
                    res.append((checking_x, checking_y))
        return res

    def add_connection(arr, source, dest):
        if source not in arr:
            arr[source] = []
        if dest not in arr[source]:
            arr[source].append(dest)

    def get_shortest_path_length(arr, source, dest):
        _, dist, path_exists = utils.bfs(connections_list=arr, start=source, target=dest)
        if not path_exists:
            return -1
        return dist[dest]

    current = (0, 0)
    target = (0, 0)
    for y, _ in enumerate(input_lines):
        for x, _ in enumerate(input_lines[y]):
            if input_lines[y][x] == 'S':
                current = (x, y)
            elif input_lines[y][x] == 'E':
                target = (x, y)
    input_lines[current[1]] = input_lines[current[1]][:current[0]] + 'a' + input_lines[current[1]][current[0] + 1:]
    input_lines[target[1]] = input_lines[target[1]][:target[0]] + 'z' + input_lines[target[1]][target[0] + 1:]
    grid = [[get_dot_height(i) for i in row] for row in input_lines]
    graph_short = []
    for y, _ in enumerate(grid):
        for x, _ in enumerate(grid[y]):
            graph_short.append((x, y))
    coords_to_short = {}
    for ind, i in enumerate(graph_short):
        coords_to_short[str(i)] = ind
    connections = {}
    counter = 0
    for b, _ in enumerate(input_lines):
        for a, _ in enumerate(input_lines[b]):
            for i in get_all_connections(grid, a, b):
                add_connection(connections, counter, coords_to_short[str(i)])
            counter += 1

    results = {}
    for y, _ in enumerate(grid):
        for x, _ in enumerate(grid[y]):
            if grid[y][x] == 1:
                results[(x, y)] = -1
    for i in results:
        results[i] = get_shortest_path_length(
            connections, coords_to_short[str(i)], coords_to_short[str(target)]
        )
    return min(filter(lambda x: x > 0, results.values()))


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
