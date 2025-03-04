from sly import Parser
from Lexer.Lexer import DiamantLexer

class DiamantParser(Parser):
    tokens = DiamantLexer.tokens


    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }
        self.modules = {}

    
    
    @_('')
    def statement(self, p):
        pass


    @_('FOR "(" var_assign ")" TO expr THEN "{" statement_list "}"')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement_list)



    @_('IF condition THEN statement_list ELSE statement_list')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement_list0, p.statement_list1))

    @_('IF "(" condition ")" "{" statement_list "}"')
    def statement(self, p):
        return ('if_stmt_if', p.condition, p.statement_list)



    @_('FUN NAME "(" ")" ARROW statement_list')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement_list)

    @_('FUN NAME "(" args ")" ARROW statement_list')
    def statement(self, p):

        return ('fun_def_args', p.NAME,p.args, p.statement_list)

    @_('NAME')
    def args(self,p):

        return [p.NAME]

    @_('args "," NAME')
    def args(self,p):
        return p.args + [p.NAME]
    @_('NAME "(" ")"')
    def expr(self, p):
        return ('fun_call', p.NAME)


    @_('NAME "(" print_args ")"')
    def expr(self, p):
        return ('fun_call_args', p.NAME,p.print_args)

    @_('TRUE')
    def condition(self, p):
        return ('condition_true', True)

    @_('FALSE')
    def condition(self, p):
        return ('condition_false', False)


    @_('expr')
    def condition(self, p):
        return (p.expr)

    @_('condition EQEQ condition')
    def condition(self, p):
        return ('condition_eqeq', p.condition0, p.condition1)



    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_('NAME "=" condition')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.condition)

    @_('expr')
    def statement(self, p):
        return (p.expr)


    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)



    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('STRING')
    def expr(self,p):
        return ('str',p.STRING)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('PRINT "(" print_args ")"')
    def statement(self, p):
        return ('print_stmt', p.print_args)

    @_('PRINTF "(" print_args ")"')
    def statement(self, p):
        return ('print_stmt_f', p.print_args)

    @_('expr')
    def print_args(self, p):
        return [p.expr]



    @_('print_args "," expr')
    def print_args(self, p):
        return p.print_args + [p.expr]

    @_('statement_list "," statement')
    def statement_list(self, p):
        return p.statement_list + [p.statement]

    @_('statement')
    def statement_list(self, p):
        return [p.statement]

    @_('TK NAME')
    def statement(self, p):
        return ("TK",p.NAME)
    # @_('IMPORT NAME')
    # def statement(self,p):
    #     return ('import',p.NAME)
    @_("NAME '.' NAME '(' print_args ')'" )
    def expr(self, p):
        return ('builtin-func', p.NAME0,p.NAME1,p.print_args)

    @_("list")
    def expr(self, p):
        return p.list

    @_('"[" elements "]"')
    def list(self, p):
        return ('lst',p.elements)


    @_('expr')
    def elements(self, p):
        return [p.expr]

    @_('elements "," expr')
    def elements(self, p):
        p.elements.append(p.expr)
        return p.elements

    @_('list')
    def print_args(self,p):
        return [p.list]

    @_('dict')
    def print_args(self, p):
        return  [p.dict]

    @_('NAME "=" list')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.list)

    @_('NAME "=" dict')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.dict)
    @_("NAME list")
    def expr(self, p):
        return ('var', p.NAME,p.list)

    @_('NAME ":" expr')
    def key_value_pair(self, p):
        return (p.NAME, p.expr)

    @_('"{" key_value_pairs "}"')
    def dict(self, p):
        return ('dict',dict(p.key_value_pairs))

    @_('key_value_pair')
    def key_value_pairs(self, p):
        return [p.key_value_pair]

    @_('key_value_pairs "," key_value_pair')
    def key_value_pairs(self, p):
        return p.key_value_pairs + [p.key_value_pair]
    #maybe standalone list and dicy
    @_("NAME '+' '=' expr")
    def statement(self, p):
        return ('var_peq', p.NAME,p.expr)

    @_("NAME '-' '=' expr")
    def statement(self, p):
        return ('var_seq', p.NAME, p.expr)

    @_("NAME '/' '=' expr")
    def statement(self, p):
        return ('var_deq', p.NAME, p.expr)

    @_("NAME '*' '=' expr")
    def statement(self, p):
        return ('var_meq', p.NAME, p.expr)

    @_('NAME  "(" NUMBER ")" "=" STRING')
    def statement(self,p):
        return ('str_chg', p.NAME, p.NUMBER,p.STRING)

    @_('NAME "[" NUMBER "]" "=" expr')
    def statement(self, p):
        return ('list_chg', p.NAME, p.NUMBER,p.expr)

    @_('NAME "{" NAME "}" "=" expr')
    def statement(self, p):
        return ('dict_chg', p.NAME0, p.NAME1, p.expr)


    @_('RET expr')
    def statement(selfself,p):
        return ("RET",p.expr)

    @_('NAME "+" "+"')
    def statement(self,p):
        return ("INC",p.NAME)
