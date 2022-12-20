with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def get_result(sector_size, line):
    for ind, i in enumerate(range(0, len(line) - (sector_size - 1), 1)):
        sector = line[i:i + sector_size]
        if len({*sector}) == len([*sector]):
            return ind + sector_size


def part_1():
    result = get_result(4, lines[0])
    return result


def part_2():
    result = get_result(14, lines[0])
    return result


print(part_1())
print(part_2())
