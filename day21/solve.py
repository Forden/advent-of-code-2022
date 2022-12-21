import typing


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    result = 0
    memory = {}
    while 'root' not in memory:
        for i in input_lines:
            monkey, data = i.split(': ')
            if data.isdigit():
                data = int(data)
                memory[monkey] = data
            else:
                first, oper, second = data.split()
                if first in memory and second in memory:
                    if oper == '+':
                        memory[monkey] = memory[first] + memory[second]
                    elif oper == '-':
                        memory[monkey] = memory[first] - memory[second]
                    elif oper == '/':
                        memory[monkey] = memory[first] / memory[second]
                    elif oper == '*':
                        memory[monkey] = memory[first] * memory[second]
                    else:
                        print('weird', monkey, data)

    return memory['root']


def part_2_test(input_lines: typing.List[str]) -> int:
    memory = {}
    while 'humn' not in memory:
        for i in input_lines:
            monkey, data = i.split(': ')
            if data.isdigit():
                data = int(data)
                memory[monkey] = data
            else:
                first, oper, second = data.split()
                if first in memory and second in memory:
                    if oper == '+':
                        memory[monkey] = memory[first] + memory[second]
                    elif oper == '-':
                        memory[monkey] = memory[first] - memory[second]
                    elif oper == '/':
                        memory[monkey] = memory[first] / memory[second]
                    elif oper == '*':
                        memory[monkey] = memory[first] * memory[second]
                    else:
                        print('weird', monkey, data)

    return memory['humn']


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    global check

    def check(checking: int) -> typing.Dict[str, typing.Union[int, float]]:
        memory = {}
        while 'root' not in memory:
            for i in input_lines:
                monkey, data = i.split(': ')
                if monkey == 'humn':
                    memory[monkey] = checking
                else:
                    if data.isdigit():
                        data = int(data)
                        memory[monkey] = data
                    else:
                        first, oper, second = data.split()
                        if monkey == 'root':
                            oper = '='
                        if first in memory and second in memory:
                            if oper == '+':
                                memory[monkey] = memory[first] + memory[second]
                            elif oper == '-':
                                memory[monkey] = memory[first] - memory[second]
                            elif oper == '/':
                                memory[monkey] = memory[first] / memory[second]
                            elif oper == '*':
                                memory[monkey] = memory[first] * memory[second]
                            elif oper == '=':
                                print(
                                    i,
                                    memory[first], memory[second],
                                    memory[first] > memory[second],
                                    memory[first] - memory[second]
                                )
                                memory[monkey] = memory[first] == memory[second]
                            else:
                                print('weird', monkey, data)
        return memory

    res = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    min_diff = 9999999999999999999999999999999
    for i in range(len(res)):
        print(res)
        i_to_set = 9
        for test_int in range(1 if i == 0 else 0, 10):
            imag = res
            imag[i] = str(test_int)
            test_res = check(int(''.join(imag)))
            if test_res['wrvq'] - test_res['vqfc'] == 0:
                return int(''.join(imag))
            if test_res['wrvq'] - test_res['vqfc'] < 0:
                break
            if test_res['wrvq'] - test_res['vqfc'] <= min_diff:
                min_diff = test_res['wrvq'] - test_res['vqfc']
                i_to_set = test_int
        res[i] = str(i_to_set)
    return 0


def read_file_lines(file_to_read: str, strip: bool = True) -> typing.List[str]:
    try:
        with open(file_to_read) as f:
            lines = f.readlines()
    except:
        return []
    if strip:
        lines = [i.strip() for i in lines]
    return lines.copy()


if __name__ == '__main__':
    files_to_run = [
        # 'sample.txt',
        'input.txt'
    ]
    for filename in files_to_run:
        file_content = read_file_lines(filename, strip=True)
        if len(file_content) == 0:
            print(f'nothing in file {filename}, skipping')
            continue
        print(f'part 1 for {filename}')
        print(part_1(file_content.copy()))
        print(f'part 2 for {filename}')
        print(part_2(file_content.copy()))
        print()
