with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    result = 0
    for pair in lines:
        first, second = pair.split(',')
        first_range = tuple(map(int, first.split('-')))
        second_range = tuple(map(int, second.split('-')))
        if first_range[0] >= second_range[0] and first_range[1] <= second_range[1]:
            result += 1
        elif first_range[0] <= second_range[0] and first_range[1] >= second_range[1]:
            result += 1
        else:
            pass
    return result


def part_2():
    result = 0
    for pair in lines:
        first, second = pair.split(',')
        first_range = tuple(map(int, first.split('-')))
        second_range = tuple(map(int, second.split('-')))
        if set(
                [i for i in range(first_range[0], first_range[1] + 1, 1)]
        ).intersection(
            [i for i in range(second_range[0], second_range[1] + 1, 1)]
        ):
            result += 1
    return result


print(part_1())
print(part_2())
