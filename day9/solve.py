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
    pass
    return result_tail_coords


def part_1():
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

    return len(set(map(tuple, tail_visited_coords)))


def part_2():
    def print_rope(m_x, m_y, rope):
        grid = [['.' for _ in range(m_x)] for _ in range(m_y)]
        print('---')
        for part_ind, part in enumerate(rope):
            for y in range(m_y - 1, -1, -1):
                for x in range(m_x):
                    if (x, y) == tuple(part):
                        print(x, y, part, part_ind)
                        if grid[m_y - y - 1][x] in ['.', 's']:
                            if part_ind == 0:
                                grid[m_y - y - 1][x] = 'H'
                            else:
                                grid[m_y - y - 1][x] = part_ind
                    elif (x, y) == (0, 0):
                        grid[m_y - y - 1][x] = 's'
        print(*[''.join(map(str, i)) for i in grid], sep='\n')
        print('---')
    result = 0
    result = 0
    tail_visited_coords = []
    head_visited_coords = []
    rope_coords = [[0, 0] for _ in range(10)]
    head_coords = [0, 0]
    tail_coords = [0, 0]
    min_x, min_y = 0, 0
    max_x, max_y = 7, 10
    tail_visited_coords.append(rope_coords[-1].copy())
    head_visited_coords.append(head_coords.copy())
    for line in lines:
        cmd, size = line.split()
        size = int(size)
        print(cmd, size)
        for _ in range(size):
            if cmd == 'R':
                rope_coords[0][0] += 1
            elif cmd == 'U':
                rope_coords[0][1] += 1
            elif cmd == 'L':
                rope_coords[0][0] -= 1
            elif cmd == 'D':
                rope_coords[0][1] -= 1
            if rope_coords[0][0] > max_x:
                max_x = rope_coords[0][0]
            if rope_coords[0][0] < min_x:
                min_x = rope_coords[0][0]
            if rope_coords[0][1] > max_y:
                max_y = rope_coords[0][1]
            if rope_coords[0][1] < min_y:
                min_y = rope_coords[0][1]
            print(rope_coords)
            for part_ind, part in enumerate(rope_coords):
                if part_ind == 0:
                    pass
                else:

                    # print(f'{part_ind=} {rope_coords[part_ind - 1]=} {adjust_tail_coords(part, rope_coords[part_ind - 1])=}')
                    rope_coords[part_ind] = adjust_tail_coords(part, rope_coords[part_ind - 1])
            tail_visited_coords.append(rope_coords[-1].copy())
            # print_rope(max_x, max_y, rope_coords)
        print(rope_coords)
        grid = [['.' for _ in range(max_x)] for _ in range(max_y)]
        print('---')
        # for part_ind, part in enumerate(rope_coords):
        #     for y in range(max_y - 1, -1, -1):
        #         for x in range(max_x):
        #             if (x, y) == tuple(part):
        #                 print(x, y, part, part_ind)
        #                 if grid[max_y - y - 1][x] in ['.', 's']:
        #                     if part_ind == 0:
        #                         grid[max_y - y - 1][x] = 'H'
        #                     else:
        #                         grid[max_y - y - 1][x] = part_ind
        #             elif (x, y) == (0, 0):
        #                 grid[max_y - y - 1][x] = 's'
        # print(*[''.join(map(str, i)) for i in grid], sep='\n')
        # print('---')
    return len(set(map(tuple, tail_visited_coords)))


# print(f'{part_1()=}')
print(f'{part_2()=}')
