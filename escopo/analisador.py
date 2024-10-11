from lexico.analisador import *
from escopo.rules import *
from escopo.classes import *
from escopo.types import *

# Global variables
global SymbolTable
SymbolTable = []
global SymbolTableLast
SymbolTableLast = []
global nCurrentLevel
nCurrentLevel = 0

global labelNo
labelNo = 0
global constPool
constPool = 0
global curFunction
curFunction = object()

# Function types
int_ = object(-1, None, SCALAR_TYPE_)
char_ = object(-1, None, SCALAR_TYPE_)
bool_ = object(-1, None, SCALAR_TYPE_)
string_ = object(-1, None, SCALAR_TYPE_)
universal_ = object(-1, None, SCALAR_TYPE_)

def newLabel():
    global labelNo
    labelNo += 1
    return labelNo - 1

def NewBlock():
    global nCurrentLevel
    global SymbolTable
    global SymbolTableLast
    nCurrentLevel += 1
    SymbolTable.append(None)
    SymbolTableLast.append(None)

def EndBlock():
    global nCurrentLevel
    nCurrentLevel -= 1

def Define(aName, pType):
    global SymbolTable
    global SymbolTableLast
    obj = object(aName, None, pType)
    
    # Ensure the symbol table is initialized
    if SymbolTable[nCurrentLevel] is None:
        SymbolTable[nCurrentLevel] = obj
        SymbolTableLast[nCurrentLevel] = obj
    else:
        aux = SymbolTable[nCurrentLevel]
        while True:
            if aux.pNext is None:
                aux.pNext = obj
                SymbolTableLast[nCurrentLevel] = obj
                break
            else:
                aux = aux.pNext

def Search(aName):
    global SymbolTable
    obj = SymbolTable[nCurrentLevel]
    while obj is not None:
        if obj.nName == aName:
            return obj
        obj = obj.pNext
    return None

def Find(aName):
    global SymbolTable
    for i in range(nCurrentLevel + 1):
        obj = SymbolTable[i]
        while obj is not None:
            if obj.nName == aName:
                return obj
            obj = obj.pNext
    return None

def Error(lexical, code):
    print("Line: " + str(lexical.line) + " - ")
    if code == ERR_NO_DECL:
        print("Variable not declared")
    elif code == ERR_REDCL:
        print("Variable already declared")
    elif code == ERR_TYPE_EXPECTED:
        print("Type not declared")
    elif code == ERR_INVALID_TYPE:
        print("Invalid Type for this operation")

def CheckTypes(t1, t2):
    if t1 == t2:
        return True
    # Add additional type checks as needed
    return False

def print_SymbolTable():
    global SymbolTable
    if len(SymbolTable) > 0:
        obj = SymbolTable[nCurrentLevel]
        print("Symbol Table:")
        while obj is not None:
            print(obj.nName)
            obj = obj.pNext
