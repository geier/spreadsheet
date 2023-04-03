from typing import Tuple, List

column_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def cellname_to_indices(cellname: str) -> Tuple[int, int]:
    column_name = cellname.strip('01234567890')
    row_name = cellname.strip(column_labels)
    row_index = int(row_name) - 1

    column_index = 0
    for index in range(len(column_name)):
        column_index *= len(column_labels)**index
        column_index += ord(column_name[index]) - 64
    column_index -= 1
    return column_index, row_index


def range_to_cells(cellname1: str, cellname2: str) -> List[Tuple[int, int]]:
    col_index_1, row_index_1 = cellname_to_indices(cellname1)
    col_index_2, row_index_2 = cellname_to_indices(cellname2)

    if col_index_1 == col_index_2 and row_index_1 == row_index_2:
        return [(col_index_1, row_index_1)]

    if col_index_1 > col_index_2:
        raise ValueError('col_index_2 must be larger than col_index_1')
    if row_index_1 > row_index_2:
        raise ValueError('row_index_2 must be larger than row_index_1')

    if row_index_2 > row_index_1:
        row_indices = range(row_index_1, row_index_2 + 1)
    else:
        row_indices = [row_index_1]

    rlist = list()
    for row_index in row_indices:
        if col_index_1 == col_index_2:
            rlist.append((col_index_1, row_index))
        else:
            for col_index in range(col_index_1, col_index_2 + 1):
                rlist.append((col_index, row_index))
    return rlist
