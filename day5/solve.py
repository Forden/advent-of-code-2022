with open('input.txt') as f:
    lines = f.readlines()
lines = [i.rstrip() for i in lines]


def chunks(list_to_split, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i:i + chunk_size]


def part_1():
    result = 0
    max_items_start = 1
    stacks_amount = 1
    for ind, i in enumerate(lines):
        if i.startswith(' 1'):
            max_items_start = ind
            stacks_amount = int(i.strip().split()[-1])
    for line_ind, i in enumerate(lines[:max_items_start + 2]):
        if len(i) < (stacks_amount * 3 + stacks_amount - 1):
            lines[line_ind] = i + ((stacks_amount * 3 + stacks_amount - 1) - len(i)) * ' '
        lines[line_ind] = i + ' '
    symbols_by_stack = [[] for _ in range(stacks_amount)]
    for i in lines[:max_items_start]:
        # print(i)
        symbols = [i[:-1] for i in chunks(list(i), 4)]
        for stack_ind, stack_symbols in enumerate(symbols):
            symbols_by_stack[stack_ind].append(stack_symbols)
    symbols_by_stack = [list(map(lambda x: x[1], filter(lambda x: x[1] != ' ', reversed(i)))) for i in symbols_by_stack]
    print(*symbols_by_stack, sep='\n')
    for cmd in lines[max_items_start + 2:]:
        _, amount_to_move, _, start_stack_ind, _, target_stack_ind = cmd.split()
        amount_to_move = int(amount_to_move)
        start_stack_ind, target_stack_ind = int(start_stack_ind) - 1, int(target_stack_ind) - 1
        for _ in range(amount_to_move):
            moving_pack = symbols_by_stack[start_stack_ind].pop()
            symbols_by_stack[target_stack_ind].append(moving_pack)
    print(*symbols_by_stack, sep='\n')

    return ''.join([i[-1] for i in symbols_by_stack])


def part_2():
    result = 0
    return result


print(part_1())
print(part_2())
