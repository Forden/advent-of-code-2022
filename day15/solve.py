import typing
from multiprocessing import Pool


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_manh_distance(start, end):
        diff_x, diff_y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return diff_x + diff_y

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
    result = 0
    marked = set()
    for sensor, closest_beacon in closest_beacon_to_sensor.items():
        to_beacon = get_manh_distance(sensor, closest_beacon)
        for i in range(-10_000_000, 10_000_000):
            if (i, 2000000) in marked:
                continue
            dist = get_manh_distance(sensor, (i, 2000000))
            if dist <= to_beacon:
                marked.add((i, 2000000))
                result += 1
    return len(marked.difference(beacons_locations))


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def get_manh_distance(start, end):
        diff_x, diff_y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return diff_x + diff_y

    sensors_locations = set()
    beacons_locations = set()
    closest_beacon_to_sensor = {}
    closest_beacon_to_sensor_distances = {}
    for i in input_lines:
        _, _, x, y, _, _, _, _, x_clo, y_clo = i.split()
        x = int(x.split('=')[1][:-1])
        y = int(y.split('=')[1][:-1])
        x_clo = int(x_clo.split('=')[1][:-1])
        y_clo = int(y_clo.split('=')[1])
        sensors_locations.add((x, y))
        beacons_locations.add((x_clo, y_clo))
        closest_beacon_to_sensor[(x, y)] = (x_clo, y_clo)
        closest_beacon_to_sensor_distances[(x, y)] = get_manh_distance((x, y), (x_clo, y_clo))
    global check_xs_for_y

    def check_xs_for_y(y: int):
        ranges = []
        for sensor, distance_to_beacon in closest_beacon_to_sensor_distances.items():
            height_diff = get_manh_distance(sensor, (sensor[0], y))
            if height_diff > distance_to_beacon:
                continue
            min_x = sensor[0] - (distance_to_beacon - height_diff)
            max_x = sensor[0] + (distance_to_beacon - height_diff)
            ranges.append((min_x, max_x))
        if ranges:
            occupied = []
            for begin, end in sorted(ranges):
                if occupied and occupied[-1][1] >= begin - 1:
                    occupied[-1] = (occupied[-1][0], max(end, occupied[-1][1]))
                else:
                    occupied.append((begin, end))
            if len(occupied) != 1:
                occupied_needed = []
                for start, end in occupied:
                    occupied_needed.extend(filter(lambda x: 4000000 >= x >= 0, range(start, end + 1)))
                occupied_amount = len(occupied_needed)
            else:
                occupied = list(map(list, occupied))
                if occupied[0][0] < 0:
                    occupied[0][0] = 0
                if occupied[0][1] > 4000001:
                    occupied[0][1] = 4000001
                occupied_amount = occupied[0][1] - occupied[0][0]
            if 0 < occupied_amount < 4000001:
                occupied_needed = []
                for start, end in occupied:
                    occupied_needed.extend(filter(lambda x: 4000000 >= x >= 0, range(start, end + 1)))
                return occupied, y
        return None

    with Pool(11) as p:
        results = list(filter(lambda res: res is not None, p.map(check_xs_for_y, range(4000001))))
    ranges, y = list(filter(lambda a: a is not None, results))[0]
    return (ranges[0][1] + 1) * 4000000 + y


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
