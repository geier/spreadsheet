import pytest

from spread.cells import from_rst
from spread.helper import cellname_to_indices, range_to_cells

class Test_cellname_to_indices:
    def test_basic(self):
        assert cellname_to_indices('A1') == (0, 0)
        assert cellname_to_indices('B1') == (1, 0)
        assert cellname_to_indices('C19') == (2, 18)

    def test_double(self):
        assert cellname_to_indices('AA1') == (26, 0)
        assert cellname_to_indices('AC151') == (28, 150)


class Test_range_to_cells:
    def test_equal(self):
        assert range_to_cells('A1', 'A1') == [(0, 0)]
        assert range_to_cells('AC23', 'AC23') == [(28, 22)]

    def test_row_range(self):
        #                                      B  4    C  4    D  4    E  4    F  4
        assert range_to_cells('B4', 'F4') == [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)]

    def test_col_range(self):
        assert range_to_cells('F3', 'F9') == [(5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)]

    def test_area_range(self):
        assert range_to_cells('B3', 'F9') ==  [
            (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
            (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
            (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
            (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),
            (1, 8), (2, 8), (3, 8), (4, 8), (5, 8),
        ] 


class TestTable:
    def test_basic(self):
        with open('tests/example_table_plain.rst') as file:
            table = from_rst(file.read())
        assert table['D5'].value == 21.5
        assert table['D6'].value == pytest.approx(7.16, 0.01)
        assert table['D7'].value == pytest.approx(7.16, 0.01)
        assert table['D8'].value == pytest.approx(7.16, 0.01)

