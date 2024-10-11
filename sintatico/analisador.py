from lexico.analisador import *
from estados import *
import csv

# Criação da tabela de ação e goto
TAB_ACTION_GOTO = list(csv.reader(open("action_table.csv", "r"), delimiter="\t"))

# Definindo os tokens
TOKEN_TAB_ACTION = [NUMERAL, PLUS, MINUS, TIMES, DIVIDE, SEMICOLON, COLON, COMMA, EQUAL, EQUAL_EQUAL, 
                    LEFT_PARENTHESIS, RIGHT_PARENTHESIS, LEFT_BRACES, RIGHT_BRACES, LEFT_BRACKET, 
                    RIGHT_BRACKET, LESS_THAN, GREATER_THAN, LESS_OR_EQUAL, GREATER_OR_EQUAL, NOT, 
                    NOT_EQUAL, AND, OR, DOT, ID, TRUE, FALSE, CHARACTER, STRINGVAL, EOF]

def tokenTAB(a):
    return TOKEN_TAB_ACTION.index(a) + 1

class Syntatical_Analysis:
    def __init__(self, lexical):
        self.lexical = lexical
        self.syntaticalError = False

    def parse(self):
        if self.lexical.erroLexico:
            return

        STACK = [0]
        readToken = self.lexical.proximo_Token()
        action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

        while action != "acc":
            if self.lexical.erroLexico:
                break

            if action[0] == "s":  # Shift
                state = int(action[1:])
                STACK.append(state)
                readToken = self.lexical.proximo_Token()
                action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

            elif action[0] == "r":  # Reduce
                rule = int(action[1:])
                for _ in range(RIGHT[rule - 1]):
                    STACK.pop()
                try:
                    state = int(TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(LEFT[rule - 1])])
                except IndexError:
                    print(f"Erro de sintaxe na linha {self.lexical.linha}")
                    self.syntaticalError = True
                    break
                STACK.append(state)
                action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

            else:  # Error
                self.syntaticalError = True
                print(f"Erro de sintaxe na linha {self.lexical.linha}")
                break
