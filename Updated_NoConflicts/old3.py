import io
#import custom_syntax
from sly import Lexer, Parser
import DIA_GUI
import time
import inspect
import importlib
from copy import deepcopy
import sys
import copy
#import win32com.client
import os
import sys
#import custom_syntax
#this one is to edit and allow for pywin32
import ctypes
from ctypes import CDLL, CFUNCTYPE
from multiprocessing import Process
import time


from ctypes import wintypes

from soupsieve.util import lower


class InvalidTypeError(Exception):
    def _init_(self, message):
        super()._init_(message)


class BasicLexer(Lexer):
    tokens = {C,ASM,EVERY,RARROW,GUI,HOTKEY,EXTERN,LOAD,YIELD,INFIX,WATCH,MEM,ONCE,LAZY,DEFER,TIME,BOOL,DICT,FLT,WITH,ENUM, IN,PRINTF,IMPORT,TK,PRINT,NAME, NUMBER,FLOAT, STRING,TRUE,FALSE, IF, THEN, ELSE, FOR, FUN, TO,RET, PUBLIC,ARROW,CLASS,LARROW,EQEQ,GEQEQ,LEQEQ,IDENTIFIER,STRUCT,WHILE,EXPO,FLOOR,OR,AND,NOT,ELIF,INT,STR,STRING3,NULL_COL,BREAK,MATCH,EXCEL,LIVE}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','.','[',']','{','}',"$" ,":","?",'>','<',"%", "@"}
    lineno=0

    ASM = r"ASM"
    C = r"C"
    RET = r'ret'
    MEM = r'MEM'
    EVERY = r'EVERY'
    LOAD = r'LOAD'
    HOTKEY = r'HOTKEY'
    EXTERN = r'EXTERN'
    YIELD = r'YIELD'
    OR = r'or|Of'
    AND = r'and|En|&&'
    NOT = r'not|Nie'
    INT = r"INT"
    IN = r'in'
    TIME = r'TIME'
    INFIX = r'INFIX'
    WATCH = r'WATCH'
    DEFER = r'DEFER'
    WITH = r'with'
    STR = r'STRING'
    FLT = r'FLOAT'
    CLASS = r'Class'
    BOOL = r'BOOL'
    GUI = r'GUI'
    DICT = r'DICT'
    LAZY = r'LAZY'
    # Define tokens
    STRING3 = r'"""[^"]*"""'
    STRING = r'"(?:\\.|[^"\\])*"'



    #STRING = r'"(?:\\.|[^"\\])"|\'(?:\\.|[^\'\\])\''
    PRINTF=r'printf'
    PRINT = r'print'
    IF = r'if|As'
    BREAK=r'break|breek'
    IMPORT = r'import'
    THEN = r'then|Dan'
    TK=r'tk'
    ELSE = r'Anders|else'
    ELIF = r'elif'
    FOR = r'for'
    FUN = r'fun'
    TO = r'To'
    TRUE=r'True'
    ENUM = r'ENUM'
    FALSE =r'False'
    MATCH =r'match'
    ARROW = r'->'
    RARROW = r'<-'
    EXCEL = r'Excel'
    LIVE =  r'live'
    LARROW=r'=>'
    PUBLIC = r'public'
    STRUCT = r"struct|strukt"
    WHILE = r'while|terwyl'
    ONCE =r'ONCE'
    IDENTIFIER = r"int|str|hlt|tkr|list|lys|any|enige"
    NULL_COL = r'\?\?'


    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #STRING = r'\".*?\"'
    #STRING = r'"(?:\\.|[^"\\])*"'


    EQEQ = r'=='
    GEQEQ=r'>='
    LEQEQ=r'<='
    EXPO = r'\*\*'
    FLOOR = r'//'


    @_(r'\d+\.\d+')
    def FLOAT(self,t):
    	t.value = float(t.value)
    	return t
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'>>>.*')
    def COMMENT_SINGLE(self, t):
        pass  # Ignore it

    @_(r"\/\*[\s\S]*?\*\/")
    def COMMENT(self,t):
    	pass

    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')


