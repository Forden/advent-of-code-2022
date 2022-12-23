import typing

T = typing.TypeVar('T')


def get_neighbours_in_2d_list(
        grid: typing.List[typing.List[T]], row_ind: int, cell_ind: int
) -> typing.List[typing.Tuple[int, int]]:
    """
    Returns coords of current cell neighbours
    :param grid:
    :param row_ind:
    :param cell_ind:
    :return:
    """
    res = []
    rows_amount = len(grid)
    cell_amount = len(grid[0])
    x_s, y_s = [cell_ind - 1, cell_ind, cell_ind + 1], [row_ind - 1, row_ind, row_ind + 1]
    for x in x_s:
        for y in y_s:
            if y < 0 or x < 0:
                continue
            if y > rows_amount - 1:
                continue
            if x > cell_amount - 1:
                continue
            if y == row_ind and x == cell_ind:
                continue
            res.append((x, y))
    return res
