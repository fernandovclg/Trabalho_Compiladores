from lexico.analisador import *
from sintatico.estados import *
from lexico.key_words_cpp import *
import csv

# Criação da tabela de ação e goto
TAB_ACTION_GOTO = list(csv.reader(open("./action_table.csv", "r"), delimiter="\t"))

# Definindo os tokens
TOKEN_TAB_ACTION = [ID, NUMERAL, PLUS, MINUS, TIMES, DIVIDE, SEMICOLON, COLON, COMMA, EQUAL, EQUAL_EQUAL, 
                    LEFT_PARENTHESIS, RIGHT_PARENTHESIS, LEFT_BRACES, RIGHT_BRACES, LEFT_BRACKET, 
                    RIGHT_BRACKET, LESS_THAN, GREATER_THAN, LESS_OR_EQUAL, GREATER_OR_EQUAL, NOT, 
                    NOT_EQUAL, AND, OR, DOT, TRUE, FALSE, CHARACTER, STRINGVAL, EOF, UNKNOWN, CHARACTER, STRINGVAL, TRUE, FALSE]


def tokenTAB(a):
    try:
        token_index = TOKEN_TAB_ACTION.index(a)
        print(f"Token encontrado: {a}, Índice: {token_index + 1}")
        return token_index + 1
    except ValueError:
        print(f"Token {a} não encontrado na tabela de tokens.")
        return -1

class Syntatical_Analysis:
    def __init__(self, lexical):
        self.lexical = lexical
        self.syntaticalError = False

    def parse(self):
        if self.lexical.erroLexico:
            return

        STACK = [0]
        readToken = self.lexical.proximo_Token()
        print(f"Token lido: {readToken}")  # Debugging
        print(f"Tamanho da tabela TAB_ACTION_GOTO: {len(TAB_ACTION_GOTO)}")
        print(f"Estado atual (STACK[-1]): {STACK[-1]}")
        print(f"Índice do token: {tokenTAB(readToken)}")
        print(f"Tamanho da linha da tabela: {len(TAB_ACTION_GOTO[STACK[-1] + 1])}")
        action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

        if action == -1:
            print(f"Erro de sintaxe na linha {self.lexical.linha}: Token inválido.")
            return

        while action != "acc":
            if self.lexical.erroLexico:
                break

            if action == "":
                print(f"Erro: Nenhuma ação definida para o estado {STACK[-1]} e o token {readToken} (índice do token: {tokenTAB(readToken)}).")
                print("Por favor, verifique o arquivo action_table.csv para entradas faltando ou incorretas.")
                break  # Exit the loop if there's no valid action
            print(f"Action: {action}") 
            if action[0] == "s":  # Shift
                state = int(action[1:])
                STACK.append(state)
                readToken = self.lexical.proximo_Token()
                action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

                if action == -1:
                    print(f"Erro de sintaxe na linha {self.lexical.linha}: Token inválido.")
                    break

            elif action[0] == "r":  # Reduce
                rule = int(action[1:])
                for _ in range(RIGHT[rule - 1]):
                    STACK.pop()
                try:
                    state = int(TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(LEFT[rule - 1])])
                except IndexError:
                    print(f"Erro de sintaxe na linha {self.lexical.linha}: Índice fora do intervalo.")
                    self.syntaticalError = True
                    break
                STACK.append(state)
                action = TAB_ACTION_GOTO[STACK[-1] + 1][tokenTAB(readToken)]

                if action == -1:
                    print(f"Erro de sintaxe na linha {self.lexical.linha}: Token inválido.")
                    break

            else:  # Error
                self.syntaticalError = True
                print(f"Erro de sintaxe na linha {self.lexical.linha}")
                break