class BasicParser(Parser):
    tokens = BasicLexer.tokens
    t1234=[]
    precedence = (
        ('left', '.', '?', ':'),  # ternary + dot
        ('right', 'NOT'),  # unary NOT
        ('left', 'EXPO'),  # exponentiation
        ('left', 'AND', 'OR', 'INT'),  # logical ops
        ('left', '+', '-'),  # add, sub
        ('left', '>', '<', 'GEQEQ', 'LEQEQ', 'EQEQ', 'NULL_COL'),
        ('left', '*', '/', 'FLOOR', '%','[',']'),  # mul/div/mod
        ('left', 'ELSE','@',"STR_expr"),

        ('right', 'CAST', 'UNPACK'),  # cast (LOWER)

        ('right', 'UMINUS')  # other unary
    )

    def _init_(self):
        self.env = {}
        self.modules = {}
        self.t1234=[]

    @_("")
    def statement(self,p):
    	return


    @_("Body")
    def statement(self, p):
        return p.Body

    @_("'{' procs '}'")
    def Body(self, p):
        return p.procs
    #for classes
    @_("PUBLIC NAME '{' procs '}'")
    def Body(self, p):
        return [('public_name', p.NAME, p.procs)]

    @_("procs ',' proc")
    def procs(self, p):
        return p.procs + [p.proc]

    @_('proc')
    def procs(self, p):
        return [p.proc]

    @_('statement')
    def proc(self, p):
        return p.statement

    @_("'$' Body")
    def Class_Body(self,p):

    	return p.Body
    @_("Body Body")
    def Class_Body(self,p):
    	#print(p.Body0)
    	return p.Body0 + p.Body1

    @_('Class_Body Body')
    def Class_Body(self,p):
    	#print(p.Class_Body )
    	return p.Class_Body + p.Body


    @_('CLASS NAME "{" Class_Body "}"')
    def statement(self,p):
    	#print(p.Class_Body)
    	return ('Normal_Class', p.NAME, p.Class_Body)
    @_('ELIF expr statement')
    def elif_branch(self,p):
    	return ("elif_expr",p.expr,p.statement)

    @_("elif_branch")
    def elif_branches(self,p):
    	return [p.elif_branch]

    @_('elif_branches elif_branch')
    def elif_branches(self,p):
    	return p.elif_branches + [p.elif_branch]

    #########GUI
    @_('GUI ARROW NAME "(" STRING ")"')
    def statement(self,p):
        return ("Setup-GUI", p.NAME, p.STRING)

    @_('GUI RARROW NAME "(" STRING ")"')
    def statement(self, p):
        return ("Close-GUI", p.NAME,p.STRING)

    @_('GUI')
    def statement(self, p):

        return ("GUI_Start","")

    @_("RET expr")
    def statement(self,p):
        return ("RET", p.expr)


    @_("ASM '{' STRING3 '}'")
    def statement(self,p):

        return ("ASM",p.STRING3)

    @_(" C '{' STRING3 '}'")
    def statement(self, p):

        return ("C", p.STRING3)

    @_(" C ARROW '{' STRING3 '}'")
    def statement(self, p):

        return ("C_delay", p.STRING3)

    @_("expr EQEQ expr")
    def expr(self, p):
    	#print(p.expr0)
    	return ("expr_EQEQ", p.expr0, p.expr1)

    @_("expr GEQEQ expr")
    def expr(self, p):
    	return ("expr_GEQEQ", p.expr0, p.expr1)
    @_("expr LEQEQ expr")
    def expr(self, p):
    	return ("expr_LEQEQ", p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):

    	return ('bigger_than', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
    	return ('less_than', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):

    	return ('and', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
    	return ('or', p.expr0, p.expr1)

    @_('NOT expr %prec NOT')
    def expr(self, p):
    	return ('not', p.expr)

    @_('expr ARROW statement')
    def case(self, p):
    	return ("case", p.expr,p.statement)
    @_("EXCEL LIVE")
    def statement(self,p):

    	return ("Excel_Live",0)

    @_('case')
    def cases(self, p):
    	return [p.case]
    @_('cases "," case')
    def cases(self, p):
    	return p.cases + [p.case]
    @_('"{" cases "}"')
    def CASE(self,p):
    	return p.cases

    @_('MATCH expr CASE')
    def statement(self, p):
    	#print(p.CASE)
    	return ('match',p.expr,p.CASE)

    @_('NAME')
    def LNAME(self,p):
        return [p.NAME]

    @_('LNAME "," NAME')
    def LNAME(self, p):
        return p.LNAME + [p.NAME]

    @_("'{' LNAME '}'")
    def NAMES(self,p):
        return p.LNAME

    @_('ENUM NAME NAMES')
    def statement(self, p):
        print(p.NAMES)
        return ('enum',p.NAME,p.NAMES)

    @_('DEFER statement')
    def statement(self, p):

        return ('defer_statement',p.statement)

    @_('STRING ARROW statement')
    def statement(self, p):

        return ('config-statement',p.STRING, p.statement)



    @_('IMPORT STRING')
    def statement(self,p):
    	return ('import_py_module',p.STRING)

    @_('LOAD STRING')
    def expr(self, p):
        return ('LOAD_DLL', p.STRING)

    @_('EXTERN NAME "("  keys ")" ARROW STRING')
    def statement(self, p):
        return ('EXTERN',p.NAME,dict(p.keys),p.STRING)

    @_('IMPORT NAME')
    def statement(self,p):
    	return ('import_dia_module',p.NAME)

    @_("WATCH NAME statement")
    def statement(self,p):
        return ("WATCH_NAME",p.NAME,p.statement)

    @_('tuple ARROW statement')
    def LMD(self,p):
    	return ('LMD',p.tuple,p.statement)

    @_('tuple LARROW  expr')
    def LMD(self,p):
    	return ('LMD_expr',p.tuple,p.expr)

    @_("NAME '=' expr")
    def element(self,p):
        return [(("var",p.NAME),p.expr)]

    @_("expr '.' '.' expr")
    def expr(self, p):
        #struct
        return ("struct_fetch" ,p.expr0,p.expr1)
        return



    @_('NAME "=" LMD')
    def statement(self,p):
    	return ('var_assign_lmd',p.NAME,p.LMD)
    # Statement rules
    @_('FOR NAME "=" expr  TO expr statement')
    def statement(self, p):
        return ('for_loop',('for_loop_setup',('var_assign', p.NAME, p.expr0),p.expr1),p.statement)
        return ('for_loop', p.expr0, p.expr1, p.statement)


    @_("FOR NAME IN expr statement")
    def statement(self,p):
        return ("FOR_IN_EXPR", p.NAME, p.expr, p.statement)

    @_("FOR NAME ',' NAME IN expr statement")
    def statement(self, p):
        return ("FOR_IN_EXPR", p.NAME0, p.expr, p.statement, p.NAME1)


    #############STruct
    @_("STRUCT NAME statement")
    def statement(self, p):

        return ("DEFINE_STRUCT", p.NAME, p.statement)



    ####################################
    # @_("IF expr ARROW statement")
    # def statement(self,p):
    #     return 0

    # @_('ELSE statement')
    # def a(self, p):
    #     return (p.statement0, p.statement1)
    #
    # @_("elif_branches a")
    # def b(self,p):
    #     return ([p[0]],p.elif_branches)



    # @_('ARROW statement')
    # def c(self,p):
    #     return p.statement
    #
    # @_('statement  elif_branches')
    # def d(self,p):
    #     return p.statement
    #
    # @_('c a')
    # def d(self, p):
    #     return [p.c],p.a
    #
    # @_('c b')
    # def d(self, p):
    #     return p.statement,p.b


    # @_('statement')
    # def l(self,p):
    #     return [p.statement]


    # @_("IF expr d")
    # def statement(self, p):
    #     print(p.c)
    #     return
    #     if len(p.s)==1:
    #         print(p.s)
    #         return ('if_stmt', p.expr, p.s[0], p.statement)
    #
    #     return ('if_stmt_elif', p.expr, p.s[0], p.s[1], p.statement)
        #return ('if_stmt_elif', p.expr, p.statement0, p.elif_branches, p.statement1)
    @_('IF expr statement')
    def statement(self, p):
       return ('if_statement', p.expr, p.statement)



    @_('IF expr THEN statement elif_branches ELSE statement')
    def statement(self, p):

        return ('if_stmt_elif', p.expr, p.statement0, p.elif_branches, p.statement1)

    # @_('IF expr ARROW statement elif_branches')
    # def statement(self, p):
    #
    #     return ('if_stmt_elif', p.expr, p.statement0, p.elif_branches, p.statement1)

    @_('IF expr THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.expr, p.statement0, p.statement1)



    @_('FUN NAME "(" ")" statement')
    def statement(self, p):

        return ('fun_def', p.NAME, p.statement)

    @_(' HOTKEY STRING FUN NAME "(" ")" statement')
    def statement(self, p):

        return ('fun_def_hotkey', p.NAME, p.statement,p.STRING)

    @_('WHILE expr statement')
    def statement(self,p):
    	return ("while_loop_expr",p.expr,p.statement)


    @_('FUN NAME tuple statement')
    def statement(self, p):
        return ('fun_def_args', p.NAME,p.tuple, p.statement)

    #@_("tuple ARROW statement")
    #def expr(self,p):
    #	print(777);


    @_("WITH expr statement")
    def statement(self, p):
        return ("WITH_expr_env", p.expr, p.statement)
    @_('INT NAME')
    def statement(self, p):

        return ('var_assign_type_int', p.NAME)
    @_('STR NAME')
    def statement(self, p):

        return ('var_assign_type_string', p.NAME)


    @_('FLT NAME')
    def statement(self, p):

        return ('var_assign_type_float', p.NAME)

    @_('BOOL NAME')
    def statement(self, p):

        return ('var_assign_type_bool', p.NAME)

    @_('DICT NAME')
    def statement(self, p):

        return ('var_assign_type_dict', p.NAME)





    @_('INT NAME "=" expr')
    def statement(self, p):

        return ('var_assign_type_int_expr', p.NAME,p.expr)

    @_('FLT NAME "=" expr')
    def statement(self, p):

        return ('var_assign_type_float_expr', p.NAME,p.expr)

    @_('BOOL NAME "=" expr')
    def statement(self, p):

        return ('var_assign_type_bool_expr', p.NAME,p.expr)

    @_('DICT NAME "=" expr')
    def statement(self, p):

        return ('var_assign_type_dict_expr', p.NAME,p.expr)


    @_('STR NAME "=" expr')
    def statement(self, p):

        return ('var_assign_type_str_expr', p.NAME,p.expr)

    @_('NAME "=" expr')
    def statement(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('MEM NAME "=" expr')
    def statement(self, p):
        return ('MEM_var', p.NAME, p.expr)
    @_('LAZY NAME "=" expr')
    def statement(self, p):
        return ('var_assign_lazy', p.NAME, p.expr)
    @_('NAME "+" "=" expr')
    def statement(self, p):
        return ("var_peq",p.NAME,p.expr)

    @_('NAME "-" "=" expr')
    def statement(self, p):
       return ("var_seq",p.NAME,p.expr)
    @_('NAME "/" "=" expr')
    def statement(self, p):
       return ("var_deq",p.NAME,p.expr)
    @_('NAME "*" "=" expr')
    def statement(self, p):
       return ("var_meq",p.NAME,p.expr)

    @_('NAME "?" "+" "=" expr')
    def statement(self, p):

       return ("var_check_peq",p.NAME,p.expr)

    @_('NAME "?" "-" "=" expr')
    def statement(self, p):

       return ("var_check_seq",p.NAME,p.expr)

    @_('NAME "?" "/" "=" expr')
    def statement(self, p):

       return ("var_check_deq",p.NAME,p.expr)


    @_('NAME "?" "*" "=" expr')
    def statement(self, p):

       return ("var_check_meq",p.NAME,p.expr)
    # Print statement
    @_('PRINT tuple')
    def statement(self, p):
        return ('print_stmt', p.tuple)



    # Printf statement
    @_('PRINTF "(" expr ")"')
    def statement(self, p):
        return ('print_stmt_f', p.expr)

    @_('"$" STRING')
    def expr(self,p):

        return ('f_str', p.STRING)
    #expr section.
    # Expression rules
    # @_("NAME '(' expr ')' ")
    # def expr(self,p):
    # 	#print(p[0],p[2])
    # 	if(p[0]=="con_list"):
    #
    # 		return ('con_list',p[2])
    # 	return 0
    @_("expr '[' expr ']'")
    def expr(self, p):

        return ("get_index", p.expr0, list(p.expr1))


    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_("NAME '(' ')'")
    def expr(self,p):
        return ('fun_call',p.NAME)
    @_("NAME tuple")
    def expr(self,p):
        return ('fun_call_args',p.NAME,p.tuple)

    @_("NAME '(' ')'")
    def statement(self,p):
        return ('fun_call',p.NAME)
    @_("'$' NAME '(' ')'")
    def expr(self,p):
    	return ("builtin_funcs",p.NAME)
    @_("'$' NAME tuple")
    def expr(self,p):
    	return ("builtin_funcs",p.NAME,p.tuple)
    @_("'$' NAME '(' ')'")
    def statement(self,p):
    	return ("builtin_funcs",p.NAME)
    @_("'$' NAME tuple")
    def statement(self,p):
    	return ("builtin_funcs",p.NAME,p.tuple)
    @_("NAME tuple")
    def statement(self,p):
        return ('fun_call_args',p.NAME,p.tuple)

   # @_("NAME '>' '(' ')'")
  #  def expr(self,p):
    #    return ('fun_call',p.NAME)
    #@_("NAME '>' '(' ')'")
    #def statement(self,p):
     #   return ('fun_call',p.NAME)


    @_("expr '.' NAME")
    def expr(self,p):
    	return ("Chain_Expr",p.expr,p.NAME)
    #check var chnages and mem etc
    @_("ARROW expr")
    def statement(self, p):
        return ("program", None,p.expr)

    @_("expr '.' NAME tuple")
    def expr(self,p):
    	return ("Chain_Expr_tuple",p.expr,p.NAME,p.tuple)

    @_("expr '.' NAME '(' ')'")
    def expr(self,p):
    	return ("Chain_Expr_call",p.expr,p.NAME)


    @_('"-" expr "=" expr')
    def statement(self,p):

    	return ("var_assign_expr_expr",p.expr0,p.expr1)

    @_("'[' expr '.' '.'  expr '.' '.' expr ']'")
    def expr(self, p):

            return ("Create_range_inc", p.expr0, p.expr1, p.expr2)
    @_("'[' expr '.' '.' expr ']'")
    def expr(self,p):
        return ("Create_range", p.expr0, p.expr1)


    @_("INFIX STRING tuple LARROW statement")
    def statement(self, p):
        return ("INFIX", p.STRING, p.tuple, p.statement)

    @_("expr STRING expr %prec STR_expr")
    def expr(self,p):
        return ("USE_Custom", p.expr0, p.STRING, p.expr1)


    @_("expr '[' expr '.' '.' expr ']'")
    def expr(self,p):
        return ("Get_range_expr", p.expr0,p.expr1, p.expr2)

    @_("expr '[' expr '.' '.' expr '.' '.' expr ']'")
    def expr(self,p):
        return ("Get_range_expr_inc", p.expr0,p.expr1, p.expr2,p.expr3)

    @_("expr '[' '.' '.' expr ']'")
    def expr(self, p):
        return ("reverse_expr", p.expr0, p.expr1)



    @_("expr '[' expr '.' '.' ']'")
    def expr(self, p):
        return ("last_elements_expr", p.expr0, p.expr1)


    @_("'[' expr FOR NAME IN expr  ']'")
    def expr(self, p):
        return ("list_comp_basic", p.expr0, p.NAME,p.expr1)

    @_("'[' expr FOR NAME IN expr IF expr ']'")
    def expr(self, p):
        return ("list_comp_if", p.expr0, p.NAME,p.expr1,p.expr2)

    @_("ONCE statement")
    def statement(self,p):
        return ("Once_statement", p.statement)
    @_("list")
    def expr(self,p):
    	return p[0]
    @_("tuple")
    def expr(self,p):
    	return p[0]
    @_("set")
    def expr(self,p):
    	return p[0]

    @_("dict")
    def expr(self,p):
    	return p[0]

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    @_('FLOAT')
    def expr(self, p):
        #print(777)
        return ('float', p.FLOAT)
    @_("STRING")
    def expr(self,p):
     	return ("str",p.STRING[1:-1])
    @_("STRING3")
    def expr(self,p):
     	return ("str",p.STRING3[3:-3])

    @_('TRUE')
    def expr(self, p):

        return ('condition_true', True)

    @_('FALSE')
    def expr(self, p):
        return ('condition_false', False)

    @_('expr "?" "(" expr ":" expr ")"  ')
    def expr(self, p):
        return ("Ternary", p.expr0, p.expr1, p.expr2)


    @_('expr "+" expr')
    def expr(self, p):



        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)
    @_('expr EXPO expr')
    def expr(self, p):
    	return ('expo', p.expr0, p.expr1)
    @_('expr FLOOR expr')
    def expr(self, p):
    	return ('floor', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('expr "%" expr')
    def expr(self, p):
        return ('mod', p.expr0, p.expr1)

    @_("NAME '@' '*'")
    @_("NAME '@' expr")
    def expr(self, p):
        if p[2]=="*":
            return ("Full_History",p.NAME)
        return ("VAR_History", p.NAME,p.expr)
    @_('expr NULL_COL expr')
    def expr(self, p):
        return ('NULL_COL', p.expr0, p.expr1)
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('uminus', p.expr)


    @_('"*" expr %prec UNPACK')
    def expr(self, p):
        return ('unpack', p.expr)

    # List rule

    @_('"[" "]"')
    @_('"[" elements "]"')
    def list(self, p):
       #print(p[1])
        if len(p)<3:
            return ("list",[])
        return ('list', p.elements)


    @_('"(" elements ")"')
    def tuple(self,p):
    	return ('tuple',p[1])


    @_('LNAME ARROW tuple')
    def statement(self,p):
        return ('NAMES_TUPLE', p.LNAME, p.tuple)

    @_('"{" elements "}"')
    def set(self,p):
    	return ('set',p[1])


    @_("NAME list '=' expr")
    def statement(self, p):
        # checks if its a num print(p[1]) to see why

        return ("set_index",p.NAME, p.list, p.expr)
    @_("expr '?' list")
    def expr(self,p):
    	#checks if its a num print(p[1]) to see why
    	#print(p.expr,999)
    	return ("get_index_expr_null", p.expr,p.list)


    #ignore for now
    @_("expr '$' list")
    def expr(self,p):
    	return ("get_index_null", p.expr,p.list)


    @_("TIME NAME statement")
    def statement(self,p):
        return ("TIME", p.NAME,p.statement)

    @_("'(' INT ')'")
    def CAST(self,p):
        return int

    @_("'(' STR ')'")
    def CAST(self, p):
        return str

    @_("'(' FLT ')'")
    def CAST(self, p):
        return float

    @_("'(' BOOL ')'")
    def CAST(self, p):
        return bool

    @_("'(' DICT ')'")
    def CAST(self, p):
        return dict
    @_("CAST expr %prec CAST")
    def expr(self,p):


        return ('Type_Cast_old', p.CAST, p.expr)

    #subsection of list is the elements section
    @_("elements ',' element")
    def elements(self,p):
    	#print(p[0],11)
    	#print(p[0],777)
    	return p[0]+p[2]


    @_("element")
    def elements(self,p):
    	return p[0]
    #subsection element of elepments

    @_("expr")
    def element(self,p):
    	return [p[0]]
    #END OF LIST RULE
    #start of dict sect#
    @_(' "{" keys "}" ')
    def dict(self, p):
       #print(p[1])
        #print(p[1],100)
        return ('dict', dict(p.keys))




    #subsection of list is the elements section
    @_("keys ',' key")
    def keys(self,p):
    	#print(p[0],11)
    	#print(p[0],777)
    #	print(p.keys)
    	return p.keys + [p.key]

    @_("key")
    def keys(self,p):
    	return [p[0]]
    #subsection element of elepments

    @_("expr ':' expr")
    def key(self,p):
    	return (p.expr0,p.expr1)




    	#END
    def check_brak(self, str):
    	stack = []
    	brackets = {')': '(', ']': '[', '}': '{'}
    	bracks = {'(': ')', '[': ']', '{': '}'}
    	num=[]
    	for char in str:
    	       if char in brackets.values():
    	       	stack.append(char)
    	       elif char in brackets.keys():
    	           if stack and stack[-1] == brackets[char]:
    	           	stack.pop()
    	           else:
    	           	num.append(char)
    	if(len(num)!=0): return (False,num)
    	if len(stack)!= 0: return(False,stack)
    	return (len(stack) == 0,True)

    def error(self, p):
        #print(p,77)
        #print(vars(self))
#        print()
#        print(self.t1234)
        self.t1234 = "".join(self.t1234).split("\n")
        self.t1234 = [ i for i in self.t1234 if i!=""]
        #print(self.t1234)
        ret=(0,0)
        ret = self.check_brak(str("".join(self.t1234)))
        if(ret[0]==False):
        	raise SyntaxError(f"Unmatched {len(ret[1])} parentheses {' '.join(ret[1])} at {''.join(self.t1234)}")








        if p is None:
            raise SyntaxError("Unexpected EOF or mismatched parentheses")
        else:
            raise SyntaxError(f"Syntax error at token {p.value} {BasicLexer.lineno}")

class ReadOnlyDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("Cannot modify read-only dict")
    def __delitem__(self, key):
        raise TypeError("Cannot modify read-only dict")
    def clear(self):
        raise TypeError("Cannot modify read-only dict")
    def pop(self, key, default=None):
        raise TypeError("Cannot modify read-only dict")
    def popitem(self):
        raise TypeError("Cannot modify read-only dict")
    def update(self, *args, **kwargs):
        raise TypeError("Cannot modify read-only dict")


class BasicExecute:
    def update_variable(env, name, val):
    	var = env.get(name)
    	if isinstance(var, tuple):
        	if type(var[0]) == type(val):
            		env[name] = (var[0] + val, type(var[0]).__name__)
            		print(env[name])
            		return
        	else:
            		print(f"Type Error: Cannot add {type(val).__name__} to {type(var[0]).__name__}")
            		exit()

    def __init__(self, tree, env,Func,temp_env,struct_env,builtins,defered=[],IsOnce=[],var_his={},watch={},custom_operators={},GUI_STRUCT={"Main":"","Win":[]}):
        self.env = env
        self.Func =Func
        self.temp_env = temp_env
        self.struct_env = struct_env
        self.builtins = builtins
        self.defaults = {int: 0, float: 0.0, str: "", bool: False, list: [], dict: {}, set: set(), tuple: (), type(None): None}
        self.defered = defered
        self.var_his = var_his
        self.watch = watch
        self.custom_operators = custom_operators
        self.GUI_mode = False
        self.GUI_STRUCT = GUI_STRUCT
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):

            return node

        if node is None:

            return None
        if node[0] == 'program':

            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0]=="C_delay":
            from C import build_and_load_c_block
            import re

            s = self.walkTree(node[1][1:-1]).replace("'", '"')[2:-2].replace("\\s", ";")

            # --- Map C types to ctypes ---
            ctypes_map = {
                'void': None,
                'int': ctypes.c_int,
                'int*': ctypes.POINTER(ctypes.c_int),
                'double': ctypes.c_double,
                'float': ctypes.c_float,
                'char': ctypes.c_char,
            }

            # --- Extract return type, function name, and args ---
            func_pattern = r'\b(void|int\*|int|double|float|char)\s+(\w+)\s*\(([^)]*)\)'
            matches = re.findall(func_pattern, s)
            # matches: [('void', 'hello', ''), ('int', 'add', 'int a, int b')]

            # --- Compile and load C block ---
            lib = build_and_load_c_block(s)

            # --- Build list of callable functions with restype & argtypes ---
            all_funcs = []
            for ret_type, name, args in matches:
                f = getattr(lib, name)

                f.restype = ctypes_map.get(ret_type, ctypes.c_void_p)
                # Parse argument types
                args = args.strip()
                if args == "" or args == "void":
                    f.argtypes = []
                else:
                    argtypes_list = []
                    for arg in args.split(","):
                        ctype_str = arg.strip().split()[0]  # take the type only
                        argtypes_list.append(ctypes_map.get(ctype_str, ctypes.c_void_p))
                    f.argtypes = argtypes_list

                all_funcs.append((name, f))

            # --- Register in Diamant builtins ---
            for name, func in all_funcs:
                self.builtins["_C_" + name] = func

        if  node[0]=="C":
            from C import build_and_load_c_block
            s = self.walkTree(node[1][1:-1]).replace("'", '"')[2:-2].replace("\\s",";")

            lib = build_and_load_c_block(s)
            func = getattr(lib, "main")  # Or any other function
            func.restype = None  # Important: tells ctypes that function returns void
            func()  # Executes the function


        if node[0]=="ASM":
            from ASM import build_and_load_asm
            s=self.walkTree(node[1][1:-1]).replace("'",'"')[2:-2]
            print(s)
            build_and_load_asm(s)

        if node[0]=="Close-GUI":
            for i in self.GUI_STRUCT["Win"]:
                if i["ID"]==self.walkTree(node[2]):
                    i["Win"].destroy()
        if node[0]=="GUI_Start":

            if self.GUI_mode:
                pass
            else:

                self.GUI_mode = True
                for i in self.GUI_STRUCT["Win"]:
                    i["Win"].mainloop()
                #self.GUI_STRUCT["Main"]["Win"].mainloop()

        if node[0]=="Setup-GUI":
            gui = DIA_GUI.DiaGUI()
            window = gui.Window(self.walkTree(node[1]))
            if self.GUI_mode:
                pass
            else:
                #add some id logic
                self.GUI_STRUCT["Win"].append({"Win":window,"Name":self.walkTree(node[1]),"ID":self.walkTree(node[2])})


            return
        if node[0]=="fun_def_hotkey":
            import keyboard
            key = self.walkTree(node[3])

            fun = node[2]

            def run_all():
                for i in fun:
                    self.walkTree(i)

            keyboard.add_hotkey(key[1:-1], run_all)

            return
        if node[0]=="Full_History":
            return self.var_his[self.walkTree(node[1])]

        if node[0]=="LOAD_DLL":
            dll_name = self.walkTree(node[1]).strip('"').split('.')[0]
            # → "a"
            self.env["current_lib"] = {"attr":CDLL(os.path.abspath(self.walkTree(node[1])[1:-1])),"name":dll_name}

            return self.env["current_lib"]
        if node[0]=="EXTERN":
            TYPE_MAP = {
                "int": ctypes.c_int,
                "float": ctypes.c_float,
                "double": ctypes.c_double,
                "char": ctypes.c_char,
                "char*": ctypes.c_char_p,
                "void": None,
                "bool": ctypes.c_bool,
                "short": ctypes.c_short,
                "long": ctypes.c_long,
                "size_t": ctypes.c_size_t,
            }
            func = getattr(self.env["current_lib"]["attr"], self.walkTree(node[1]))


            ret_str=self.walkTree(node[3])
            arg_dict = self.walkTree(("dict",node[2]))

            func.restype = TYPE_MAP.get(ret_str, ctypes.c_int)  # default to int

            # Convert args: {'a': 'int', 'b': 'int'} → [c_int, c_int]
            arg_types = []
            for param_name in arg_dict:
                ctype = TYPE_MAP.get(arg_dict[param_name], ctypes.c_int)
                arg_types.append(ctype)

            func.argtypes = arg_types

            # Return a callable Diamant function
            param_order = list(arg_dict.keys())

            self.builtins[self.env["current_lib"]["name"]+"_"+self.walkTree(node[1])] = lambda *args, **kwargs: func(
                *[
                    kwargs[p] if p in kwargs else args[i]
                    for i, p in enumerate(param_order)
                ]
            )


        if node[0] == "struct_fetch":
            #return self.walkTree(node[1])
            #basically gets the value of d..a d then goes get a names then goes to d with a gets a and return
            #its value at 0 not the type at index 1
            return self.walkTree(node[1])[node[2][1]][0]
            return self.env[self.walkTree(node[1])]

        if node[0]=="DEFINE_STRUCT":
            t = {}

            for i,v in enumerate(node[2]):
                if len(v)>2:
                    print(f"ERROR incorrect signature of struct {node[2][1]}")
                    return
                var_type = node[2][i][0]

                var_name = node[2][i][1]
                #assigns the whole type without unneccesary ifs
                t[var_name] = (None,var_type[16:])
                #if var_type == "var_assign_type_int":
                    # t[var_name]  = (None,'int')
            self.env[node[1]] = t,"struct"
            #print(self.env[node[1]])



        if node[0]=="config-statement":
            string = self.walkTree(node[1])[1:-1]
            stat = node[2]

            if string.lower()=="readonly":

                t = self.env
                self.env = ReadOnlyDict(self.env)

                for i in stat:
                    self.walkTree(i)
                self.env = t
            if string.lower()=="no-vars":

                t = self.env
                self.env = None

                for i in stat:
                    self.walkTree(i)
                self.env = t
            if string.lower()[0:5]=="timer":
                #implement later
                return
            if string.lower()=="step-by-step":

                t=self.env
                self.env={}
                for i in stat:
                    input(i)
                    self.walkTree(i)

                self.env = t
        if node[0]=="USE_Custom":


            t = self.env
            s = {}
            s.update(self.env)


            vars=[]
            expr0 = self.walkTree(node[1])
            expr1 = self.walkTree(node[3])
            if node[2] in self.custom_operators:
                for key in self.custom_operators[node[2]]["args"]:
                    vars.append(key)
                for i,v in enumerate(vars):
                    if i==0:
                        s[v] = expr0
                    else:
                        s[v] = expr1
                self.env = s
                for i in self.custom_operators[node[2]]["body"]:
                    if (i[0] == "RET"):
                        for j in self.defered:
                            self.walkTree(j)



                        return self.walkTree(i)
                    self.walkTree(i)

            self.env = t
            return
        if node[0]=="INFIX":
            d = {i[1]:None for i in node[2][1] if i[0]=='var'}
            self.custom_operators[node[1]] = {"args": d, "len" : len(node[2][1]), "body": node[3] }


        if node[0]=="MEM_var":
            self.env[node[1]] = self.walkTree(node[2]) # add some checks here
            self.var_his[node[1]] = [self.env[node[1]]]

        if node[0]=="WATCH_NAME":

            if node[1] in self.watch:

                self.watch[node[1]].append(node[2][0])


                return
            self.watch[node[1]] = node[2]
        if node[0]=="VAR_History":


            return self.var_his[node[1]][self.walkTree(node[2])]
        if node[0]=="Once_statement":
            for i in node[1]:
                self.walkTree(i)
        if node[0]=="var_assign_lazy":
            self.env[node[1]]=("LAZY",node[2])


        if node[0]=="defer_statement":
            self.defered = node[1]
            defered=[9]
        if node[0]=="TIME":
            a = time.time()
            for i in node[2]:
                self.walkTree(i)
            elapsed = time.time() - a

            #print(f"⏱️ Execution time: {elapsed:.6f} seconds")
            if node[1] in self.env:
                if not isinstance(self.env[node[1]], tuple):

                    self.env[node[1]] = elapsed
                    return
                if self.env[node[1]][1] != 'float':
                    raise ValueError(f"Variable {node[1]} is not of type 'FLOAT'")
            self.env[node[1]]=elapsed
        if node[0]=="Type_Cast_old":

            if node[2][0]=='tuple':
                var = self.walkTree(node[2])
                var = var[0]
            else:
                var = self.walkTree(node[2])


            if node[1] == int:

                return int(var)
            if node[1] == str:
                print(node[2],100)
                return str(var)
            if node[1] == bool:
                return bool(var)
            if node[1] == list:
                return list(var)
            if node[1] == dict:
                return dict(var)
            if node[1] == float:
                return float(var)


        if node[0]=="NAMES_TUPLE":
            # add delayed execution
            tuples = self.walkTree(node[2])
            print(node[2])
            for i,v in enumerate(node[1]):
                self.env[v] = tuples[i]
        if node[0]=="Ternary":
            res = self.walkTree(node[1])
            if res:
                return self.walkTree(node[2])
            return self.walkTree(node[3])
        if node[0]=="WITH_expr_env":
            t = self.env

            self.env = self.walkTree(node[1])
            for i in node[2]:
                self.walkTree(i)

            self.env = t
        if node[0] =="unpack":
            return None
        if node[0]=="list_comp_basic":


            return [self.walkTree(node[1]) for self.env[self.walkTree(node[2])] in self.walkTree(node[3])]
        if node[0]=="list_comp_if":
            return [self.walkTree(node[1]) for self.env[self.walkTree(node[2])] in self.walkTree(node[3]) if self.walkTree(node[4])]

        if node[0]=="last_elements_expr":
            return list(self.walkTree(node[1])[self.walkTree(node[2])::])
        if node[0]=="reverse_expr":
            return list(self.walkTree(node[1]))[::self.walkTree(node[2])]
        if node[0]=="Get_range_expr":
            return list(self.walkTree(node[1]))[self.walkTree(node[2]):self.walkTree(node[3])]
        if node[0]=="Get_range_expr_inc":
            return list(self.walkTree(node[1]))[self.walkTree(node[2]):self.walkTree(node[3]):self.walkTree(node[4])]
        if node[0]=="Create_range_inc":
            return list(range(self.walkTree(node[1]), self.walkTree(node[2]), self.walkTree(node[3])))

        if node[0]=="Create_range":
            return range(self.walkTree(node[1]), self.walkTree(node[2]))
        if node[0]=="FOR_IN_EXPR":

            t=self.env

            var = self.walkTree(node[1])
            expr = self.walkTree(node[2])
            statement = node[3]

            if(len(node) > 4):
                var1 = self.walkTree(node[4])

                for i,v in enumerate(expr):
                    self.env[var] = i
                    self.env[var1]= self.walkTree(v)
                    for j in statement:
                        self.walkTree(j)
                self.env = t
                return
            for i in expr:
                self.env[var] =  self.walkTree(i)
                for j in statement:
                    self.walkTree(j)
            self.env = t
        if node[0]=="RET":
            return self.walkTree(node[1])

        if node[0]=="public_name":
        	return {node[1]:node[2]}
        if node[0]=="Normal_Class":
        	identifier = node[2][0]
        	self.env[node[1]]= {"Type":"Class", "Methods":{}}
        	for i in node[2]:
        		res = self.walkTree(i)
        		self.env[node[1]]["Methods"].update(res)


        	#print(node[1],node[2])
        if node[0]=="var_assign_expr_expr":
        	i = self.walkTree(node[1])
        	print(i)
        	return setattr(i,i,i)
        	return getattr(i,"ok")




        if node[0]=="Chain_Expr_tuple":
        	expr1 = self.walkTree(node[1])

        	args = [self.walkTree(i) for i in node[3][1]]

        	return getattr(expr1, node[2])(*args)
        if node[0]=="Chain_Expr_call":
        	try:
                 expr1 = self.walkTree(node[1])

                 #args = [self.walkTree(i) for i in node[3][1]]

                 return getattr(expr1, node[2])()
        	except:
                 method = self.walkTree(node[1])


                 for i in method["Methods"][node[2]]:
                     self.walkTree(i)
                 return
        if node[0]=="Chain_Expr":
        	expr1 = self.walkTree(node[1])
        	try:
        		return getattr(expr1, node[2])
        	except:
        		return expr1["Methods"][node[2]]
        		return 0
        	return getattr(expr1, expr)
        	pass
        if node[0]=="Excel_Live":

        	excel = win32com.client.GetActiveObject("Excel.Application")
        	self.env["EXCEL"] = excel

        if node[0]=="case":
        	return node[1],node[2]
        if node[0]=="match":
        	case = self.walkTree(node[1])
        	for i in node[2]:

        		val = self.walkTree(i)

        		if val[0][1]=="_":
        			return self.walkTree(val[1][0])
        		value = self.walkTree(val[0])

        		if value==case:

        			return self.walkTree(val[1][0])

        if node[0]=="elif_expr":
                res = self.walkTree(node[1])
                if res:
                	for i in node[2]:
        	        	self.walkTree(i)
        	        return res
                return None
        if node[0]=="var_assign_lmd":
        	ret=self.walkTree(node[2])
        	print(ret[1][1])
        	args= [i[1] for i in ret[1][1] if i[0]=="var"]
        	args={key : 0 for key in args}
        	print(args)
        	self.env[node[1]] = {"body": ret[0],"args":args}
        if node[0]=="LMD_expr":
        	return (node[2],node[1])
        if node[0]=="LMD":
        	return (node[2],node[1])
        if node[0]=="NULL_COL":
        	if not self.walkTree(node[1]): return self.walkTree(node[2])
        	return self.walkTree(node[1])
        if node[0]=="if_statement":
        	res= self.walkTree(node[1])
        	if res:
        		for i in node[2]:
        			t = self.walkTree(i)

        if node[0]=="var_assign_type_float":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            self.env[node[1]] = (self.defaults[float],'float')
        if node[0]=="var_assign_type_bool":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            self.env[node[1]] = (self.defaults[bool],'bool')
        if node[0]=="var_assign_type_dict":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            self.env[node[1]] = (self.defaults[dict],'dict')

        if node[0]=="var_assign_type_string":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            self.env[node[1]] = (self.defaults[str],'string')
        if node[0]=="var_assign_type_str_expr":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            val = self.walkTree(node[2])
            if type("")!=type(val):
                print(f"TypeError: Var '{node[1]}' type is {"STR"} not type {type(val).__name__} '{val}' at line_number: {lexer.lineno+1}")
                exit(100)
            self.env[node[1]] = (val,'string')

        if node[0]=="var_assign_type_int_expr":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            val = self.walkTree(node[2])
            if type(0)!=type(val):
                print(f"TypeError: Var '{node[1]}' type is {"INT"} not type {type(val).__name__} '{val}'")
                exit(100)
            self.env[node[1]] = (val,'int')
        if node[0]=="var_assign_type_float_expr":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            val = self.walkTree(node[2])
            if type(0.1) != type(val):
                print(f"TypeError: Var '{node[1]}' type is {"FLOAT"} not type {type(val).__name__} '{val}'")
                exit(100)
            self.env[node[1]] = (val, 'float')
        if node[0]=="var_assign_type_bool_expr":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            val = self.walkTree(node[2])
            if type(True) != type(val):
                print(f"TypeError: Var '{node[1]}' type is {"BOOL"} not type {type(val).__name__} '{val}'")
                exit(100)
            self.env[node[1]] = (val, 'bool')

        if node[0]=="var_assign_type_dict_expr":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            val = self.walkTree(node[2])

            if type({"a":9}) != type(val):
                print(f"TypeError: Var '{node[1]}' type is {"DICT"} not type {type(val).__name__} '{val}'")
                exit(100)
            self.env[node[1]] = (val, 'dict')




        if node[0]=="import_dia_module":
        	file = self.builtins["read"](node[1]+".dia")
     	  	
        	file = file.split(";")
        	file = [p for p in file if p != '']

        	for i in file:
        		
        		b=parser.parse(lexer.tokenize(i))
        		#print(b)
        		if b[0]=="fun_def":
        			self.env[node[1]+"_"+b[1]]=b[2]

                    

        		if b[0][0:3]=="var":
        			if len(b)<3: self.walkTree((b[0],node[1]+"_"+b[1]))
        			else : self.walkTree((b[0],node[1]+"_"+b[1],(b[2])))

        if node[0] == "var_assign_type_int":
            if node[1] in self.env:
                raise ValueError(f"{node[1]} is already defined")
            self.env[node[1]] = (self.defaults[int],'int')



        if node[0]=='import_py_module':
            cwd = os.getcwd()
            sys.path.insert(0, cwd)
            module = __import__(self.walkTree(node[1])[1:-1])

        	#func = getattr(module, "p")
        	#result = func()
            self.builtins[module.__name__] = module
            #print(self.builtins)
        	#print(self.builtins)
            return

        if node[0]=="builtin_funcs":


        	if node[1]=="time_now":
        		return self.builtins[node[1]]()
        	args=[]
        	if len(node) >2 :args = [self.walkTree(i) for i in node[2][1]]
        	try:
        		module, func = node[1].split("_", 1)

        		func = getattr(self.builtins[module], func)

        		return func(*args)

        	except: pass
        	#if node[1] not in self.builtins: return "Error",exit(1)
        	if node[1] == "read":

        		return self.builtins[node[1]](*args)
        		return
        	if node[1]=="write":

        		self.builtins[node[1]](*args)
        		return
        	if node[1]=="append":

        		self.builtins[node[1]](*args)
        		return

        	if node[1]=="sub_str":

        		return self.builtins[node[1]](*args)
        	if node[1]=="len":


        		return self.builtins[node[1]](*args)
        	if node[1]=="sum":

        		return self.builtins[node[1]](*args)

        	if node[1] == "type":
                	print(node[2])
        	        return 
                

        	return self.builtins[node[1]](*args)
        if node[0]=="expr_EQEQ":

        	return self.walkTree(node[1])==self.walkTree(node[2])
        if node[0]=="bigger_than": return self.walkTree(node[1])>self.walkTree(node[2])
        if node[0]=="less_than": return self.walkTree(node[1])<self.walkTree(node[2])
        if node[0]=="uminus": return -self.walkTree(node[1])
        if node[0]=="not": return not self.walkTree(node[1])
        if node[0]=="and": return self.walkTree(node[1]) and self.walkTree(node[2])
        if node[0]=="or": return self.walkTree(node[1]) or self.walkTree(node[2])

        if node[0]=="con_list":
                print(node[1],1)
                return list(self.walkTree(node[1]))
        if node[0]=="while_loop_expr":
        	while self.walkTree(node[1]):
        		for i in node[2]:
        			self.walkTree(i)
        if node[0]=="expr_GEQEQ": return self.walkTree(node[1]) >= self.walkTree(node[2])
        if node[0]=="expr_LEQEQ": return self.walkTree(node[1]) <= self.walkTree(node[2])

        if node[0]=="set_index":
            # have to add in try catch for int is not subcriptable
            # essentially gets the variable list ie a=[9,9]
            # returns [9,9]

            key = self.walkTree(node[2])[0]


            var = self.env[node[1]]

            expr = self.walkTree(node[3])

            if type(var).__name__ == "set":
                raise TypeError(f"Return Type:{lst} cannot be indexed because it is typeof {type(lst)._name_}")

            if type(var).__name__ == "dict":

                try:



                    self.env[node[1]][key] = expr
                    return
                except:

                    self.env[node[1]][str(node[1])] = expr


                    return
            # print(a,a[0],350,node[2])
            # print(lst[0])
            # this gets the index and then gets the index from the above list then returns a list or if its a another variable that
            var[key] = expr
            # print(lst)
            return

        if node[0]=="get_index":

        	#have to add in try catch for int is not subcriptable
        	#essentially gets the variable list ie a=[9,9]
            #returns [9,9]

        	lst=self.walkTree(node[1])

        	if type(lst).__name__=="set":
        		raise TypeError(f"Return Type:{lst} cannot be indexed because it is typeof {type(lst)._name_}")

        	if type(lst).__name__=="dict":

        		try:

        			key = self.walkTree(node[2])[0]

        			d = dict(self.walkTree(node[1]))
        			return d[key]
        		except:
        			key = node[2][1][0][1]
        			d = dict(self.walkTree(node[1]))
        			return d[key]
        	#print(a,a[0],350,node[2])
        	#print(lst[0])
        	#this gets the index and then gets the index from the above list then returns a list or if its a another variable that
        	lst = lst[self.walkTree(node[2])]


        	return lst
        #get_index_expr_null
        if node[0]=="get_index_expr_null":

        	#have to add in try catch for int is not subcriptable
        	#essentially gets the variable list ie a=[9,9]
            #returns [9,9

        	try:
        	      	lst=self.walkTree(node[1])
        	except:
              		return -1

        	#print(lst,8)

        	if lst==None:

        		return None

        	if type(lst).__name__=="set":
        		return None

        	if type(lst).__name__=="dict":
        		#print(lst,8)
        		try:

        			key = self.walkTree(node[2])[0]

        			#print("kry",key)
        			d = dict(self.walkTree(node[1]))
        			#print(d)

        			return d[key]
        		except:
        			try:

        				key = node[2][1][0][1]

        				d = dict(self.walkTree(node[1]))

        				return d[key]
        			except:

        				return None

        	#print(a,a[0],350,node[2])
        	#print(lst[0])
        	#this gets the index and then gets the index from the above list then returns a list or if its a another variable that
        	try:

        		lst = lst[self.walkTree(node[2])[0]]

        	except:
        		lst=None
        	#print(lst)

        	return lst
	#$
        if node[0]=="get_index_null":

        	#have to add in try catch for int is not subcriptable
        	#essentially gets the variable list ie a=[9,9]
            #returns [9,9]

        	lst=self.walkTree(node[1])

        	#print(lst,8)

        	if lst==None:

        		return None

        	if type(lst).__name__=="set":
        		return None

        	if type(lst).__name__=="dict":
        		#print(lst,8)
        		try:

        			key = self.walkTree(node[2])[0]
       			#print("kry",key)
        			d = dict(self.walkTree(node[1]))
        			#print(d)

        			return d[key]
        		except:
        			try:

        				key = node[2][1][0][1]

        				d = dict(self.walkTree(node[1]))

        				return d[key]
        			except:

        				return None

        	#print(a,a[0],350,node[2])
        	#print(lst[0])
        	#this gets the index and then gets the index from the above list then returns a list or if its a another variable that
        	try:

        		lst = lst[self.walkTree(node[2])[0]]
        	except:
                 if(len(node[2][1]) >=2):
                    for i in node[2][1]:
                        try:
                            item_value = lst[self.walkTree(i)]
                            return item_value
                        except:
                            pass
                            #return lst
       		lst=None
        	#print(lst)

        	return lst

        if node[0]=="get_key-value":
        	pass

        if node[0]=="INC":
            self.env[node[1]]+=1
            return self.env[node[1]]

        if node[0]=="condition_true":
            return node[1]
        if node[0]=="condition_false":
            return node[1]

            # Existing cases...

        if node[0] == 'import':
            #node 2 is the list of codelines
            module_name = node[1]
            print(node[2])
            #runs trhough them and exe them
            for i in node[2]:
                print(i,100)
                prt=parser.parse(lexer.tokenize(i))
                if prt[0]=='fun_def_args':

                    t=self.env
                    self.env=self.Func
                    self.walkTree(prt)

                    #r                    m: statements            vars of m
                    self.Func[node[1]]= {prt[1]:self.Func[prt[1]],"vars":prt[2]}
                    del self.Func[prt[1]]
                    print(self.Func)

                    self.env=t
                elif prt[0]=='fun_def_args':
                    pass
                    #print(7)
                else:

                    self.walkTree(prt)
            return node[2]

        if node[0]=="LMD":
        	t={}
        	t = self.env
        	self.env={}
        	#print(node[1])

        	for i, j in zip(node[1], node[3]):




        		i = i[1]

        		j = self.walkTree(j)

        		self.env[i]=j
        		#print(self.env,"7",i,j)


        	for i in node[2]:
        		#print(i)
        		r= self.walkTree(i)

        	self.env =  t


        	return r
        if node[0]=="def_struct":
        	if node[1] in self.struct_env:
        		raise RuntimeError(f"Error: Struct '{node[1]}' is already defined and cannot be redefined.")

        	self.struct_env[node[1]] ={}

        	for i in node[2]:
        		i = self.walkTree(i)
        		#print(i[1])
        		self.struct_env[node[1]][i[1]] = [None,i[0]]

        	#self.struct_env
        	return

        if node[0]=="def_struct_instance":
        	if node[1] in self.struct_env:
        		raise RuntimeError(f"Error: Struct '{node[1]}' is already defined and cannot be redefined.")
        	#print(node)
        	self.struct_env[node[1]] ={}

        	for i in node[2]:
        		i = self.walkTree(i)
        		#print(i[1])
        		self.struct_env[node[1]][i[1]] = [None,i[0]]

        	#self.struct_env
        	return

        if node[0]=="IDENTIFY":
        	return [node[1],node[2]]
        	return ()
        if node[0]=="assign_attr":
        	try:
        		#print(self.struct_env)
        		if self.struct_env[node[1]][node[2]][1]:
        			self.struct_env[node[1]][node[2]][0]= self.walkTree(node[3])
        			#print(7)
        			return
        		#print(self.struct_env[node[1]][node[2]])
        		if (type(self.walkTree(node[3]))._name_!= self.struct_env[node[1]][node[2]][1]):
        			raise InvalidTypeError(f"Invalid type {node[1]}.{node[2]} type: {self.struct_env[node[1]][node[2]][1]} does not match type :  {type(self.walkTree(node[3]))._name_}")
        		self.struct_env[node[1]][node[2]][0]= self.walkTree(node[3])



        		#print(self.struct_env)
        		return

        	except Exception as e:
        		#print(self.env,100,node[1])
        		#print(self.env)
        		self.env[node[1]][node[2]][0] = self.walkTree(node[3])
        		self.struct_env[node[1]] = self.env[node[1]]
        		return
        if node[0]=="get_attr":
        	if node[1] in self.struct_env:
        		#print(self.struct_env[node[1]][node[2]])
        		return self.struct_env[node[1]][node[2]][0]
        	return

        if node[0] == 'num':
            return int(node[1])
        if node[0]=="float":

        	return float(node[1])
        if node[0] == 'str':
            return node[1] # Strip quote
        if node[0]=='list':
            #print(node[1])
            return [self.walkTree(i) for i in node[1]]
            #print([self.walkTree(i) for i in node[1]])
           # print(node[1],100)

        if node[0]=="tuple":
          return  tuple([self.walkTree(i) for i in node[1]])
        if node[0]=="set":
          return set([self.walkTree(i) for i in node[1]])




        if node[0]=="dict":
            #print(node[1])
            return {key[1]: self.walkTree(val) for key, val in node[1].items()}

        if node[0]=="RET":
            return self.walkTree(node[1])
        if node[0]=="var_peq":
            #print(node[2])
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		self.env[node[1]] = (var[0]+val,type(var[0]).__name__)
            		#print(self.env[node[1]])

            	else: print(f"Type Error"); exit()

            self.env[node[1]]+=val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

            if node[1] in self.watch:
                for i in self.watch[node[1]]:
                    self.walkTree(i)
            return
        if node[0]=="var_seq":
            val = self.walkTree(node[2])
            var = self.env[node[1]]
            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		self.env[node[1]] = (var[0]-val,type(var[0]).__name__)
            		print(self.env[node[1]])
            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] -= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])
            if node[1] in self.watch:
                for i in self.watch[node[1]]:
                    self.walkTree(i)
            return
        if node[0]=="var_deq":
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if (type(var[0])==

                        type(val)):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]/val,type(var[0]).__name__)
            		print(self.env[node[1]])
            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] /= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

            if node[1] in self.watch:
                for i in self.watch[node[1]]:
                    self.walkTree(i)
            return self.env[node[1]]
        if node[0]=="var_meq":
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]*val,type(var[0]).__name__)
            		print(self.env[node[1]])
            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] *= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

            if node[1] in self.watch:
                for i in self.watch[node[1]]:
                    self.walkTree(i)
            return self.env[node[1]]

        if node[0]=="var_check_peq":
            #check the type
            if(node[1] not in self.env):
            	value = self.walkTree(node[2])
            	self.env[node[1]] = self.defaults.get(type(value))
            	return
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]+val,type(var[0]).__name__)

            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] += val
            return self.env[node[1]]
        if node[0]=="var_check_seq":

            if(node[1] not in self.env):
            	value = self.walkTree(node[2])
            	self.env[node[1]] = self.defaults.get(type(value))
            	return
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]-val,type(var[0]).__name__)

            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] -= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

                return
            return self.env[node[1]]

        if node[0]=="var_check_deq":

            if(node[1] not in self.env):
            	value = self.walkTree(node[2])
            	self.env[node[1]] = self.defaults.get(type(value))
            	return
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]/val,type(var[0]).__name__)
            		print(self.env[node[1]])
            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] /= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

                return
            return self.env[node[1]]

        if node[0]=="var_check_meq":

            if(node[1] not in self.env):
            	value = self.walkTree(node[2])
            	self.env[node[1]] = self.defaults.get(type(value))
            	return
            val = self.walkTree(node[2])
            var = self.env[node[1]]

            if isinstance(var,tuple):
            	if type(var[0])==type(val):
            		#add to make sure an int cant become a float
            		self.env[node[1]] = (var[0]*val,type(var[0]).__name__)

            		return self.env[node[1]]
            	else: print(f"Type Error"); exit()
            self.env[node[1]] *= val
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

                return
            return self.env[node[1]]

        if node[0]=='var_arreq':
            self.env[node[1]].append(self.walkTree(node[2]))
            if node[1] in self.var_his:
                self.var_his[node[1]].append(self.env[node[1]])

            if node[1] in self.watch:
                for i in self.watch[node[1]]:
                    self.walkTree(i)
            return

        if node[0] == "builtin-func":
            #print(node)
            if node[2]=="str":
                args = [self.walkTree(i) for i in node[3]][0]
                try:
                    return getattr(self.env[node[1]],args[0])
                except:
                    return str(self.env[node[1]])
            if node[1] == "math":
                if Func[node[1]] == 1:
                    import math

                else:
                    return -1
                f = getattr(math, node[2])
                try:
                    return f(*[self.walkTree(i) for i in node[3]])

                except TypeError:
                    print(
                        f"Too many argumens passed to module:{node[1]} of function:{node[2]} was expecting:{len(inspect.signature(f).parameters)}")
                    return -1
            elif node[2]=="Len":
                a = self.env[node[1]]
                #print(len(a))
                if isinstance(a,list) or isinstance(a,str):
                    return len(a)

            else:
                module_name, func_name, args = node[1], node[2], node[3]

                # Handle functions from imported modules or user-defined functions
                if module_name in self.Func and func_name in self.Func[module_name]:
                    func = self.Func[module_name][func_name]
                    #make t =  env to preserve vars

                    t = self.env

                    self.env = {}
                    for i,v in enumerate(self.Func[module_name]['vars']):
                        self.env[v]=args[i]



                    last=0
                    for i in func:
                        #print(7777)
                        #doesnt compute correclt without double self.walktree mayb ebcause of no basicexe at the print
                        self.walkTree(i)
                        last=i

                    self.env = t
                    return last
                else:
                    print(f"Unknown function '{func_name}' in module '{module_name}'")
                    return -1

        if node[0]=='str_chg':
            s=self.env[node[1]]
            s= [i for i in s if i!="'" and i!='"']
            print(s)
            s[self.walkTree(node[2])]=self.walkTree(node[3])[1:-1]

            self.env[node[1]]="".join(s)

        if node[0]=='list_chg':
            s=self.env[node[1]]
            s= [i for i in s if i!="[" and i!=']']

            s[self.walkTree(node[2])]=self.walkTree(node[3])

            self.env[node[1]]=s

        if node[0] == 'dict_chg':
            s = self.env[node[1]]

            s[self.walkTree(node[2])] = self.walkTree(node[3])

            self.env[node[1]] = s



        if node[0]=='import':
            if node[1] in Func:
                if Func[str(node[1])] == 0:
                    if str(node[1])=="math":
                        Func[str(node[1])]=1
                        return 100
                else:
                    print(f"Error already imported '{node[1]}'")
                    return -1
            else:
                raise ValueError("Import doesnt exist")
        if node[0]=="if_stmt_elif":
                res = self.walkTree(node[1])
                if res:
                	for i in node[2]: self.walkTree(i)
                	return
                for i in node[3]:
                	res = self.walkTree(i)
                	if res: return
                else:
                	for i in node[4]: self.walkTree(i)

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])

           # print(node[2],result,node[1])
            if result:
                for i in node[2]:

                    if (i[0] == "RET"):
                        return self.walkTree(i)
                    self.walkTree(i)
                #return last stmt
                return
                #return self.walkTree(node[2][-1])
            for i in node[3]:
                if (i[0] == "RET"):
                    return self.walkTree(i)
                self.walkTree(i)

            #return self.walkTree(node[3][-1])

        if node[0] == 'if_stmt_if':
            result = self.walkTree(node[1])

            if result:
                for i in node[2]:

                    if (i[0] == "RET"):

                        return self.walkTree(i)
                    self.walkTree(i)
                # return last stmt
                return
                return self.walkTree(node[2][-1])

            return
            return self.walkTree(node[2][-1])


        if node[0] == 'condition_eqeq':

            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':

            self.env[node[1]] = node[2]

        if node[0]=='fun_def_args':
            #a:0 etc

            arg = node[2][1]
            #print(arg)
            args = [i[1] for i in arg if i[0]=="var"]
            assigned_args = [(i[0][1],self.walkTree(i[1])) for i in arg if i[0][0] == "var"]
            #print(assigned_args)
            non_args = [i for i in arg if i[1] not in args]


            args={key : 0 for key in args}
            #len needed
            l=0
            for i in assigned_args:
                l+=1
                args[i[0]] = i[1]

            #print(args)
            #self.env[node[1]] = {"body":node[3],"args":args}
            self.env[(node[1],len(args))] = {"body":node[3],"args":args}
            self.env[(node[1],"Default")] = {"body":node[3],"args":args,"Largs":l}


            for i in non_args:
            	#checks if its a list
            	if i[0]=="list":
            		i=i[1] #
            		if i[0][0]=="var":
            			self.env[node[1]]["args"][i[0][1]]=self.walkTree(i[1])
            #print(f"These values were ignored {non_args} because they dont match thr correct arguments format.")


            #print(self.env)


            #print(self.env)
            return
        if node[0] == 'fun_call':
            #print(7)
            lst = self.env[node[1]]
            once =0

            if node[1] in IS_Once:
                once+=1
            IS_Once.append(node[1])
            #print(lst,10)
            if "args" in lst:
                return self.walkTree(("fun_call_args",node[1],))
            for i in self.env[node[1]]:

                try:
                    if i[0]=="Once_statement":
                        if once==0:
                            self.walkTree(i)
                        once +=1
                        continue
                    if(i[0]=="RET"):
                        for j in self.defered:
                            self.walkTree(j)
                        return self.walkTree(i)
                    self.walkTree(i)
                    continue
                except LookupError:
                    print("Undefined function '%s'" % node[1])
                    return 0
            for i in self.defered:
                self.walkTree(i)
            return
            return self.walkTree(self.env[node[1]][-1])

        if node[0] == 'fun_call_args':
            vals = self.walkTree(node[2]) if len(node) > 2 else []

            once = 0
            if (node[1],len(vals)) in IS_Once:
                once+=1
            IS_Once.append((node[1],len(vals)))
            #print(self.env[(node[1],len(vals))])
            if (node[1],"Default") in self.env:
                t = self.env

                if (node[1],len(vals)) in self.env:
                    self.env = self.env[(node[1],len(vals))]['args']
                    Param = len(vals)
                else:
                    self.env = self.env[(node[1], "Default")]['args']
                    Param= "Default"
                    ## add checking




                # print(self.env)
                # print(t[node[1]]['body'],100)

                self.env[node[1]] = t[(node[1],Param)]

                # print(t,self.env,node[1])

                for k, v in zip(t[(node[1],Param)]['args'], vals):
                    self.env[k] = v
                # print(self.walkTree(t[node[1]]['body']),1000)
                for i in t[(node[1],Param)]['body']:
                    # print(i,100)

                    try:
                        if i[0] == "Once_statement":
                            if once == 0:
                                temp = self.walkTree(i)
                            once += 1
                            temp = None
                            continue
                        if (i[0] == "RET"):
                            temp = self.walkTree(i)

                            break
                        #       print(self.walkTree(i),100)
                        temp = self.walkTree(i)

                    except LookupError:
                        print("Undefined function '%s'" % node[1])
                        return 0

                # ie the last statement
                for j in self.defered:
                    self.walkTree(j)
                self.env = t

                return temp
                return

            #file management
            if node[1]=="open":
                file = (self.walkTree(node[2][0]))
                return open(f"{file}","r")

            # for i,v in enumerate(t[node[1]]):
            #
            #     t[node[1]][v]=self.walkTree(node[2][i])


            #print(self.env[node[1]],100)
            t = self.env
            self.env = self.env[node[1]]['args']
            #print(self.env)
            #print(t[node[1]]['body'],100)

            self.env[node[1]] = t[node[1]]

            #print(t,self.env,node[1])




            for k,v in zip(t[node[1]]['args'],vals):

                self.env[k]=v
            #print(self.walkTree(t[node[1]]['body']),1000)
            for i in t[node[1]]['body']:
                #print(i,100)

                try:

                    if(i[0]=="RET"):
                        temp = self.walkTree(i)
                        break
             #       print(self.walkTree(i),100)
                    temp=self.walkTree(i)

                except LookupError:
                    print("Undefined function '%s'" % node[1])
                    return 0


            #ie the last statement
            self.env = t
            return temp
           # print(self.env[node[1]][-1],"ok")

        if node[0] == 'add':

            arg1 = self.walkTree(node[1])

            arg2 = self.walkTree(node[2])
            tuples = -1

            if isinstance(arg1, tuple) and isinstance(arg2, tuple):
                pass
            elif isinstance(arg1,tuple) or isinstance(arg2,tuple):

                if isinstance(arg1,tuple):
                    tuples+=1
                    if (len(arg1) < 2):
                        arg1 = arg1[0]
                if isinstance(arg2,tuple):
                    tuples+=1
                    if (len(arg2) < 2):
                        arg2=arg2[0]







            if isinstance(arg1,list) and isinstance(arg2,str):
                return [i+arg2 for i in arg1]
            if isinstance(arg1,str) and isinstance(arg2,list):
                return [arg1+i for i in arg2]
            if isinstance(arg1,list) and isinstance(arg2,int):

            	return arg1+[arg2]
            if(tuples!=-1 and tuples>2):
                if tuples==0:
                    return
                else:
                    return

            return arg1 + arg2

        elif node[0] == 'sub':
            try:
                return self.walkTree(node[1]) - self.walkTree(node[2])
            except TypeError:
                if isinstance(self.walkTree(node[1]),list) and isinstance(self.walkTree(node[2]),int):
                    l = list(self.walkTree(node[1]))
                    l.pop(self.walkTree(node[2]))
                    return l

        elif node[0] == 'mul':
            arg1 = self.walkTree(node[1])
            arg2 = self.walkTree(node[2])
            if(isinstance(arg1,tuple) or isinstance(arg2,tuple)):
                if isinstance(arg1,tuple):
                    if (len(arg1) < 2):
                        arg1 = arg1[0]
                else:
                    if (len(arg2) < 2):
                        arg2 = arg2[0]
            if isinstance(self.walkTree(node[1]),str):
                return self.walkTree(node[1]) * self.walkTree(node[2])
            return arg1 * arg2

        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        if node[0]=='mod':

            return self.walkTree(node[1])% self.walkTree(node[2])
        if node[0]=="expo": return self.walkTree(node[1])**self.walkTree(node[2])
        if node[0]=="floor": return self.walkTree(node[1])//self.walkTree(node[2])

        if node[0] == 'var_assign':
            #print(node[2],node[1])
            val = self.walkTree(node[2])


            try: var=self.env[node[1]]
            except: var =[]

            if isinstance(var,tuple):
                print(var)
                #check type for something like var,int etc
                if (len(var) < 2):
                    self.env[node[1]] = (val, type(val).__name__)
                else:
                    if (type(val).__name__ != var[1]):
                        print(f"ERRROOROROR incorrect type assigned to {var} {type(val).__name__} {val}")
                    else:
                        self.env[node[1]] = (val, type(val).__name__)

                # if type(var[0])!=type(val):
                #
                #     print(f"TypeError: Var '{node[1]}' type is {type(var[0]).__name__} not type {type(val).__name__} '{val}'")
                #     exit()

                if node[1] in self.var_his:
                    self.var_his[node[1]].append(self.walkTree(node[2]))

                if node[1] in self.watch:

                    for i in self.watch[node[1]]:
                        self.walkTree(i)

            	#print(777,self.env[node[1]]) added this to ensure it stays the same type and doesnt get changed
                return node[1]
            if node[2][0] == "var" and node[2][1] in struct_env:


            	#print(self.struct_env)
            	d = {}
            	j=self.walkTree(node[2])

            	#print(j)
            	for i,v in dict(j).items():
            		d[i]=v
            	#print(d,100)
            	#d = self.walkTree(node[2])
            	self.struct_env[node[1]] = d
            	#print(self.struct_env)
            	return

            if isinstance(val,list):

                self.env[node[1]] = list(val)
                if node[1] in self.var_his:
                    self.var_his[node[1]].append(self.walkTree(node[2]))

                if node[1] in self.watch:
                    for i in self.watch[node[1]]:
                        self.walkTree(i)
                return node[2]
            if isinstance(val,dict):
                self.env[node[1]] = dict(val)
                if node[1] in self.var_his:
                    self.var_his[node[1]].append(self.walkTree(node[2]))

                if node[1] in self.watch:
                    for i in self.watch[node[1]]:
                        self.walkTree(i)
                return node[2]

            self.env[node[1]] = val
            if node[1] in self.var_his:

                self.var_his[node[1]].append(self.env[node[1]])
                if node[1] in self.watch:
                    for i in self.watch[node[1]]:
                        self.walkTree(i)
                return
            self.var_his[node[1]] = [self.walkTree(node[2])]
            if node[1] in self.watch:

                for i in self.watch[node[1]]:

                    self.walkTree(i)
            #print(self.env,777)
            if self.env[node[1]]==True or self.env[node[1]]==False:
                self.env[node[1]] = 1 if self.env[node[1]] == True else 0
                if node[1] in self.var_his:
                    self.var_his[node[1]].append(self.env[node[1]])

                if node[1] in self.watch:
                    for i in self.watch[node[1]]:
                        self.walkTree(i)
                return node[1]
            return node[1]

        if node[0] == 'var':
            #print(7)
            #print(node[1],100)
            #first try excepts is for list
            try:

            	var = self.env[node[1]]

            	if(isinstance(var,tuple)):
                    if var[0]=="LAZY":

                        self.env[node[1]] = self.walkTree(var[1])
                        return self.env[node[1]]
                    if var[1] == 'struct':
                        #do something
                        return var[0]
                        return
                    return self.walkTree(var[0])
            except: pass
            try:
            	obj = self.env[self.walkTree(node[1])]
            	if(isinstance(obj, io.TextIOWrapper)):
            		return obj
            except:
            	pass

            try:

                if isinstance(self.env[node[1]], dict):
                    try:
                        key = self.walkTree(node[2])[0]
                        return self.env[node[1]][key]
                    except:
                        return dict(self.env[node[1]])
                if isinstance(self.env[node[1]],list):
                    try:
                        #print(self.env[node[1]][int(self.walkTree(node[2])[0])]," node 2")
                        return self.env[node[1]][int(self.walkTree(node[2])[0])]
                    except:
                        return self.env[node[1]]

            except:

                pass

            try:

                return self.env[node[1]]
            except LookupError:
                try:

                	#print(self.struct_env[node[1]],node[1])
                	return self.struct_env[node[1]]
                except:
                	raise ValueError("")
                	print("Undefined variable '"+node[1]+"' found!")
                	return 0

        if node[0] == 'for_loop':

            if node[1][0] == 'for_loop_setup':

                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                if loop_limit<loop_count:
                    for i in range(loop_count-1, loop_limit-1,-1):
                        #res = self.walkTree(node[2])

                        for j in node[2]:
                            res=self.walkTree(j)
                            if res is not None:
                                print(res)
                        self.env[loop_setup[0]] = i
                    del self.env[loop_setup[0]]
                else:

                    #0.2
                    str1 = self.walkTree(node[2][0][1])
                    #print(node[2][0])
                    if len(node[2])==1 and node[2][0][0]=="print_stmt":
                    	str1 = str(self.walkTree(node[2][0][1]))+"\n"
                    	print((str1)*loop_limit)

                    	return
                    if len(node[2])==1 and node[2][0][0]=="var_assign":

                    	self.walkTree(node[2][0])

                    	return
                    if len(node[2])==1 and node[2][0][0]=="var_peq":
                    	tup  = node[2][0][2][1]*loop_limit
                    	#print((node[2][0][2][0],tup))
                    	new_node = (node[2][0][0],node[2][0][1],(node[2][0][2][0],tup))
                    	self.walkTree(new_node)
                    	return
                    #for i in node[2]:
                    #	if i[0]=="print_stmt":
                    #		print(i[1],99,self.W)
                    #		str1 = self.walkTree(i[1])
                    #		print((str1+"\n")*loop_limit)
                    #return
                    for i in range(loop_count+1, loop_limit+1):
                        #res = self.walkTree(node[2])
                        for j in node[2]:
                            res=self.walkTree(j)

                            if res is not None:
                                #print(res)
                                pass
                        self.env[loop_setup[0]] = i
                    del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'print_stmt':
            #print(node[1])
            #print(7)
            #print(node)




            #print(self.env)
            p = self.walkTree(node[1])
            for i in p:
                print(i)
            #i=('print_stmt', ('num', 7))
