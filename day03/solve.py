import string

with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def get_item_priority(item: str):
    return string.ascii_letters.index(item) + 1


def part_1():
    priorities_score = 0

    for rucksack in lines:
        first_part, second_part = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
        intersection = set(first_part).intersection(set(second_part))
        for i in intersection:
            priorities_score += get_item_priority(i)

    return priorities_score


def part_2():
    priorities_score = 0

    for first_rucksack_id in range(0, len(lines), 3):
        rucksacks_group = lines[first_rucksack_id:first_rucksack_id + 3]
        intersection = set(rucksacks_group[0]).intersection(*rucksacks_group[1:])
        for i in intersection:
            priorities_score += get_item_priority(i)

    return priorities_score


print(part_1())
print(part_2())
