from typing import List, Tuple
import sys
sys.setrecursionlimit(200000)

class Token:
    def __init__(self):
        self.x = 1

    # __repr__ :: Token -> String
    def __repr__(self):
        return "Undefined"


class Add(Token):
    def increment(self):
        self.x += 1
        return self

    # __repr__ :: Add -> String
    def __repr__(self):
        return "Add " + str(self.x)


class IncPtr(Token):
    def increment(self):
        self.x += 1
        return self

    # __repr__ :: IncPtr -> String
    def __repr__(self):
        return "IncrementPtr " + str(self.x)


class Min(Token):
    def increment(self):
        self.x += 1
        return self

    # __repr__ :: Min -> String
    def __repr__(self):
        return "Min " + str(self.x)


class DecPtr(Token):
    def increment(self):
        self.x += 1
        return self

    # __repr__ :: DecPtr -> String
    def __repr__(self):
        return "DecrementPtr " + str(self.x)


class LoopOpen(Token):
    # __repr__ :: LoopOpen -> String
    def __repr__(self):
        return "Open"


class LoopClose(Token):
    # __repr__ :: LoopClose -> String
    def __repr__(self):
        return "Close"


class Input(Token):
    # __repr__ :: Input -> String
    def __repr__(self):
        return "InputChar"


class Output(Token):
    #__repr__ :: Output -> String
    def __repr__(self):
        return "OutputChar"

#charlist :: [Char]
charlist = ['+', '-', '>', '<', '[', ']', '.', ',']

#multilist :: [Char]
multilist = charlist[:4]

#tokendict :: Dict((String,Token))
tokendict = dict()
tokendict['+'] = ("Add", lambda: Add())
tokendict['-'] = ("Min", lambda: Min())
tokendict['>'] = ("IncrementPtr", lambda: IncPtr())
tokendict['<'] = ("DecrementPtr", lambda: DecPtr())
tokendict['['] = ("Open", lambda: LoopOpen())
tokendict[']'] = ("Close", lambda: LoopClose())
tokendict[','] = ("InputChar", lambda: Input())
tokendict['.'] = ("OutputChar", lambda: Output())


class SimpleStatement:
    def __init__(self, num=1):
        self.number = num

class CodeBlock:
    def __init__(self, nest=0):
        self.statements = []
        self.nestlevel = nest

    #addStatement :: CodeBlock -> SimpleStatement -> CodeBlock
    def addStatement(self, statement : SimpleStatement):
        self.statements.append(statement)
        return self

    def __str__(self):
        return self.__repr__()

    #__repr__ :: CodeBlock -> String
    def __repr__(self) -> str:
        nstr = repeatStr("   ", self.nestlevel)
        statestr = ''.join(map(lambda st: nstr + str(st) + "\n", self.statements))
        return "Begin Block: \n" + statestr + repeatStr("   ", self.nestlevel - 1) + "End Block"


#repeatStr :: String -> Integer -> String
def repeatStr(s : str, i : int):
    if (i <= 0):
        return ""
    return s + repeatStr(s, i - 1)


class Increment(SimpleStatement):
    def __init__(self, n):
        self.number = n

    # __repr__ :: Increment -> String
    def __repr__(self) -> str:
        return "Increment " + str(self.number)


class Decrement(SimpleStatement):
    def __init__(self, n):
        self.number = n

    # __repr__ :: Decrement -> String
    def __repr__(self) -> str:
        return "Decrement " + str(self.number)


class IncrementPointer(SimpleStatement):
    def __init__(self, n):
        self.number = n

    # __repr__ :: IncrementPointer -> String
    def __repr__(self) -> str:
        return "Increment Pointer " + str(self.number)


class DecrementPointer(SimpleStatement):
    def __init__(self, n):
        self.number = n

    # __repr__ :: DecrementPointer -> String
    def __repr__(self) -> str:
        return "Decrement Pointer " + str(self.number)


class InputCharacter(SimpleStatement):
    def __init__(self):
        self.number = 1

    # __repr__ :: InputCharacter -> String
    def __repr__(self) -> str:
        return "Input Character"


class OutputCharacter(SimpleStatement):
    def __init__(self) -> str:
        self.number = 1

    # __repr__ :: OutputCharacter -> String
    def __repr__(self) -> str:
        return "Output Character"


class Loop(SimpleStatement):
    def __init__(self, block):
        self.code = block

    #__repr__ :: Loop -> String
    def __repr__(self) -> str:
        s = self.code.__repr__()
        return s


