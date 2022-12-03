import string

with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    priorities_score = 0

    def get_item_priority(item: str):
        return string.ascii_letters.index(item) + 1

    for rucksack in lines:
        first_part, second_part = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
        intersection = set(first_part).intersection(set(second_part))
        for i in intersection:
            priorities_score += get_item_priority(i)

    return priorities_score


print(part_1())
