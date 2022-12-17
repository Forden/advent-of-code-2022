import typing

T = typing.TypeVar('T')


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    graph = {}
    valves_rates = {}
    valve_to_num = {}
    num_to_valve = {}
    for i in input_lines:
        _, name, _, _, rate_raw = i.split('; ')[0].split()
        rate = int(rate_raw.split('=')[1])
        second_part = i.split('; ')[1].split()
        second_part = second_part[4:]
        valves_rates[name] = rate
        graph[name] = list(map(lambda x: x.rstrip(','), second_part))
    for k in sorted(graph.keys()):
        valve_to_num[k] = len(valve_to_num.values()) + 1
        num_to_valve[len(valve_to_num.values())] = k

    TOTAL_TIME = 30

    states: list[tuple[int, set, int]] = [
        (
            valve_to_num['AA'], set(
                filter(
                    lambda x: valves_rates[num_to_valve[x]] <= 0,
                    [valve_to_num[i] for i in valve_to_num]
                )
            ),
            0
        )
    ]  # open all zero valves
    best_orders = {}

    # cursed bfs
    for t in range(1, TOTAL_TIME + 1):
        new_states = []
        for current_location, opened, total_pressure_released in states:
            key = (current_location, ','.join(map(str, opened)))
            if key in best_orders:
                if total_pressure_released <= best_orders[key]:
                    continue
                else:
                    pass

            best_orders[key] = total_pressure_released

            flow_rate = valves_rates[num_to_valve[current_location]]
            children = graph[num_to_valve[current_location]]
            if current_location in opened:
                pass
            elif flow_rate <= 0:
                pass
            else:
                new_states.append(
                    (
                        current_location,
                        opened.union({current_location}),
                        total_pressure_released + flow_rate * (TOTAL_TIME - t)
                    )
                )
            for dest in children:
                new_states.append((valve_to_num[dest], opened, total_pressure_released))
        states = new_states
    return max(best_orders.values())


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    graph = {}
    valves_rates = {}
    valve_to_num = {}
    num_to_valve = {}
    for i in input_lines:
        _, name, _, _, rate_raw = i.split('; ')[0].split()
        rate = int(rate_raw.split('=')[1])
        second_part = i.split('; ')[1].split()
        second_part = second_part[4:]
        valves_rates[name] = rate
        graph[name] = list(map(lambda x: x.rstrip(','), second_part))
    for k in sorted(graph.keys()):
        valve_to_num[k] = len(valve_to_num.values()) + 1
        num_to_valve[len(valve_to_num.values())] = k

    TOTAL_TIME = 26

    states: list[tuple[int, set, int]] = [
        (
            valve_to_num['AA'],
            set(
                filter(
                    lambda x: valves_rates[num_to_valve[x]] <= 0,
                    [valve_to_num[i] for i in valve_to_num]
                )
            ),
            0
        )
    ]  # open all zero valves
    best_orders = {}

    # cursed bfs
    for t in range(1, TOTAL_TIME + 1):
        new_states = []
        for current_location, opened, total_pressure_released in states:
            key = (current_location, ','.join(map(str, opened)))
            if key in best_orders:
                if total_pressure_released <= best_orders[key]:
                    continue
                else:
                    pass

            best_orders[key] = total_pressure_released

            flow_rate = valves_rates[num_to_valve[current_location]]
            children = graph[num_to_valve[current_location]]
            if current_location in opened:
                pass
            elif flow_rate <= 0:
                pass
            else:
                new_states.append(
                    (
                        current_location,
                        opened.union({current_location}),
                        total_pressure_released + flow_rate * (TOTAL_TIME - t)
                    )
                )
            for dest in children:
                new_states.append((valve_to_num[dest], opened, total_pressure_released))
        states = new_states
    best_pressure = max(best_orders.values())
    for k, v in best_orders.items():
        if v == best_pressure:
            key = k
    states: list[tuple[int, set, int]] = [
        (
            valve_to_num['AA'],
            set(
                filter(
                    lambda x: valves_rates[num_to_valve[x]] <= 0,
                    [valve_to_num[i] for i in valve_to_num]
                )
            ).union(set(map(int, key[1].split(',')))),
            best_pressure
        )
    ]
    for t in range(1, TOTAL_TIME + 1):
        new_states = []
        for current_location, opened, total_pressure_released in states:
            key = (current_location, ','.join(map(str, opened)))
            if key in best_orders:
                if total_pressure_released <= best_orders[key]:
                    continue
                else:
                    pass

            best_orders[key] = total_pressure_released

            flow_rate = valves_rates[num_to_valve[current_location]]
            children = graph[num_to_valve[current_location]]
            if current_location in opened:
                pass
            elif flow_rate <= 0:
                pass
            else:
                new_states.append(
                    (
                        current_location,
                        opened.union({current_location}),
                        total_pressure_released + flow_rate * (TOTAL_TIME - t)
                    )
                )
            for dest in children:
                new_states.append((valve_to_num[dest], opened, total_pressure_released))
        states = new_states
    return max(best_orders.values())


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
