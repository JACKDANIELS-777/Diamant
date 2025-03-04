
import os
import io
from Lexer.Lexer import DiamantLexer
from Parser.Parser import DiamantParser
from ParseTree.ParseTree import DiamantExecute
import sys	
if __name__ == '__main__':
    lexer = DiamantLexer()
    parser = DiamantParser()
    env = {}
    temp_env = {}
    Func = {"math": 0,"wisk":0}
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

                DiamantExecute(tree, env, Func, temp_env)

                i+=1
        except EOFError:
            exit()