#            return self.walkTree(i)
            return
            #i=input("input:")
#            l=BasicLexer()
#            p=BasicParser()
#            tree =p.parse(l.tokenize(i))
#            print(tree)
#            if tree=="":
#            	return
#            return self.walkTree(tree)
            for i in node[1]:
                print(node[1])
                #had to add in because import name.nam() doesnt parse function statements correclty

                print(self.walkTree(i))
            #print(*[self.walkTree(arg) for arg in node[1]])

            return
        if node[0] == 'f_str':
            s=node[1]
            bnum = 0
            fstr = ''
            for i in s:

                if i == '{' and bnum == 0:

                    bnum = 1
                elif i == '}' and bnum == 1:
                    try:
                        a =lexer.tokenize(fstr)


                        t = parser.parse(lexer.tokenize(fstr))

                        # print(f"t is {self.walkTree(t)}")

                        # s = s.replace('{' + fstr + '}', str(BasicExecute(t, self.env, Func, self.temp_env)))
                        s = s.replace('{' + fstr + '}', str(self.walkTree(t)))


                    except:
                        pass
                    try:

                        s = s.replace('{' + fstr + '}', str(self.env[fstr]))


                    except:
                        pass
                    bnum = 0

                    fstr = ''
                elif bnum == 1:

                    fstr += i
                else:
                    pass



            return s[1:-1]

        if node[0] == 'print_stmt_f':

            for i in node[1]:
                    if i[0]=='str':
                        s=self.walkTree(i)

                        #bracket num to recognize the {
                        bnum=0
                        fstr=''
                        for j in s:

                            if j=='{' and bnum==0:

                                bnum=1
                            elif j=='}' and bnum==1:
                                try:

                                    t = parser.parse(lexer.tokenize(fstr))
                                    #print(f"t is {self.walkTree(t)}")
                                    #s = s.replace('{' + fstr + '}', str(BasicExecute(t, self.env, Func, self.temp_env)))
                                    s=s.replace('{' + fstr + '}',str(self.walkTree(t)))

                                except:
                                    pass
                                try:


                                    s=s.replace('{'+fstr+'}',str(self.env[fstr])[1:-1])


                                except:
                                    pass
                                bnum=0
                                fstr=''
                            elif bnum==1:
                                fstr+=j
                            else:
                                pass
                        print(s)
                        return



                    else:print(self.walkTree(i))

            return


            #print(*[self.walkTree(arg) for arg in node[1]])





