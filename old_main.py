
import io
from sly import Lexer, Parser
import os
import sys 	

import inspect


class BasicLexer(Lexer):
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

class BasicParser(Parser):
    tokens = BasicLexer.tokens


    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }
        self.modules = {}

    @_('IMPORT NAME')
    def statement(self, p):
        module_name = p.NAME
        if module_name in self.modules:
            print(f"Module '{module_name}' already imported.")
            return

        module_code=self.load_module(module_name)
        return ('import', module_name,module_code)
    def load_module(self, module_name):
        try:
            # Open the module file
            with open(f"{module_name}.txt", 'r') as file:
                lines = file.readlines()

            # Prepare a list of code lines
            module_code = [line.strip() for line in lines if line.strip()]

            # Initialize a new environment for this module
            module_env = {}



            # Store the module functions in the modules dictionary
            self.modules[module_name] = module_env
            return module_code
        except FileNotFoundError:
            print(f"Module '{module_name}' not found.")
        except Exception as e:
            print(f"Error loading module '{module_name}': {e}")
    @_('')
    def statement(self, p):
        pass


    @_('FOR var_assign TO expr THEN statement_list')
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

class BasicExecute:

    def __init__(self, tree, env,Func,temp_env):
        self.env = env
        self.Func =Func
        self.temp_env = temp_env
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




        if node[0] == 'num':
            return node[1]
        if node[0] == 'str':
            return node[1][1:-1]  # Strip quote
        if node[0]=='lst':
            return [self.walkTree(i) for i in node[1]]
        if node[0]=="dict":
            return {key : self.walkTree(val) for key, val in node[1].items()}

        if node[0]=="RET":
            return self.walkTree(node[1])
        if node[0]=="var_peq":
            print(node[2])
            self.env[node[1]]+=self.walkTree(node[2])
            return self.env[node[1]]
        if node[0]=="var_seq":
            self.env[node[1]] -= self.walkTree(node[2])
            return self.env[node[1]]
        if node[0]=="var_deq":
            self.env[node[1]] /= self.walkTree(node[2])
            return self.env[node[1]]
        if node[0]=="var_meq":
            self.env[node[1]] *= self.walkTree(node[2])
            return self.env[node[1]]

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

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                for i in node[2][1]:

                    if (i[0] == "RET"):
                        return self.walkTree(i)
                    self.walkTree(i)
                #return last stmt
                return self.walkTree(node[2][1][-1])
            for i in node[2][2]:
                if (i[0] == "RET"):
                    return self.walkTree(i)
                self.walkTree(i)
            return self.walkTree(node[2][2][-1])

        if node[0] == 'if_stmt_if':
            result = self.walkTree(node[1])
            if result:
                for i in node[2]:

                    if (i[0] == "RET"):

                        return self.walkTree(i)
                    self.walkTree(i)
                # return last stmt
                return self.walkTree(node[2][-1])
            for i in node[2]:
                if (i[0] == "RET"):
                    return self.walkTree(i)
                self.walkTree(i)
            return self.walkTree(node[2][-1])


        if node[0] == 'condition_eqeq':

            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':

            self.env[node[1]] = node[2]

        if node[0]=='fun_def_args':
            #a:0 etc
            self.temp_env[node[1]]={key : 0 for key in node[2]}

            self.env[node[1]]=node[3]
            return 0
        if node[0] == 'fun_call':
            for i in self.env[node[1]]:
                try:
                    if(i[0]=="RET"):
                        return self.walkTree(i)
                    self.walkTree(i)
                except LookupError:
                    print("Undefined function '%s'" % node[1])
                    return 0
            return self.walkTree(self.env[node[1]][-1])

        if node[0] == 'fun_call_args':
            #file management
            if node[1]=="open":
                file = (self.walkTree(node[2][0]))
                return open(f"{file}","r")

            for i,v in enumerate(self.temp_env[node[1]]):

                self.temp_env[node[1]][v]=self.walkTree(node[2][i])

            t=self.env
            self.env=self.temp_env[node[1]]


            for i in t[node[1]]:

                try:

                    if(i[0]=="RET"):
                        temp = self.walkTree(i)
                        break

                    temp=self.walkTree(i)
                except LookupError:
                    print("Undefined function '%s'" % node[1])
                    return 0

            self.env=t
            #ie the last statement
            return temp
           # print(self.env[node[1]][-1],"ok")

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            try:
                return self.walkTree(node[1]) - self.walkTree(node[2])
            except TypeError:
                if isinstance(self.walkTree(node[1]),list) and isinstance(self.walkTree(node[2]),int):
                    l = list(self.walkTree(node[1]))
                    l.pop(self.walkTree(node[2]))
                    return l
        elif node[0] == 'mul':
            if isinstance(self.walkTree(node[1]),str):
                return self.walkTree(node[1]) * self.walkTree(node[2])

        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            if isinstance(self.walkTree(node[2]),list):
                self.env[node[1]] = list(self.walkTree(node[2]))

                return node[2]
            if isinstance(self.walkTree(node[2]),dict):
                self.env[node[1]] = dict(self.walkTree(node[2]))
                return node[2]
            self.env[node[1]] = self.walkTree(node[2])
            if self.env[node[1]]==True or self.env[node[1]]==False:
                self.env[node[1]] = 1 if self.env[node[1]] == True else 0
            return node[1]

        if node[0] == 'var':
            #first try excepts is for list
            obj = self.env[self.walkTree(node[1])]
            if(isinstance(obj, io.TextIOWrapper)):
                return obj

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
                    for i in range(loop_count+1, loop_limit+1):
                        #res = self.walkTree(node[2])
                        for j in node[2]:
                            res=self.walkTree(j)
                            if res is not None:
                                print(res)
                        self.env[loop_setup[0]] = i
                    del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'print_stmt':
            #print(7)
            for i in node[1]:

                #had to add in because import name.nam() doesnt parse function statements correclty
                print(self.walkTree(self.walkTree(i)))
            #print(*[self.walkTree(arg) for arg in node[1]])

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
                    else:print(self.walkTree(i))


            #print(*[self.walkTree(arg) for arg in node[1]])


        if node[0]=="TK":
            import tkinter as tk
            root = tk.Tk()
            print(self.walkTree(node[1]))
            tk.Label(master=root, text=self.walkTree(node[1])).pack()
            root.mainloop()

def multiline_input(prompt="basic > "):
    print("Enter multiline code. Type 'END' on a new line to finish.")
    lines = []
    while True:
        line = input(prompt)
        if line.strip().lower() == 'end':  # Check for the END keyword to finish input
            break
        lines.append(line)
    return "\n".join(lines)  # Combine lines into a single string


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    temp_env = {}
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
            print("*")
            os.system("cls")

            for l in code.split(";"):

                tree = parser.parse(lexer.tokenize(l))

                BasicExecute(tree, env, Func, temp_env)

                i+=1
        except EOFError:
            exit()

# if __name__ == '__main__':
#     lexer = BasicLexer()
#     parser = BasicParser()
#     env = {}
#     temp_env={}
#     Func={"math":0}
#
#     while True:
#         try:
#             text = input('basic > ')
#
#         except EOFError:
#             break
#         if text:
#             tree = parser.parse(lexer.tokenize(text))
#             BasicExecute(tree, env, Func,temp_env)
