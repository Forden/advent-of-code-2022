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
    print(f'{valve_to_num=}')
    print(f'{num_to_valve=}')
    print(f'{graph=}')

    TOTAL_TIME = 30

    states: list[tuple[int, set, int]] = [(valve_to_num['AA'], set(), 0)]
    best_orders = {}

    # cursed bfs
    for t in range(1, TOTAL_TIME + 1):
        print(f'{t=}, {len(states)=} {states=}')

        new_states = []
        for current_location, opened, total_pressure_released in states:
            print(f'{current_location=}, {opened=}, {total_pressure_released=}')
            key = (current_location, ','.join(map(str, opened)))
            if key in best_orders:
                if total_pressure_released <= best_orders[key]:
                    print('skipped because already checked and no better')
                    continue
                else:
                    print(f'found better order with {total_pressure_released=} (old pressure={best_orders[key]})')

            best_orders[key] = total_pressure_released

            flow_rate = valves_rates[num_to_valve[current_location]]
            children = graph[num_to_valve[current_location]]
            if current_location in opened:
                print('skipping because already opened')
            elif flow_rate <= 0:
                print(f'skipping because {flow_rate=}')
            else:
                print(
                    f'opening, pressure += {flow_rate * (TOTAL_TIME - t)} with new presssure={total_pressure_released + flow_rate * (TOTAL_TIME - t)}'
                )
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
    answer = max(pressure for _, _, pressure in states)
    return answer


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
