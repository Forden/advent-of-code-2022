with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    result = 0
    data = [[[int(i), False] for i in row] for row in lines]
    for tree_row_ind, tree_row in enumerate(data):
        for tree_in_row_ind, tree in enumerate(tree_row):
            if tree_row_ind == 0 or tree_row_ind == len(lines) - 1:
                result += 1
                tree[1] = True
            elif tree_in_row_ind == 0 or tree_in_row_ind == len(tree_row) - 1:
                result += 1
                tree[1] = True
            else:
                column = [i[tree_in_row_ind] for i in data]
                print(
                    f'tree={tree} up={column[:tree_row_ind]}, down={column[tree_row_ind + 1:]}, left={tree_row[:tree_in_row_ind]}, right={tree_row[tree_in_row_ind + 1:]}'
                )
                if all([i[0] < tree[0] for i in column[:tree_row_ind]]):
                    result += 1
                    tree[1] = True
                    print('x', tree)
                elif all([i[0] < tree[0] for i in column[tree_row_ind + 1:]]):
                    result += 1
                    tree[1] = True
                    print('y', tree)
                elif all([i[0] < tree[0] for i in tree_row[:tree_in_row_ind]]):
                    result += 1
                    tree[1] = True
                    print('z', tree)
                elif all([i[0] < tree[0] for i in tree_row[tree_in_row_ind + 1:]]):
                    result += 1
                    tree[1] = True
                    print('a', tree)
    # print()
    # print(*data, sep='\n')
    return result


def part_2():
    result = 0
    return result


print(part_1())
print(part_2())
