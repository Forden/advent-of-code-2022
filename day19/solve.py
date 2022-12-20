import itertools
import time
import typing
from multiprocessing import Pool
from queue import Queue


def solve(
        blueprint_config: typing.Dict[str, typing.Dict[str, int]],
        time_to_finish: int
) -> int:
    max_spent_per_minute = {
        'ore':      max(
            blueprint_config['ore']['ore'],
            blueprint_config['clay']['ore'],
            blueprint_config['obsidian']['ore'],
            blueprint_config['geode']['ore'],
        ),
        'clay':     blueprint_config['obsidian']['clay'],
        'obsidian': blueprint_config['geode']['obsidian'],
        'geode':    100000000
    }
    Q = Queue()
    Q.put((0, 0, 0, 0, 1, 0, 0, 0, time_to_finish))
    seen = set()
    best_geodes = -1
    while not Q.empty():
        checking = Q.get()

        ore_amount, clay_amount, obsidian_amount, geode_amount = checking[:4]
        ore_robots_amount, clay_robots_amount, obsidian_robots_amount, geode_robots_amount = checking[4:8]
        time_left = checking[8]
        best_geodes = max(best_geodes, geode_amount)

        if time_left == 0:
            continue

        ore_robots_amount = min(ore_robots_amount, max_spent_per_minute['ore'])
        clay_robots_amount = min(clay_robots_amount, max_spent_per_minute['clay'])
        obsidian_robots_amount = min(obsidian_robots_amount, max_spent_per_minute['obsidian'])

        ore_amount = min(
            ore_amount,
            time_left * max_spent_per_minute['ore'] - ore_robots_amount * (time_left - 1)
        )
        clay_amount = min(
            clay_amount,
            time_left * max_spent_per_minute['clay'] - clay_robots_amount * (time_left - 1)
        )
        obsidian_amount = min(
            obsidian_amount,
            time_left * max_spent_per_minute['obsidian'] - obsidian_robots_amount * (time_left - 1)
        )

        checking = (
            ore_amount, clay_amount, obsidian_amount, geode_amount,
            ore_robots_amount, clay_robots_amount, obsidian_robots_amount, geode_robots_amount,
            time_left
        )
        assert ore_amount >= 0 and clay_amount >= 0 and obsidian_amount >= 0 and geode_amount >= 0, checking
        if checking in seen:
            continue
        seen.add(checking)
        # if len(seen) % 100000 == 0:
        #     print(time_left, best_geodes, len(seen))

        Q.put(
            (
                ore_amount + ore_robots_amount,
                clay_amount + clay_robots_amount,
                obsidian_amount + obsidian_robots_amount,
                geode_amount + geode_robots_amount,
                ore_robots_amount,
                clay_robots_amount,
                obsidian_robots_amount,
                geode_robots_amount,
                time_left - 1
            )
        )
        if ore_amount >= blueprint_config['ore']['ore']:
            Q.put(
                (
                    ore_amount + ore_robots_amount - blueprint_config['ore']['ore'],
                    clay_amount + clay_robots_amount,
                    obsidian_amount + obsidian_robots_amount,
                    geode_amount + geode_robots_amount,
                    ore_robots_amount + 1,
                    clay_robots_amount,
                    obsidian_robots_amount,
                    geode_robots_amount,
                    time_left - 1
                )
            )
        if ore_amount >= blueprint_config['clay']['ore']:
            Q.put(
                (
                    ore_amount + ore_robots_amount - blueprint_config['clay']['ore'],
                    clay_amount + clay_robots_amount,
                    obsidian_amount + obsidian_robots_amount,
                    geode_amount + geode_robots_amount,
                    ore_robots_amount,
                    clay_robots_amount + 1,
                    obsidian_robots_amount,
                    geode_robots_amount,
                    time_left - 1
                )
            )
        if (
                ore_amount >= blueprint_config['obsidian']['ore']
        ) and (
                clay_amount >= blueprint_config['obsidian']['clay']
        ):
            Q.put(
                (
                    ore_amount + ore_robots_amount - blueprint_config['obsidian']['ore'],
                    clay_amount + clay_robots_amount - blueprint_config['obsidian']['clay'],
                    obsidian_amount + obsidian_robots_amount,
                    geode_amount + geode_robots_amount,
                    ore_robots_amount,
                    clay_robots_amount,
                    obsidian_robots_amount + 1,
                    geode_robots_amount,
                    time_left - 1
                )
            )
        if (
                ore_amount >= blueprint_config['geode']['ore']
        ) and (
                obsidian_amount >= blueprint_config['geode']['obsidian']
        ):
            Q.put(
                (
                    ore_amount + ore_robots_amount - blueprint_config['geode']['ore'],
                    clay_amount + clay_robots_amount,
                    obsidian_amount + obsidian_robots_amount - blueprint_config['geode']['obsidian'],
                    geode_amount + geode_robots_amount,
                    ore_robots_amount,
                    clay_robots_amount,
                    obsidian_robots_amount,
                    geode_robots_amount + 1,
                    time_left - 1
                )
            )
    return best_geodes


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    blueprints = {}
    for blueprint_id, i in enumerate(input_lines):
        ore_robot, clay_robot, obsidian_robot, geode_robot, _ = list(
            map(
                lambda x: list(map(int, filter(lambda a: a.isdigit(), x.strip().split()[4:]))),
                i.split(':')[1].split('.')
            )
        )
        blueprints[blueprint_id] = {
            'ore':      {'ore': ore_robot[0]},
            'clay':     {'ore': clay_robot[0]},
            'obsidian': {'ore': obsidian_robot[0], 'clay': obsidian_robot[1]},
            'geode':    {'ore': geode_robot[0], 'obsidian': geode_robot[1]}
        }
    with Pool() as p:
        result = sum(
            map(
                lambda x: (x[0] + 1) * x[1],
                enumerate(
                    p.starmap(
                        solve,
                        zip(
                            blueprints.values(), itertools.repeat(24)
                        )
                    )
                )
            )
        )
    return result


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    blueprints = {}
    for blueprint_id, i in enumerate(input_lines[:3]):
        ore_robot, clay_robot, obsidian_robot, geode_robot, _ = list(
            map(
                lambda x: list(map(int, filter(lambda a: a.isdigit(), x.strip().split()[4:]))),
                i.split(':')[1].split('.')
            )
        )
        blueprints[blueprint_id] = {
            'ore':      {'ore': ore_robot[0]},
            'clay':     {'ore': clay_robot[0]},
            'obsidian': {'ore': obsidian_robot[0], 'clay': obsidian_robot[1]},
            'geode':    {'ore': geode_robot[0], 'obsidian': geode_robot[1]}
        }
    result = 1
    with Pool() as p:
        for i in p.starmap(solve, zip(blueprints.values(), itertools.repeat(32))):
            result *= i
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
        part_1_start = time.time()
        print(f'part 1 for {filename}')
        print(part_1(file_content.copy()))
        print(f'took {time.time() - part_1_start} sec')
        part_2_start = time.time()
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print(f'took {time.time() - part_2_start} sec')
        print()
