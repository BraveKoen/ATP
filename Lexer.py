from os import error
from typing import List
import re
import ast

class Token:
    def __init__(self, type, value, line) -> None:

        self.type = type
        self.value = value
        self.lineNumber = line
    

    def __str__(self) -> str:
        return f"{self.value} at Line {self.lineNumber}, Type {self.type}."
    def printType(self):
        x = f"{self.value} at Line {self.lineNumber}, Type {self.type}."
        print(x)




CHAR, INTEGER, PLUS, MINUS, EQUAL, MUL, DIV, STARTBRACKED, ENDBRACKED, OPENCURLY, CLOSECURLY, EOF, EOL, NOTFOUND = (
    'CHAR','INTEGER', 'PLUS', 'MINUS', 'EQUAL', 'MUL', 'DIV', '(', ')','{', '}', 'EOF', 'EOL', 'NOT FOUND'
)

def lexerReverse(code, tokenList : List[Token] = [], charNum = 0, lineNumber = 0, charValue = "", intValue = ""):
    print(len(code))
    print(code)
    if len(code) == charNum:
        if len(charValue)> 0:
            if charValue == "tni":
                tokenList.append(Token(INTEGER, charValue, lineNumber))
                return tokenList
            else:
                tokenList.append(Token(CHAR, charValue, lineNumber))
                return tokenList
        if len(intValue) > 0:
            tokenList.append(Token(INTEGER, int(intValue), lineNumber))
            return tokenList
        else:
            return tokenList


        return tokenList
    
    if code[charNum] == ' ':
        if len(intValue) > 0:
            tokenList.append(Token(INTEGER, int(intValue), lineNumber))
        if len(charValue) > 0:
            if charValue == "tni":
                tokenList.append(Token(INTEGER, charValue, lineNumber))
            else:
                tokenList.append(Token(CHAR, charValue, lineNumber))
            return lexerReverse(code, tokenList, charNum+1, lineNumber)
        else:
            return lexerReverse(code, tokenList, charNum+1, lineNumber)
    
    if code[charNum] == ';':
        tokenList.append(Token(EOL, None, lineNumber))
        return lexerReverse(code, tokenList, charNum+1 , lineNumber)

    if code[charNum] >= '0' and code[charNum] <= '9':
        if(len(intValue)> 0):
            return lexerReverse(code, tokenList, charNum+1, lineNumber, "" , intValue+ str(code[charNum]))

        return lexerReverse(code, tokenList, charNum+1, lineNumber, "" , str(code[charNum]))
    if code[charNum] == "+":
        tokenList.append(Token(MINUS, '-', lineNumber))
        return lexerReverse(code, tokenList, charNum+1, lineNumber)
    if code[charNum] == "-":
        tokenList.append(Token(PLUS, '+', lineNumber))
        return lexerReverse(code, tokenList, charNum+1, lineNumber)
    if code[charNum] == "=":
        tokenList.append(Token(EQUAL, '=', lineNumber))
        return lexerReverse(code, tokenList, charNum+1, lineNumber)
    if code[charNum].isalpha():
        return lexerReverse(code, tokenList, charNum+1, lineNumber, charValue + str(code[charNum]))


    
    
        




file = open('test.esrever', 'r')
code = file.readlines()
lineNum = 0
for lines in code:
    lineNum+=1
    x = lexerReverse(lines, [], 0, lineNum)
    for i in x:
        i.printType()



