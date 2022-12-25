import typing


def part_1(input_lines: typing.List[str]) -> typing.Union[int, str]:
    def snafu_to_10(snafu: str) -> int:
        res = 0
        for ind, i in enumerate(reversed(snafu)):
            v = 5 ** ind
            res += sn_digit_to_digit[i] * v
            # print(ind, i, v)
        return res

    def dec_to_snafu(x: int) -> typing.List[str]:
        res = []
        if x == 0:
            return []
        elif x % 5 == 0:
            return ['0'] + dec_to_snafu(x // 5)
        elif x % 5 == 1:
            return ['1'] + dec_to_snafu(x // 5)
        elif x % 5 == 2:
            return ['2'] + dec_to_snafu(x // 5)
        elif x % 5 == 3:
            return ['='] + dec_to_snafu((x+2) // 5)
        elif x % 5 == 4:
            return ['-'] + dec_to_snafu((x + 2) // 5)

    digits = ['2', '1', '0', '-', '=']
    sn_digit_to_digit = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }
    print(snafu_to_10('2-=2==00-0==2=022=10'))
    print(sum(map(snafu_to_10, input_lines)))
    # print(''.join(dec_to_snafu(4890)))
    return ''.join(reversed(dec_to_snafu(sum(map(snafu_to_10, input_lines)))))


def part_2(input_lines: typing.List[str]) -> typing.Union[int, str]:
    result = 0
    return result


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
        'sample.txt',
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
