from sly import Lexer

class DiamantLexer(Lexer):
    lineno=0
    tokens = {PRINTF, IMPORT, TK, PRINT, NAME, NUMBER, STRING, TRUE, FALSE, IF, THEN, ELSE, FOR, FUN, TO, RET, ARROW, EQEQ}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';', '.', '[', ']', '{', '}', ":" }
    RET = r'ret|terug'  # English: return, Afrikaans: terug
    # Define tokens
    PRINTF = r'printf|drukf'  # English: printf, Afrikaans: drukf
    PRINT = r'print|druk'  # English: print, Afrikaans: druk
    IF = r'if|as'  # English: if, Afrikaans: as
    IMPORT = r'import|invoer'  # English: import, Afrikaans: invoer
    THEN = r'then|dan'  # English: then, Afrikaans: dan
    TK = r'tk|tk'  # English: tk, Afrikaans: tk (no translation)
    ELSE = r'else|anders'  # English: else, Afrikaans: anders
    FOR = r'for|vir'  # English: for, Afrikaans: vir
    FUN = r'func|funk'  # English: function, Afrikaans: funksie
    TO = r'to|na'  # English: to, Afrikaans: na
    TRUE = r'True|Waar'  # English: True, Afrikaans: Waar
    FALSE = r'False|Onwaar'  # English: False, Afrikaans: Onwaar
    ARROW = r'->'  # English: arrow, Afrikaans: na
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'  # English: variable name, Afrikaans: naam
    STRING = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''  # Matches strings, no direct translation
    EQEQ = r'==|gelyk_aan'  # English: equality, Afrikaans: is

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    @_(r'/\*.*?\*/')
    def block_comment(self, t):
        pass  # Ignore block comments


    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1  # Skip the illegal character and continue lexing
