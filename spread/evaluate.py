from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { CELL, NUMBER, RANGE, SUM, AVG}
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', ':'}

    # Tokens (order matters!)
    RANGE = r'[A-Z][0-9]\:[A-Z][0-9]'
    CELL = r'[A-Z]{1,2}[0-9]+'
    SUM = "SUM"
    AVG = "AVG"

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self, table):
        self.names = { }
        self._table = table

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('CELL')
    def expr(self, p):
        return self._table[p.CELL].value

    @_('SUM "(" RANGE ")"')
    def expr(self, p):
        return sum(cell.value for cell in self._table.get_cell_range(p.RANGE))

    @_('AVG "(" RANGE ")"')
    def expr(self, p):
        cells = self._table.get_cell_range(p.RANGE)
        print(len(cells))
        print(cells)
        return sum(cell.value for cell in cells) / len(cells)


class Evaluator:
    def __init__(self, table):
        self._lexer = CalcLexer()
        self._parser = CalcParser(table)

    def evaluate(self, text):
        return self._parser.parse(self._lexer.tokenize(text))


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser(None)
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
