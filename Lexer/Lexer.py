from sly import Lexer

class DiamantLexer(Lexer):
    tokens = {PRINTF,IMPORT,TK,PRINT,NAME, NUMBER, STRING,TRUE,FALSE, IF, THEN, ELSE, FOR, FUN, TO,RET, ARROW, EQEQ }
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','.','[',']','{','}',":"}
    RET = r'ret'
    # Define tokens
    PRINTF=r'printf'
    PRINT = r'print'
    IF = r'if'
    IMPORT = r'import'
    THEN = r'then'
    TK=r'tk'
    ELSE = r'else'
    FOR = r'for'
    FUN = r'fun'
    TO = r'to'
    TRUE=r'True'
    FALSE =r'False'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #STRING = r'\".*?\"'
    #STRING = r'"(?:\\.|[^"\\])*"'
    STRING = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')

