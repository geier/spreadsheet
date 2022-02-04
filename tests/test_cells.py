from spread.cells import cellname_to_indices, from_rst

class Test_cellname_to_indices:
    def test_basic(self):
        assert cellname_to_indices('A1') == (0, 0)
        assert cellname_to_indices('B1') == (1, 0)
        assert cellname_to_indices('C19') == (2, 18)

    def test_double(self):
        assert cellname_to_indices('AA1') == (26, 0)
        assert cellname_to_indices('AC151') == (28, 150)


class TestTable:
    def test_basic(self):
        with open('tests/example_table_plain.rst') as file:
            table = from_rst(file.read())
        table.render()

        import pdb; pdb.set_trace()


