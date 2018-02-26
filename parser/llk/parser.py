__all__ = ['parse']

from lexer import JSONLexer, Token


class Parser(object):
    def __init__(self, lex, k):
        self.lex = lex
        self.index = 0
        self.k = k
        self.lookahead = [i for i in range(k)]
        for i in range(k):
            self.consume()

    def consume(self):
        self.lookahead[self.index] = self.lex.next_token()
        self.index = (self.index + 1) % self.k

    def token_of_next(self, n):
        i = (self.index + n - 1) % self.k
        return self.lookahead[i]

    def token_type_of_next(self, n):
        token = self.token_of_next(n)
        return token.type

    def match(self, token_type):
        if self.token_type_of_next(1) == token_type:
            self.consume()
        else:
            raise Exception(">> Expected: {}, Found: {}".format(Token(None, token_type), self.token_of_next(1)))


class JSONParser(Parser):
    def __init__(self, tokens, k=2):
        super(JSONParser, self).__init__(tokens, k)

    def array(self):
        self.match(Token.bracketLeft)
        _elements = self.elements()
        self.match(Token.bracketRight)
        return _elements

    def elements(self):
        es = [self.value()]
        while Token.comma == self.token_type_of_next(1):
            self.match(Token.comma)
            v = self.value()
            es.append(v)
        return es

    def value(self):
        n1 = self.token_of_next(1)
        if n1.type == Token.string:
            self.match(Token.string)
            return n1.value
        elif n1.type == Token.number:
            self.match(Token.number)
            return n1.value
        elif n1.type == Token.null:
            self.match(Token.null)
            return None
        elif n1.type == Token.boolean:
            self.match(Token.boolean)
            if n1.value == 'true':
                return True
            else:
                return False
        elif n1.type == Token.bracketLeft:
            return self.array()
        elif n1.type == Token.braceLeft:
            return self.object()
        else:
            raise Exception('>> Expected: value, Found: {}'.format(self.token_of_next(1)))

    def object(self):
        self.match(Token.braceLeft)
        ps = self.pairs()
        self.match(Token.braceRight)
        return dict(ps)

    def pairs(self):
        ps = [self.pair()]
        while Token.comma == self.token_type_of_next(1):
            self.match(Token.comma)
            ps.append(self.pair())
        return ps

    def pair(self):
        n1 = self.token_of_next(1)
        n2 = self.token_of_next(2)
        if n1.type == Token.string and n2.type == Token.colon:
            self.match(Token.string)
            self.match(Token.colon)
        k = n1.value
        v = self.value()
        return (k, v)


def parse(json_string):
    tokens = JSONLexer(json_string)
    parser = JSONParser(tokens)
    r = parser.object()
    return r
