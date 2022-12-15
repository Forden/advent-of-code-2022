import time
import typing
from multiprocessing import Pool


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
    def get_manh_distance(start, end):
        diff_x, diff_y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return diff_x + diff_y

    result = 0
    input_data = []
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
    print(sensors_locations, beacons_locations, closest_beacon_to_sensor, sep='\n')
    result = 0
    marked = set()
    free_spaces = set()
    global check_xs_for_y

    def check_xs_for_y(y: int):
        t = time.time()
        marked = set()
        skipped = 0
        checked_dists = 0
        # print(f'checking {y=}')
        ranges = []
        for sensor, distance_to_beacon in closest_beacon_to_sensor_distances.items():
            height_diff = get_manh_distance(sensor, (sensor[0], y))
            if height_diff > distance_to_beacon:
                continue
            min_x = sensor[0] - (distance_to_beacon - height_diff)
            max_x = sensor[0] + (distance_to_beacon - height_diff)
            ranges.append((min_x, max_x))
            # print(f'{sensor=} {distance_to_beacon=} {height_diff=} {min_x=} {max_x=}')
        if ranges:
            # print(f'{ranges=}')
            occupied = []
            for begin, end in sorted(ranges):
                if occupied and occupied[-1][1] >= begin - 1:
                    occupied[-1] = (occupied[-1][0], max(end, occupied[-1][1]))
                else:
                    occupied.append((begin, end))
            # occupied = occupied[0]
            # print(occupied)
            # occupied = {*range(*ranges[0])}.union(*map(lambda a: {*range(*a)}, ranges[1:]))
            # print('created ranges')
            if len(occupied) != 1:
                print(y, occupied)
                occupied_needed = []
                for start, end in occupied:
                    occupied_needed.extend(filter(lambda x: 4000000 >= x >= 0, range(start, end + 1)))
                occupied_amount = len(occupied_needed)
            else:
                occupied_amount = 0
                occupied = list(map(list, occupied))
                if occupied[0][0] < 0:
                    occupied[0][0] = 0
                if occupied[0][1] > 4000001:
                    occupied[0][1] = 4000001
                occupied_amount = occupied[0][1] - occupied[0][0]
                # for i in range(occupied[0][0], occupied[0][1] + 1):
                #     if 4000000 >= i >= 0:
                #         occupied_amount += 1
                # print(
                #     occupied[0],
                #     occupied_amount == occupied[0][1] - occupied[0][0],
                #     occupied_amount,
                #     occupied[0][1] - occupied[0][0]
                # )
                # occupied_amount = len(occupied_needed)
            if 0 < occupied_amount < 4000001:
                print(
                    f'processed line {y} in {time.time() - t} {occupied_amount=}'
                )
                print(ranges, occupied_amount, y)
                occupied_needed = []
                for start, end in occupied:
                    occupied_needed.extend(filter(lambda x: 4000000 >= x >= 0, range(start, end + 1)))
                print(occupied, min(occupied_needed), max(occupied_needed))
                return {(x, y) for x in range(4000001)}.difference(occupied_needed)
        return None

    #
    res = check_xs_for_y(3186981)
    print(f'{res=}')
    # abc = []
    # for y in range(4000001):
    #     abc.append(check_xs_for_y(y))
    # abc = list(filter(lambda ab: ab is not None, abc))
    # print(abc)
    # print(f'{res=}')
    # with Pool(11) as p:
    #     print(list(filter(lambda res: res is not None, p.map(check_xs_for_y, range(4000001)))))
    free_spaces = list(free_spaces)
    return free_spaces[0][0] * 4000000 + free_spaces[0][1]


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
        # print(f'part 1 for {filename}')
        # print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print()
