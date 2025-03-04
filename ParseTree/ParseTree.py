import io

from Lexer.Lexer import DiamantLexer
from Parser.Parser import DiamantParser

class DiamantExecute:

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
                                    lexer=DiamantLexer()
                                    parser = DiamantParser()
                                    #print(fstr)
                                    t = parser.parse(lexer.tokenize(fstr))
                                    #print(t,1000)
                                    #print(f"t is {self.walkTree(t)}")
                                    
                                    #s = s.replace('{' + fstr + '}', str(BasicExecute(t, self.env, Func, self.temp_env)))
                                    s=s.replace('{' + fstr + '}',str(self.walkTree(t)))
                                    
                                except:
                                    pass
                                try:
                                    
                                    
                                    
                                    s=s.replace('{'+fstr+'}',str(self.env[fstr]))
                                    

                                except:
                                    pass
                                bnum=0
                                fstr=''
                            elif bnum==1:
                                fstr+=j
                            else:
                                pass
                        print(s)
                    else:
                        print(7)
                        print(self.walkTree(i))


            #print(*[self.walkTree(arg) for arg in node[1]])


        if node[0]=="TK":
            import tkinter as tk
            root = tk.Tk()
            print(self.walkTree(node[1]))
            tk.Label(master=root, text=self.walkTree(node[1])).pack()
            root.mainloop()



