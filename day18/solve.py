import dataclasses
import typing


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
