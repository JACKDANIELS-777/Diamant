from Lexer import  DiamantLexer

#This is to test if the lexer is working correctly

lexer = DiamantLexer()
test_String = """
a=10
funk a()->7
as 
if
"""

tokens = lexer.tokenize(test_String)
for token in tokens:
	print(f"Value: {token.value} and Type:{token.type}")