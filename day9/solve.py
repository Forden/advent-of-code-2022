with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    def adjust_tail_coords(tail_coord, head_coord):
        print(f'start adj {head_coord=} {tail_coord=}')
        result_tail_coords = tail_coord.copy()
        x_difference = head_coord[0] - tail_coord[0]
        y_difference = head_coord[1] - tail_coord[1]
        if x_difference == 0 and y_difference == 0:
            print('overlap')
            pass  # overlap touch
        elif abs(x_difference) == 1 and abs(y_difference) == 1:
            print('diagonal touch')
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
                    pass
                elif y_difference == -1:
                    result_tail_coords[0] += 1
                    result_tail_coords[1] -= 1
                elif y_difference == -2:
                    pass
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
                    pass
                elif y_difference == -1:
                    result_tail_coords[0] -= 1
                    result_tail_coords[1] -= 1
                elif y_difference == -2:
                    pass

            print(x_difference, y_difference)
            print('else')
        pass
        return result_tail_coords

    result = 0
    tail_visited_coords = []
    head_visited_coords = []
    head_coords = [0, 0]
    tail_coords = [0, 0]
    max_x, max_y = 6, 5
    tail_visited_coords.append(tail_coords.copy())
    head_visited_coords.append(head_coords.copy())
    for line in lines:
        cmd, size = line.split()
        size = int(size)
        print(cmd, size)
        for _ in range(size):
            if cmd == 'R':
                head_coords[0] += 1
            elif cmd == 'U':
                head_coords[1] += 1
            elif cmd == 'L':
                head_coords[0] -= 1
            elif cmd == 'D':
                head_coords[1] -= 1
            # print(head_coords)

            # print('a', f'{tail_coords=}, {head_coords=}')
            tail_coords = adjust_tail_coords(tail_coords, head_coords)
            # x_difference = head_coords[0] - tail_coords[0]
            # y_difference = head_coords[1] - tail_coords[1]
            # if x_difference == 0 and y_difference == 0:
            #     pass  # overlap touch
            # elif abs(x_difference) == 1 and abs(y_difference) == 1:
            #     pass  # diagonal touch
            #
            # if tail_coords[0] == head_coords[0]:
            #     pass
            # elif tail_coords[0] < head_coords[0] - 1:
            #     tail_coords[0] += 1
            # elif tail_coords[0] > head_coords[0] + 1:
            #     tail_coords[0] -= 1
            #
            # if tail_coords[1] < head_coords[1] - 1:
            #     tail_coords[1] += 1
            # elif tail_coords[1] > head_coords[1] + 1:
            #     tail_coords[1] -= 1
            # else:
            #     pass
            if head_coords[0] > max_x:
                max_x = head_coords[0]
            if head_coords[1] > max_y:
                max_y = head_coords[1]

            # print('b', f'{tail_coords=}, {head_coords=}')
            head_visited_coords.append(head_coords.copy())
            tail_visited_coords.append(tail_coords.copy())
            # print('x', f'{head_visited_coords=}')
        # print('step', head_coords, tail_coords)
        for y in range(max_y - 1, -1, -1):
            s = ''
            for x in range(max_x):
                if (x, y) == tuple(head_coords):
                    s += 'H'
                elif (x, y) == tuple(tail_coords):
                    s += 'T'
                elif (x, y) == (0, 0):
                    s += 's'
                else:
                    s += '.'
            # print(s)
    unique_tail_visited_coords = list(set(map(tuple, tail_visited_coords)))
    print(max_x, max_y)
    for y in range(max_y - 1, -1, -1):
        s = ''
        for x in range(max_x):
            if (x, y) == (0, 0):
                s += 's'
            elif (x, y) in unique_tail_visited_coords:
                s += '#'
            else:
                s += '.'
        print(s)
    # print(list(head_visited_coords))
    # print(list(tail_visited_coords))
    # print(list(map(tuple, tail_visited_coords)))
    return len(set(map(tuple, tail_visited_coords)))


def part_2():
    result = 0
    return result


print(part_1())
print(part_2())
