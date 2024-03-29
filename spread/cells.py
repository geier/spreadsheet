from .helper import cellname_to_indices, range_to_cells
from typing import List, Tuple
from .evaluate import Evaluator

INT = 'int'
FLOAT = 'float'
STRING = 'string'
FORMULA = 'formula'


class Cell:
    def __init__(self, string):
        self._raw = string
        self.value = ''
        self.dtype = STRING
        while True:
            try:
                self.value = int(self._raw)
                self.dtype = INT
                break
            except ValueError:
                pass
            try:
                self.value = float(self._raw)
                self.dtype = FLOAT
                break
            except ValueError:
                pass
            try:
                if self._raw[0] == '=':
                    self.value = self._raw
                    self.dtype = FORMULA
                    break
            except (TypeError, IndexError):
                pass
            self.value = self._raw
            self.dtype = STRING
            break

    def __str__(self):
        return '<Cell: {}>'.format(self.value)

    def __repr__(self):
        return self.__str__()


class Table:
    def __init__(self, cells: List[List[Cell]]):
        self._cells = cells
        self.evaluate = Evaluator(self).evaluate

        for row in self._cells:
            for cell in row:
                if cell.dtype == FORMULA:
                    cell.value = self.evaluate(cell._raw[1:])


    def get_cell_range(self, rangestr: str) -> List[Cell]:
        assert isinstance(rangestr, str)
        assert ':' in rangestr

        cell_indices = range_to_cells(*rangestr.split(':'))
        try:
            rval = [self._cells[row_i][column_i] for column_i, row_i in cell_indices]
        except IndexError:
            raise IndexError(f'range {rangestr} out of range')
        return rval

    def __getitem__(self, cellname):
        assert isinstance(cellname, str)
        column_i, row_i = cellname_to_indices(cellname)
        try:
            cell = self._cells[row_i][column_i]
        except IndexError:
            raise IndexError(f'cellname {cellname} out of range')
        else:
            return cell

    def get_widths(self):
        # TODO
        return [10] * len(self._cells[0])

    def render(self):
        widths = self.get_widths()
        hline = '+' + '+'.join(['-' * width for width in widths]) + '+'
        out = list()
        out.append(hline)
        for row in self._cells:
            out_row = list()
            for width, cell in zip(widths, row):
                cell_formatted = str(cell.value).ljust(width)[:width]
                out_row.append(cell_formatted)
            out.append('|' + '|'.join(out_row) + '|')
            out.append(hline)
        return '\n'.join(out)


def from_rst(table, separator='|'):
    rows = list()
    for line in table.splitlines():
        if line == '':
            continue
        if line.strip('+-=') == '':  # separation line
            continue
        if line[0] == separator:
            line = line[1:]
        if line[-1] == separator:
            line = line[:-1]
        rows.append([Cell(element.strip()) for element in line.split(separator)])
    return Table(rows)
