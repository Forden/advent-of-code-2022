import typing

T = typing.TypeVar('T')


def get_manhattan_distance(start: typing.Tuple[T, T], end: typing.Tuple[T, T]) -> T:
    diff_x, diff_y = abs(start[0] - end[0]), abs(start[1] - end[1])
    return diff_x + diff_y
