with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def adjust_tail_coords(tail_coord, head_coord):
    result_tail_coords = tail_coord.copy()
    x_difference = head_coord[0] - tail_coord[0]
    y_difference = head_coord[1] - tail_coord[1]
    if x_difference == 0 and y_difference == 0:
        pass  # overlap touch
    elif abs(x_difference) == 1 and abs(y_difference) == 1:
        pass  # diagonal touch
    else:
        if x_difference == 0:
            if y_difference == 0:
                pass
            elif y_difference == 1:
                pass
            elif y_difference == 2:
                result_tail_coords[1] += 1
            elif y_difference == -1:
                pass
            elif y_difference == -2:
                result_tail_coords[1] -= 1
        elif x_difference == 1:
            if y_difference == 0:
                pass
            elif y_difference == 1:
                pass
            elif y_difference == 2:
                result_tail_coords[0] += 1
                result_tail_coords[1] += 1
            elif y_difference == -1:
                pass
            elif y_difference == -2:
                result_tail_coords[0] += 1
                result_tail_coords[1] -= 1
        elif x_difference == 2:
            if y_difference == 0:
                result_tail_coords[0] += 1
            elif y_difference == 1:
                result_tail_coords[0] += 1
                result_tail_coords[1] += 1
            elif y_difference == 2:
                result_tail_coords[0] += 1
                result_tail_coords[1] += 1
            elif y_difference == -1:
                result_tail_coords[0] += 1
                result_tail_coords[1] -= 1
            elif y_difference == -2:
                result_tail_coords[0] += 1
                result_tail_coords[1] -= 1
        elif x_difference == -1:
            if y_difference == 0:
                pass
            elif y_difference == 1:
                pass
            elif y_difference == 2:
                result_tail_coords[0] -= 1
                result_tail_coords[1] += 1
            elif y_difference == -1:
                pass
            elif y_difference == -2:
                result_tail_coords[0] -= 1
                result_tail_coords[1] -= 1
        elif x_difference == -2:
            if y_difference == 0:
                result_tail_coords[0] -= 1
            elif y_difference == 1:
                result_tail_coords[0] -= 1
                result_tail_coords[1] += 1
            elif y_difference == 2:
                result_tail_coords[0] -= 1
                result_tail_coords[1] += 1
            elif y_difference == -1:
                result_tail_coords[0] -= 1
                result_tail_coords[1] -= 1
            elif y_difference == -2:
                result_tail_coords[0] -= 1
                result_tail_coords[1] -= 1
    return result_tail_coords


def part_1():
    tail_visited_coords = []
    head_coords = [0, 0]
    tail_coords = [0, 0]
    tail_visited_coords.append(tail_coords.copy())
    for line in lines:
        cmd, size = line.split()
        size = int(size)
        for _ in range(size):
            if cmd == 'R':
                head_coords[0] += 1
            elif cmd == 'U':
                head_coords[1] += 1
            elif cmd == 'L':
                head_coords[0] -= 1
            elif cmd == 'D':
                head_coords[1] -= 1
            tail_coords = adjust_tail_coords(tail_coords, head_coords)
            tail_visited_coords.append(tail_coords.copy())
    return len(set(map(tuple, tail_visited_coords)))


def part_2():
    tail_visited_coords = []
    rope_coords = [[0, 0] for _ in range(10)]
    tail_visited_coords.append(rope_coords[-1].copy())
    for line in lines:
        cmd, size = line.split()
        size = int(size)
        for _ in range(size):
            if cmd == 'R':
                rope_coords[0][0] += 1
            elif cmd == 'U':
                rope_coords[0][1] += 1
            elif cmd == 'L':
                rope_coords[0][0] -= 1
            elif cmd == 'D':
                rope_coords[0][1] -= 1
            for part_ind, part in enumerate(rope_coords):
                if part_ind == 0:
                    pass
                else:
                    rope_coords[part_ind] = adjust_tail_coords(part, rope_coords[part_ind - 1])
            tail_visited_coords.append(rope_coords[-1].copy())
    return len(set(map(tuple, tail_visited_coords)))


print(f'{part_1()=}')
print(f'{part_2()=}')
