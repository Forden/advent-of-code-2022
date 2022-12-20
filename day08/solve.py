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
                if all([i[0] < tree[0] for i in column[:tree_row_ind]]):
                    result += 1
                    tree[1] = True
                elif all([i[0] < tree[0] for i in column[tree_row_ind + 1:]]):
                    result += 1
                    tree[1] = True
                elif all([i[0] < tree[0] for i in tree_row[:tree_in_row_ind]]):
                    result += 1
                    tree[1] = True
                elif all([i[0] < tree[0] for i in tree_row[tree_in_row_ind + 1:]]):
                    result += 1
                    tree[1] = True
    return result


def part_2():
    data = [[[int(i), False, 0] for i in row] for row in lines]
    for tree_row_ind, tree_row in enumerate(data):
        for tree_in_row_ind, tree in enumerate(tree_row):
            score = [0, 0, 0, 0]
            column = [i[tree_in_row_ind] for i in data]
            up = list(reversed(column[:tree_row_ind]))
            down = column[tree_row_ind + 1:]
            left = list(reversed(tree_row[:tree_in_row_ind]))
            right = tree_row[tree_in_row_ind + 1:]
            for i in up:
                if i[0] >= tree[0]:
                    score[0] += 1
                    break
                else:
                    score[0] += 1
            for i in down:
                if i[0] >= tree[0]:
                    score[2] += 1
                    break
                else:
                    score[2] += 1
            for i in left:
                if i[0] >= tree[0]:
                    score[1] += 1
                    break
                else:
                    score[1] += 1
            for i in right:
                if i[0] >= tree[0]:
                    score[3] += 1
                    break
                else:
                    score[3] += 1
            tree[2] = score[0] * score[1] * score[2] * score[3]
    max_score = 4
    for row in data:
        for tree in row:
            if tree[2] > max_score:
                max_score = tree[2]
    result = max_score
    return result


print(part_1())
print(part_2())