def multiline_input(prompt="basic > "):
    print("Enter multiline code. Type 'END' on a new line to finish.")
    lines = []
    while True:
        line = input(prompt)
        if line.strip().lower() == 'end':  # Check for the END keyword to finish input
            break
        lines.append(line)
    return "\n".join(lines)  # Combine lines into a single string
# Function to read a file


def ensure_console():
    """Attach to existing console or open a new one, and redirect I/O."""
    kernel32 = ctypes.windll.kernel32

    # Try to attach to parent process's console
    if not kernel32.AttachConsole(-1):  # -1 = ATTACH_PARENT_PROCESS
        # If attach failed, create a new one
        if not kernel32.AllocConsole():
            return False  # total failure

    # Redirect standard streams
    sys.stdout = open("CONOUT$", "w", buffering=1)
    sys.stderr = open("CONOUT$", "w", buffering=1)
    sys.stdin = open("CONIN$", "r")
    return True




MessageBoxA = ctypes.windll.user32.MessageBoxA
builtins = {
    "read": lambda filename: read_file(filename),
    "write": lambda filename, content: write_file(filename, content),
    "append": lambda filename, content: append_file(filename, content),
    "time_now" : time.time,
    "Win_MessageBoxA" : lambda Title, Content, Type : MessageBoxA(None, Title.encode('utf-8'), Content.encode('utf-8'), Type),
    "Input": lambda prompt: input(prompt),
    "sub_str": lambda string, start, length: string[start:start + length],
    "len" : lambda str : len(str),
    "sum": lambda list : sum(list),
    "type": lambda x : type(x),
    "min":lambda list : min(list),
    "split": lambda str , den: [i for i in str.split(den) if i!=''],
    "replace" : lambda s,r: s.replace("\n", ''),
    "max":lambda list : max(list),
    "exit": lambda int=10 : exit(int),
    "upper": lambda str : str.upper(),
    "lower": lambda str : str.lower(),
    "input": lambda prompt: input(prompt),
    "type": lambda t : type(t).__name__,
    "Int": lambda t : int(t),
    "Float": lambda t : float(t),
    "Str": lambda t : str(t),
    "List": lambda t : list(t),
    "Dict": lambda t : dict(t),
    "Set": lambda t : set(t),
    "Tuple": lambda t : tuple(t),
    "New_Env": lambda : {},
    "encode": lambda s: s.encode("utf-8")
}
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
            print(f"Content of {filename}:")
            print(content)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# Function to write to a file
