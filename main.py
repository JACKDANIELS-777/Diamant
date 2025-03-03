
import os

from Lexer.Lexer import DiamantLexer
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
            with open("r.txt", "r") as file:
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