# lexBrainfuck :: String -> [Token] -> [Token]
def lexBrainfuck(prog: str, lexed: List[Token]) -> List[Token]:
    if not prog:
        return lexed
    c, *progrest = prog
    if c in charlist:
        if len(lexed) == 0:
            lexed.append(tokendict[c][1]())
        else:
            if c in multilist and str(lexed[-1]).startswith(tokendict[c][0]):
                lexed[-1] = lexed[-1].increment()
            else:
                lexed.append(tokendict[c][1]())
    return lexBrainfuck(progrest, lexed)

# parseCodeBlock :: [Token] -> CodeBlock -> ([Token], CodeBlock)
def parseCodeBlock(tokens: List[Token], code: CodeBlock) -> Tuple[List[Token], CodeBlock]:
    if len(tokens) == 0:
        return None, code
    token, *rest = tokens
    if isinstance(token, LoopClose):
        return rest, code
    elif isinstance(token, Add):
        return parseCodeBlock(rest, code.addStatement(Increment(token.x)))
    elif isinstance(token, Min):
        return parseCodeBlock(rest, code.addStatement(Decrement(token.x)))
    elif isinstance(token, IncPtr):
        return parseCodeBlock(rest, code.addStatement(IncrementPointer(token.x)))
    elif isinstance(token, DecPtr):
        return parseCodeBlock(rest, code.addStatement(DecrementPointer(token.x)))
    elif isinstance(token, Input):
        return parseCodeBlock(rest, code.addStatement(InputCharacter()))
    elif isinstance(token, Output):
        return parseCodeBlock(rest, code.addStatement(OutputCharacter()))
    elif isinstance(token, LoopOpen):
        newrest, block = parseCodeBlock(rest, CodeBlock(nest=code.nestlevel + 1))
        return parseCodeBlock(newrest, code.addStatement(Loop(block)))
    else:
        return None, code


class ProgramState:
    def __init__(self):
        self.pointer = 0
        self.memory = [0]*10

    #__repr__ :: ProgramState -> String
    def __repr__(self) -> str:
        return "ptr: " + str(self.pointer) + " val: " + str(self.memory)

#runBlock :: CodeBlock -> Integer -> ProgramState -> String -> (ProgramState, String)
def runBlock(code : CodeBlock, codePtr : int, state : ProgramState, output : str) -> Tuple[ProgramState, str]:
    #print(state)
    if(codePtr >= len(code.statements)):
        return state, output
    statement = code.statements[codePtr]
    #print(str(statement))
    if isinstance(statement, Increment):
        state.memory[state.pointer]+=statement.number
        if state.memory[state.pointer] > 128:
            state.memory[state.pointer] -= 256
        return runBlock(code,codePtr+1,state,output)
    elif isinstance(statement, Decrement):
        state.memory[state.pointer]-= statement.number
        if state.memory[state.pointer] < -127:
            state.memory[state.pointer] += 256
        return runBlock(code,codePtr+1,state,output)
    elif isinstance(statement, IncrementPointer):
        state.pointer += statement.number
        return runBlock(code, codePtr + 1, state, output)
    elif isinstance(statement, DecrementPointer):
        state.pointer -= statement.number
        return runBlock(code, codePtr + 1, state, output)
    elif isinstance(statement, InputCharacter):
        x = input() #Ja, nee dit is niet netjes functioneel meer; maar het is de runner, dus dat mag
        if(len(x)>0):
            c = bytes(x, 'ascii')[0]
            state.memory[state.pointer] = c
        else:
            state.memory[state.pointer] = 0
        return runBlock(code, codePtr + 1, state, output)
    elif isinstance(statement, OutputCharacter):
        return runBlock(code, codePtr + 1, state, output+str(state.memory[state.pointer])+",")
    elif isinstance(statement, Loop):
        state_, output_ = runloop(statement, state, output)
        return runBlock(code, codePtr + 1, state_, output_)

#runloop :: Loop -> ProgramState -> String -> (ProgramState, String)
def runloop(loop : Loop, state: ProgramState, output : str) -> Tuple[ProgramState, str]:
    #print("loop")
    if(state.memory[state.pointer]==0):
        return state,output
    else:
        state_, output_ = runBlock(loop.code,0,state,output)
        return runloop(loop, state_, output_)

prog = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
prog2 = "+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+."
prog3 = "++++++++[>>+<<-]>>."
lexed = lexBrainfuck(prog3, [])
lexed2 = lexBrainfuck(prog2, [])
print(lexed)
print("==============================================")
empty, parsed = parseCodeBlock(lexed, CodeBlock(nest=0))
empty, parsed2 = parseCodeBlock(lexed2, CodeBlock(nest=0))
print(parsed)
print("==============================================")
output = runBlock(parsed, 0, ProgramState(), "")[1]
output2 = runBlock(parsed2, 0, ProgramState(), "")[1]
print(output)
print(output2)