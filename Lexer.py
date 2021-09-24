from os import error
from typing import List
import re
import ast

class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value


    def __str__(self) -> str:
        return self.type, self.value

# class Add(Token):
#     def __str__(self) -> str:
#         return "Add"

# class Increment(Token):
#     def __str__(self) -> str:
#         return "increment"

# class Min(Token):
#     def __str__(self) -> str:
#         return "Minus"

# class Decrement(Token):
#     def __str__(self) -> str:
#         return "Decrement"

# class OpenBrac(Token):
#     def __str__(self) -> str:
#         return "Open haakje"

# class CloseBrac(Token):
#     def __str__(self) -> str:
#         return "Dicht haakje"

# class OpenCurly(Token):
#      def __str__(self) -> str:
#         return "open curly haakje"

# class CloseCurly(Token):
#      def __str__(self) -> str:
#         return "dicht curly haakje"

# class Semi(Token):
#     def __str__(self) -> str:
#         return "Semicolon"

# class Equal(Token):
#     def __str__(self) -> str:
#         return "equal"
# class IntId(Token):
#     def __str__(self) -> str:
#         return "int identifier"

CHAR, INTEGER, PLUS, MINUS, EQUAL, MUL, DIV, STARTBRACKED, ENDBRACKED, OPENCURLY, CLOSECURLY, EOF, EOL, NOTFOUND = (
    'CHAR','INTEGER', 'PLUS', 'MINUS', 'EQUAL', 'MUL', 'DIV', '(', ')','{', '}', 'EOF', 'EOL', 'NOT FOUND'
)

def lexerReverse(code, tokenList : List[Token] = []):
    c , *rest = code
    print(rest)
    if rest == []:
        print("return list")
        return tokenList
    if c == '':
      return lexerReverse(rest, tokenList)  
   
    if c == '-':
        tokenList.append(Token(PLUS, '+'))
        return lexerReverse(rest, tokenList)

    if c == '+':
        tokenList.append(Token(MINUS, '-'))
        return lexerReverse(rest, tokenList)

    if c == ';':

        tokenList.append(Token(EOL, ';'))
        return lexerReverse(rest, tokenList)
    
    if c == ')':

        tokenList.append(Token(STARTBRACKED, '('))
        return lexerReverse(rest, tokenList)

    if c == '(':

        tokenList.append(Token(ENDBRACKED, ')'))
        return lexerReverse(rest, tokenList)

    if c == '}':

        tokenList.append(Token(OPENCURLY, '{'))
        return lexerReverse(rest, tokenList)

    if c == '{':

        tokenList.append(Token(CLOSECURLY, '}'))
        return lexerReverse(rest, tokenList)

    if c == '=':
        tokenList.append(Token(EQUAL, '='))
        return lexerReverse(rest, tokenList)
    if c == 'tni':
        tokenList.append(Token(INTEGER, 'NONE'))
        return lexerReverse(rest, tokenList)

    if c.isdigit():
        tokenList.append(Token(INTEGER, int(c)))
        return lexerReverse(rest, tokenList)
    
    if isinstance(c, str):
        tokenList.append(Token(CHAR, c))
        return lexerReverse(rest, tokenList)
   
    tokenList.append(Token(NOTFOUND, ''))
    return lexerReverse(rest, tokenList)




file = open('test.esrever', 'r')
code = file.readlines()

for lines in code:
    code = re.split('\n| |;', lines)
    print(code)
    x = lexerReverse(code)
    print(x)
    print("OUT")
