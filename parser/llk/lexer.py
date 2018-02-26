__all__ = ['Token', 'JSONLexer']


class Token(object):
    EOF = 0
    colon = 1
    comma = 2
    braceLeft = 3
    braceRight = 4
    bracketLeft = 5
    bracketRight = 6
    number = 7
    string = 8
    boolean = 9
    null = 10

    def __init__(self, tk_text, tk_type):
        self.value = tk_text
        self.type = tk_type

    def __repr__(self):
        names = (
            '<EOF>',
            'colon',
            'comma',
            'braceLeft',
            'braceRight',
            'bracketLeft',
            'bracketRight',
            'number',
            'string',
            'boolean',
            'null',
        )
        name = names[self.type]
        return '<({}), {}> \n'.format(self.value, name)


class Lexer(object):
    EOF = -1

    def __init__(self, code):
        self.input = code
        self.index = 0
        self.length = len(code)
        self.char = code[self.index]

    def consume(self):
        self.index += 1
        self.char = self.input[self.index] if self.index < self.length else Lexer.EOF


class JSONLexer(Lexer):
    spaces = ' \n\t\r'
    digits = '1234567890'
    letters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

    def next_token(self):
        '''
        每次读取一个字符 self.consume()
        可能产生一个 token, bracketLeft
        或者 不产生 token, WS
        或者 读取下一个字符来决定 是否产生 token, text
        '''

        while self.char != Lexer.EOF:
            if self.char in self.spaces:
                self.consume_spaces()
            elif self.char == '\"':
                return self.make_token_string()
            elif self.char == '-':
                self.consume()
                return self.make_token_number(-1)
            elif self.char in self.digits:
                return self.make_token_number()
            elif self.char is 'n':
                return self.make_token_null()
            elif self.char in 'tf':
                return self.make_token_boolean()
            elif self.char == '[':
                self.consume()
                return Token('[', Token.bracketLeft)
            elif self.char == ']':
                self.consume()
                return Token(']', Token.bracketRight)
            elif self.char == ',':
                self.consume()
                return Token(',', Token.comma)
            elif self.char == ':':
                self.consume()
                return Token(':', Token.colon)
            elif self.char == '{':
                self.consume()
                return Token('{', Token.braceLeft)
            elif self.char == '}':
                self.consume()
                return Token('}', Token.braceRight)
        return Token(None, Token.EOF)

    def consume_spaces(self):
        while self.char in self.spaces:
            self.consume()
            if self.char == Lexer.EOF:
                break

    def make_token_string(self):
        self.consume()
        s = ''
        while self.char != '\"':
            if self.char == '\\':
                self.consume()
                if self.char in '\"\'\\\/':
                    s += self.char
                elif self.char in 'ntr':
                    s += '\n\t\r'['ntr'.index(self.char)]
            else:
                s += self.char
            self.consume()
        self.consume()
        return Token(s, Token.string)

    def make_token_number(self, sign=1):
        s = ''
        decimal = False
        while self.char in self.digits or self.char == '.':
            if self.char == '.':
                if decimal:
                    raise Exception("invalid decimal")
                else:
                    decimal = True
                    s += self.char
                    self.consume()
            else:
                s += self.char
                self.consume()

        if '.' in s:
            s = sign * float(s)
        else:
            s = sign * int(s)
        return Token(s, Token.number)

    def make_token_null(self):
        s = ''
        while True:
            s += self.char
            self.consume()
            if len(s) == 4:
                break
        if s != 'null':
            raise Exception("invalid null")
        return Token(s, Token.null)

    def make_token_boolean(self):
        s = ''
        if self.char == 't':
            while len(s) < 4:
                s += self.char
                self.consume()
            if s != 'true':
                raise Exception("invalid true")
        else:
            while len(s) < 5:
                s += self.char
                self.consume()
            if s != 'false':
                raise Exception("invalid false")
        return Token(s, Token.boolean)
