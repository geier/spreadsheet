from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { CELL, NUMBER, }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' }

    # Tokens
    CELL = r'[A-Z]{1,2}[0-9]+'

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
        cellname = p[0]
        return self._table[cellname].value


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
