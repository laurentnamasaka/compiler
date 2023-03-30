
DIGITS = '0123456789'

#ERRORS
class Error:        
    def __init__(self,error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

    #class ExpectedCharError(Error):
     #   def __init__(self, pos_start, pos_end, details):
      #      super().__init__(pos_start, pos_end, 'Expected Character', details)

#class Error:
 #   def __init__(self, pos_start, pos_end, error_name, details):
  #      self.pos_start = pos_start
   #     self.pos_end = pos_end
    #    self.error_name = error_name
     #   self.details = details

    #def as_string(self):
     #   result  = f'{self.error_name}: {self.details}'
      #  result += f' File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
       # return result

#class IllegalCharError(Error):
 #   def __init__(self, pos_start, pos_end, details):
  #      super().__init__(pos_start, pos_end, 'Illegal Character', details)

#class ExpectedCharError(Error):
 #   def __init__(self, pos_start, pos_end, details):
  #      super().__init__(pos_start, pos_end, 'Expected Character', details)

# Token types

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

#CREATING THE TOKENS
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#CREATING THE LEXER

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

#DEFINING THE TOKENS
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    #RUN THE LEXER
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error