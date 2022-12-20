from collections.abc import MutableMapping

with open('input.txt') as f:
    lines = f.readlines()
lines = [i.strip() for i in lines]


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten(dictionary):
    resultDict = dict()
    for key, value in dictionary.items():
        parts = key.split("/")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict


def part_1():
    result = 0

    disk = {
        '/': {}
    }
    cwd = '~'
    for line_ind, i in enumerate(lines):

        if i.startswith('$ cd'):
            _, cmd, args = i.split()
            if args == '/':
                cwd = '/'
            elif args == '..':
                cwd = '/'.join(cwd.split('/')[:-2])
                cwd += '/'
            else:
                cwd += f'{args}/'
                if cwd not in disk:
                    disk[cwd] = {}
        elif i.startswith('$ ls'):
            output = []
            for x_ind, x in enumerate(lines[line_ind + 1:]):
                if x.startswith('$'):
                    break
                else:
                    output.append(x)
            for x in output:
                f_type, f_name = x.split()
                if f_type == 'dir':
                    if cwd + f_name + '/' not in disk:
                        disk[cwd + f_name + '/'] = {}
                else:
                    if f_name not in disk[cwd]:
                        disk[cwd][f_name] = int(f_type)
    dir_sizes = {}
    for k, v in disk.items():
        dir_size = 0
        if v:
            for in_kv, in_v in v.items():
                if isinstance(in_v, int):
                    dir_size += in_v
        dir_sizes[k] = dir_size
    for k in dir_sizes.keys():
        for in_k, in_v in dir_sizes.items():

            if in_k == k:
                continue
            if in_k.startswith(k):
                dir_sizes[k] += in_v
    for k, v in dir_sizes.items():
        if v <= 100000:
            result += v
    return result


def part_2():
    result = 0
    total_disk_size = 70000000
    minimum_needed = 30000000

    disk = {
        '/': {}
    }
    cwd = '~'
    for line_ind, i in enumerate(lines):

        if i.startswith('$ cd'):
            _, cmd, args = i.split()
            if args == '/':
                cwd = '/'
            elif args == '..':
                cwd = '/'.join(cwd.split('/')[:-2])
                cwd += '/'
            else:
                cwd += f'{args}/'
                if cwd not in disk:
                    disk[cwd] = {}
        elif i.startswith('$ ls'):
            output = []
            for x_ind, x in enumerate(lines[line_ind + 1:]):
                if x.startswith('$'):
                    break
                else:
                    output.append(x)
            for x in output:
                f_type, f_name = x.split()
                if f_type == 'dir':
                    if cwd + f_name + '/' not in disk:
                        disk[cwd + f_name + '/'] = {}
                else:
                    if f_name not in disk[cwd]:
                        disk[cwd][f_name] = int(f_type)
    dir_sizes = {}
    for k, v in disk.items():
        dir_size = 0
        if v:
            for in_kv, in_v in v.items():
                if isinstance(in_v, int):
                    dir_size += in_v
        dir_sizes[k] = dir_size
    for k in dir_sizes.keys():
        for in_k, in_v in dir_sizes.items():
            if in_k == k:
                continue
            if in_k.startswith(k):
                dir_sizes[k] += in_v
    current_taken_space = dir_sizes['/']
    unused_space = total_disk_size - current_taken_space
    space_to_clean = minimum_needed - unused_space
    dir_to_clean = '/'
    for k, v in dir_sizes.items():
        if space_to_clean <= v < dir_sizes[dir_to_clean]:
            dir_to_clean = k
    return dir_sizes[dir_to_clean]


print(part_1())
print(part_2())
