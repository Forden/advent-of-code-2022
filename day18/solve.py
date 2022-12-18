import dataclasses
import queue
import typing
from multiprocessing import Pool


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    @dataclasses.dataclass
    class Cube:
        x: int
        y: int
        z: int

        def __hash__(self):
            return hash((self.x, self.y, self.z))

    result = 0

    def get_cube_exposed_sides_count(
            cube: Cube, grid: typing.Set[Cube]
    ) -> int:
        res = 6
        for i in grid:
            if i.x == cube.x + 1 and i.y == cube.y and i.z == cube.z:
                res -= 1
            elif i.x == cube.x - 1 and i.y == cube.y and i.z == cube.z:
                res -= 1
            elif i.x == cube.x and i.y == cube.y + 1 and i.z == cube.z:
                res -= 1
            elif i.x == cube.x and i.y == cube.y - 1 and i.z == cube.z:
                res -= 1
            elif i.x == cube.x and i.y == cube.y and i.z == cube.z + 1:
                res -= 1
            elif i.x == cube.x and i.y == cube.y and i.z == cube.z - 1:
                res -= 1
        return res

    cubes = set()
    for cube in input_lines:
        x, y, z, = map(int, cube.split(','))
        cubes.add(Cube(x, y, z))
    for i in cubes:
        result += get_cube_exposed_sides_count(i, cubes)
    return result


@dataclasses.dataclass
class Cube:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f'Cube(x={self.x} y={self.y} z={self.z})'


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def check_reaches_outside(cube: Cube):
        q = queue.Queue()
        seen = set()
        q.put(cube)
        while not q.empty():
            checking = q.get()
            if checking in seen:
                continue
            if checking in cubes:
                continue
            seen.add(checking)
            if len(seen) > 5000:
                return True
            for _ in range(2):
                q.put(Cube(checking.x + 1, checking.y, checking.z))
                q.put(Cube(checking.x - 1, checking.y, checking.z))
                q.put(Cube(checking.x, checking.y + 1, checking.z))
                q.put(Cube(checking.x, checking.y - 1, checking.z))
                q.put(Cube(checking.x, checking.y, checking.z + 1))
                q.put(Cube(checking.x, checking.y, checking.z - 1))

        return False

    cubes = set()
    for cube in input_lines:
        x, y, z, = map(int, cube.split(','))
        cubes.add(Cube(x, y, z))

    global check_cube

    def check_cube(i: Cube) -> int:
        result = 0
        if check_reaches_outside(Cube(i.x + 1, i.y, i.z)):
            result += 1
        if check_reaches_outside(Cube(i.x - 1, i.y, i.z)):
            result += 1
        if check_reaches_outside(Cube(i.x, i.y + 1, i.z)):
            result += 1
        if check_reaches_outside(Cube(i.x, i.y - 1, i.z)):
            result += 1
        if check_reaches_outside(Cube(i.x, i.y, i.z + 1)):
            result += 1
        if check_reaches_outside(Cube(i.x, i.y, i.z - 1)):
            result += 1
        return result

    with Pool() as p:
        result = sum(list(p.map(check_cube, cubes)))
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
