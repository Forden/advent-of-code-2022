with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    result = 0
    for ind, i in enumerate(range(0, len(lines[0]) - 3, 1)):
        sector = lines[0][i:i + 4]
        print(sector)
        if len(set([*lines[0][i:i + 4]])) == len([*lines[0][i:i + 4]]):
            result = ind
            break
    return result + 4


def part_2():
    result = 0
    return result


print(part_1())
print(part_2())
