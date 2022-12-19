import typing
from queue import Queue


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def solve(
            blueprint_config: typing.Dict[str, typing.Dict[str, int]],
            robots: typing.Dict[str, int],
            goods: typing.Dict[str, int]
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
        print(max_spent_per_minute)
        Q = Queue()
        Q.put((0, 0, 0, 0, 1, 0, 0, 0, 24))
        seen = set()
        best_geodes = -1
        while not Q.empty():
            checking = Q.get()

            ore_amount, clay_amount, obsidian_amount, geode_amount = checking[:4]
            ore_robots_amount, clay_robots_amount, obsidian_robots_amount, geode_robots_amount = checking[4:8]
            time_left = checking[8]
            best_geodes = max(best_geodes, geode_amount)

            if time_left == 0:
                # print('time out')
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
            # print(checking)
            if checking in seen:
                # print(f'seen {checking}')
                continue
            seen.add(checking)
            if len(seen) % 100000 == 0:
                print(time_left, best_geodes, len(seen))

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

    result = 0
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
        print(blueprints[blueprint_id])
    # print(max_spent_per_minute)
    print(blueprints)
    geodes_per_blueprint = {}
    TIME_TO_MINE = 24
    for blueprint_id, blueprint_config in blueprints.items():
        geodes_per_blueprint[blueprint_id] = solve(
            blueprint_config,
            {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0},
            {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        )
    # for blueprint_id, blueprint_config in blueprints.items():
    #     robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    #     goods = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    #     robot_to_be_added = None
    #     for i in range(1,TIME_TO_MINE+1):
    #         for robot_priority, robot in enumerate(reversed(list(blueprint_config.keys()))):
    #             if robots[robot] >= max_spent_per_minute[robot]:
    #                 print(f'too many of {robot} skipping')
    #                 continue
    #             robot_costs = blueprint_config[robot]
    #             print(f'checking  {robot} for cost {robot_costs}')
    #             possible_to_buy = True
    #             for good_type, amount in robot_costs.items():
    #                 if goods[good_type] < amount:
    #                     print(f'not enough of {good_type} needed {amount} has {goods[good_type]}')
    #                     possible_to_buy = False
    #                     break
    #             print(f'possible to buy = {possible_to_buy}')
    #             if possible_to_buy:
    #                 for good_type, amount in robot_costs.items():
    #                     goods[good_type] -= amount
    #                 robot_to_be_added = robot
    #                 if robot_to_be_added == 'geode':
    #                     print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    #                 break
    #         for robot, robot_amount in robots.items():
    #             if robot_amount:
    #                 goods[robot] += robot_amount
    #                 print(f'+{robot_amount} of {robot}')
    #         if robot_to_be_added is not None:
    #             robots[robot_to_be_added] += 1
    #             robot_to_be_added = None
    #         print(blueprint_id, i, goods, robots)
    #    geodes_per_blueprint[blueprint_id] = goods['geode']
    print(geodes_per_blueprint)
    result = sum([(k + 1) * v for k, v in geodes_per_blueprint.items()])
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