def write_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
            return
            print(f"Successfully written to {filename}.")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")

def append_file(filename, content):
    try:
        with open(filename, 'a') as file:  # 'a' mode is for appending
            file.write(content)
            return
            print(f"Successfully appended to {filename}.")
    except Exception as e:
        print(f"Error appending to {filename}: {e}")

# Function to simulate the built-in function call
def parse_function_call(func_name, *args):
    if func_name.startswith('$'):
        # Extract the actual function name by removing the $
        func_name = func_name[1:]
        if func_name in builtins:
            builtins[func_name](*args)
        else:
            print(f"Error: {func_name} is not a valid built-in function.")
    else:
        print("Error: Not a valid function call.")

if  True:
    lexer = BasicLexer()
    parser = BasicParser()

    env = {}
    var_his={}
    temp_env = {}
    IS_Once=[]
    struct_env={}
    defered = {}
    watch = {}
    custom_operators = {}
    Func = {"math": 0}
    i=0
    while i<1:
        try:
            # Use the multiline input function
        #text = multiline_input('basic > ')
            # Reading file contents line-by-line
            with open(sys.argv[1], "r") as file:
                lines = file.readlines()  # Reads all lines as a list of strings
            code = "".join(lines)

            for l in code.split(";"):

                ll = lexer.tokenize(l)

                parser.t1234.append(l)

                tree = parser.parse(ll)

               	BasicExecute(tree, env, Func, temp_env,struct_env,builtins,defered,IS_Once,var_his,watch,custom_operators)

                i+=1
            #b=time.time()
            #print(b-a)
        except EOFError:
            exit()