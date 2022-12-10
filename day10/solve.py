with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def part_1():
    results = []
    optimized = []
    for i in lines:
        if i == 'noop':
            optimized.append(i)
        else:
            optimized.append('noop')
            optimized.append(' '.join(['add_to_x', *i.split()[1:]]))
    cycle = 1
    x_register = 1
    for line in optimized:
        if cycle in [20, 60, 100, 140, 180, 220]:
            results.append(cycle * x_register)
        if line == 'noop':
            cycle += 1
        elif line.startswith('add_to_x'):
            cmd, arg = line.split()
            cycle += 1
            x_register += int(arg)
    return sum(results)


def part_2():
    optimized = []
    for i in lines:
        if i == 'noop':
            optimized.append(i)
        else:
            optimized.append('noop')
            optimized.append(' '.join(['add_to_x', *i.split()[1:]]))
    grid = [[' ' for _ in range(40)] for _ in range(6)]
    cycle = 1
    x_register = 1
    for line in optimized:
        grid_row = (cycle - 1) // 40
        x = (cycle - 1) % 40
        if grid[grid_row][x] == ' ':
            if x_register - 1 <= x <= x_register + 1:
                grid[grid_row][x] = '#'
        if line == 'noop':
            cycle += 1
        elif line.startswith('add_to_x'):
            cmd, arg = line.split()
            cycle += 1
            x_register += int(arg)
    print(*[''.join(map(str, i)).replace(' ', '.') for i in grid], sep='\n')


print(part_1())
part_2()