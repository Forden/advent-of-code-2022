import typing


def chunks(list_to_split, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i:i + chunk_size]


def part_1(input_lines: typing.List[str]):
    inspected_by_monkeys = []
    monkeys_items = []
    for i in input_lines:
        if i.startswith('Monkey'):
            monkeys_items.append([])
            inspected_by_monkeys.append(0)
    for monkey_data in chunks(input_lines, 7):
        monkey_id = int(monkey_data[0].split()[1][:-1])
        items = list(map(int, monkey_data[1].split(':')[1].strip().split(', ')))
        monkeys_items[monkey_id] = items.copy()
    for _ in range(20):
        for monkey_data in chunks(input_lines, 7):
            monkey_id = int(monkey_data[0].split()[1][:-1])
            items = monkeys_items[monkey_id].copy()
            inspected_by_monkeys[monkey_id] += len(items)
            operation = monkey_data[2].split('=')[1].strip().split()[1]
            operation_value = monkey_data[2].split('=')[1].strip().split()[2]
            divisible_by = int(monkey_data[3].split()[-1])
            if_true = int(monkey_data[4].split()[-1])
            if_false = int(monkey_data[5].split()[-1])
            for item in items:
                if operation_value == 'old':
                    second_operator = item
                else:
                    second_operator = int(operation_value)
                if operation == '*':
                    worry = item * second_operator
                elif operation == '+':
                    worry = item + second_operator
                worry = int(worry // 3)
                monkeys_items[monkey_id] = monkeys_items[monkey_id][1:]
                if worry % divisible_by == 0:
                    monkeys_items[if_true].append(worry)
                else:
                    monkeys_items[if_false].append(worry)
    result = 1
    inspected_by_monkeys = sorted(inspected_by_monkeys, reverse=True)
    for i in range(2):
        result *= inspected_by_monkeys[i]
    return result


def part_2(input_lines: typing.List[str]):
    inspected_by_monkeys = []
    monkeys_items = []
    monkey_datas = []
    for i in input_lines:
        if i.startswith('Monkey'):
            monkeys_items.append([])
            monkey_datas.append([])
            inspected_by_monkeys.append(0)
    for monkey_data in chunks(input_lines, 7):
        monkey_id = int(monkey_data[0].split()[1][:-1])
        items = list(map(int, monkey_data[1].split(':')[1].strip().split(', ')))
        monkeys_items[monkey_id] = items.copy()
        monkey_datas[monkey_id] = {
            'monkey_id':       int(monkey_data[0].split()[1][:-1]),
            'items':           items.copy(),
            'operation':       monkey_data[2].split('=')[1].strip().split()[1],
            'operation_value': monkey_data[2].split('=')[1].strip().split()[2],
            'divisible_by':    int(monkey_data[3].split()[-1]),
            'if_true':         int(monkey_data[4].split()[-1]),
            'if_false':        int(monkey_data[5].split()[-1])
        }
    common_divider = 1
    all_dividers = [i['divisible_by'] for i in monkey_datas]
    for i in all_dividers:
        common_divider = common_divider * i
    for _ in range(10000):
        for monkey_data in monkey_datas:
            monkey_id = monkey_data['monkey_id']
            items = monkeys_items[monkey_id]
            inspected_by_monkeys[monkey_id] += len(items)
            operation = monkey_data['operation']
            operation_value = monkey_data['operation_value']
            divisible_by = monkey_data['divisible_by']
            if_true = monkey_data['if_true']
            if_false = monkey_data['if_false']
            for item in items:
                if operation_value == 'old':
                    second_operator = item
                else:
                    second_operator = int(operation_value)
                if operation == '*':
                    worry = item * second_operator
                elif operation == '+':
                    worry = item + second_operator
                worry %= common_divider
                monkeys_items[monkey_id] = monkeys_items[monkey_id][1:]
                if worry % divisible_by == 0:
                    monkeys_items[if_true].append(worry)
                else:
                    monkeys_items[if_false].append(worry)

    result = 1
    inspected_by_monkeys = sorted(inspected_by_monkeys, reverse=True)
    for i in range(2):
        result *= inspected_by_monkeys[i]
    return result


def read_file_lines(filename: str, strip: bool = True) -> typing.List[str]:
    with open(filename) as f:
        lines = f.readlines()

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
        if not file_content:
            print(f'nothing in file {filename}, skipping')
        print(f'part 1 for {filename}')
        print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print()
