from typing import List
import re

class Token:
    def __str__(self) -> str:
        return "undefined"

class Add(Token):
    def __str__(self) -> str:
        return "Add"

class Increment(Token):
    def __str__(self) -> str:
        return "increment"

class Min(Token):
    def __str__(self) -> str:
        return "Minus"

class Decrement(Token):
    def __str__(self) -> str:
        return "Decrement"

class OpenBrac(Token):
    def __str__(self) -> str:
        return "Open haakje"

class CloseBrac(Token):
    def __str__(self) -> str:
        return "Dicht haakje"

class OpenCurly(Token):
     def __str__(self) -> str:
        return "open curly haakje"

class CloseCurly(Token):
     def __str__(self) -> str:
        return "dicht curly haakje"

class Semi(Token):
    def __str__(self) -> str:
        return "Semicolon"

class Equal(Token):
    def __str__(self) -> str:
        return "equal"



def lexerReverse(code, tokenList : List[Token] = []):
    c , *rest = code
    if rest == []:
        return tokenList
   
    if c == '-':
        tokenList.append(Add())
        return lexerReverse(rest, tokenList)

    if c == '+':
        tokenList.append(Min())
        return lexerReverse(rest, tokenList)

    if c == ';':

        tokenList.append(Semi())
        return lexerReverse(rest, tokenList)
    
    if c == '++':

        tokenList.append(Decrement())
        return lexerReverse(rest, tokenList)
    
    if c == '--':

        tokenList.append(Increment())
        return lexerReverse(rest, tokenList)

    if c == ')':

        tokenList.append(OpenBrac())
        return lexerReverse(rest, tokenList)

    if c == '(':

        tokenList.append(CloseBrac())
        return lexerReverse(rest, tokenList)

    if c == '}':

        tokenList.append(OpenCurly())
        return lexerReverse(rest, tokenList)

    if c == '{':

        tokenList.append(CloseCurly())
        return lexerReverse(rest, tokenList)

    if c == '=':
        tokenList.append(Equal())
        return lexerReverse(rest, tokenList)


    else:
        return lexerReverse(rest,tokenList)


with open('test.esrever', 'r') as file:
    code = file.read()
code = re.split('\n| |;', code)
print(code)


print(lexerReverse(code))
