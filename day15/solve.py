import typing


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_manh_distance(start, end):
        diff_x, diff_y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return diff_x + diff_y

    result = 0
    input_data = []
    sensors_locations = set()
    beacons_locations = set()
    closest_beacon_to_sensor = {}
    for i in input_lines:
        _, _, x, y, _, _, _, _, x_clo, y_clo = i.split()
        x = int(x.split('=')[1][:-1])
        y = int(y.split('=')[1][:-1])
        x_clo = int(x_clo.split('=')[1][:-1])
        y_clo = int(y_clo.split('=')[1])
        sensors_locations.add((x, y))
        beacons_locations.add((x_clo, y_clo))
        closest_beacon_to_sensor[(x, y)] = (x_clo, y_clo)
    print(sensors_locations, beacons_locations, closest_beacon_to_sensor, sep='\n')
    result = 0
    marked = set()
    for sensor, closest_beacon in closest_beacon_to_sensor.items():
        to_beacon = get_manh_distance(sensor, closest_beacon)
        print(sensor)
        for i in range(-10_000_000, 10_000_000):
        # for i in range(-100, 100):
            if (i, 2000000) in marked:
                continue
            dist = get_manh_distance(sensor, (i, 2000000))
            if dist <= to_beacon:
                marked.add((i, 2000000))
                result += 1
                # print(sensor, (i, 10), dist)
    return len(marked.difference(beacons_locations))


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
