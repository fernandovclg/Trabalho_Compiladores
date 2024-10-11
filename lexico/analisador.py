from analisadorLexico.key_words_cpp import *
import string
import io

# Palavras-chave
palavras_chave = [
    "int", "float", "double", "char", "bool", "void", "class", "if", "else",
    "while", "for", "return", "true", "false", "struct", "break", "continue"
]


# Função para verificar se é um espaço
def eh_Espaco(c):
    return c in [chr(10), chr(13), "\f", "\v", "\t", " "]

class Analise_Lexica:
    def __init__(self, file):
        self.arquivo = file
        self.arquivo.seek(0)
        self.prox_Caractere = " "
        self.erroLexico = False
        self.v_Constantes = []
        self.identificadores = {}
        self.contador = 0
        self.token_Secundario = None
        self.linha = 1
        self.caractere = 1

    def adicionar_Constante(self, c):
        self.v_Constantes.append(c)
        return len(self.v_Constantes) - 1

    def obter_Constante(self, c):
        return self.v_Constantes[c]

    def buscar_Nome(self, nome):
        if nome not in self.identificadores:
            self.identificadores[nome] = self.contador
            self.contador += 1
        return self.identificadores[nome]

    def buscar_Palavra_Chave(self, nome):
        esquerda = 0
        direita = len(palavras_chave) - 1
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            if palavras_chave[meio] == nome:
                return meio
            elif palavras_chave[meio] > nome:
                direita = meio - 1
            else:
                esquerda = meio + 1
        return ID

    def erro_Lexico(self, token):
        if token == UNKNOWN:
            self.erroLexico = True
            print("Caractere "+str(self.caractere+1)+" não esperado na linha " + str(self.linha))

    def executar(self):
        self.prox_Caractere = self.arquivo.read(1)
        token_Auxiliar = self.proximo_Token()
        while token_Auxiliar != EOF:
            if token_Auxiliar == UNKNOWN:
                print("Caractere "+str(self.caractere+1)+" não esperado na linha " + str(self.linha))
                self.erroLexico = True
            token_Auxiliar = self.proximo_Token()
        if not self.erroLexico:
            print("Nenhum erro léxico.")

    def proximo_Token(self):
        separador = ""
        while eh_Espaco(self.prox_Caractere):
            if self.prox_Caractere in "\n\r":
                self.linha += 1
            self.prox_Caractere = self.arquivo.read(1)
            self.caractere += 1

        if self.prox_Caractere == "":
            return EOF

        if self.prox_Caractere.isdigit():
            return self.tratar_Numero(separador)

        if self.prox_Caractere.isalnum() or self.prox_Caractere == '_':
            return self.tratar_Identificador_Ou_Palavra(separador)

        return self.tratar_Simbolo()

    def tratar_Numero(self, separador):
        numero_Auxiliar = []
        while self.prox_Caractere.isdigit():
            numero_Auxiliar.append(self.prox_Caractere)
            self.prox_Caractere = self.arquivo.read(1)
            self.caractere += 1
        numero = separador.join(numero_Auxiliar)
        self.token_Secundario = self.adicionar_Constante(numero)
        return NUMERAL

    def tratar_Identificador_Ou_Palavra(self, separador):
        texto_Auxiliar = []
        while self.prox_Caractere.isalnum() or self.prox_Caractere == '_':
            texto_Auxiliar.append(self.prox_Caractere)
            self.prox_Caractere = self.arquivo.read(1)
            self.caractere += 1
        texto = separador.join(texto_Auxiliar)
        token = self.buscar_Palavra_Chave(texto)
        if token == ID:
            self.token_Secundario = self.buscar_Nome(texto)
        return token

    def tratar_Simbolo(self):
        simbolo = self.prox_Caractere
        self.prox_Caractere = self.arquivo.read(1)
        self.caractere += 1

        if simbolo == "+":
            return PLUS
        if simbolo == "-":
            return MINUS
        if simbolo == "*":
            return TIMES
        if simbolo == "/":
            return DIVIDE
        if simbolo == ";":
            return SEMICOLON
        if simbolo == ":":
            return COLON
        if simbolo == ",":
            return COMMA
        if simbolo == "=":
            if self.prox_Caractere == "=":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return EQUAL_EQUAL
            return EQUAL
        if simbolo == "(":
            return LEFT_PARENTHESIS
        if simbolo == ")":
            return RIGHT_PARENTHESIS
        if simbolo == "{":
            return LEFT_BRACES
        if simbolo == "}":
            return RIGHT_BRACES
        if simbolo == "[":
            return LEFT_BRACKET
        if simbolo == "]":
            return RIGHT_BRACKET
        if simbolo == "<":
            if self.prox_Caractere == "=":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return LESS_OR_EQUAL
            return LESS_THAN
        if simbolo == ">":
            if self.prox_Caractere == "=":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return GREATER_OR_EQUAL
            return GREATER_THAN
        if simbolo == "!":
            if self.prox_Caractere == "=":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return NOT_EQUAL
            return NOT
        if simbolo == "&":
            if self.prox_Caractere == "&":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return AND
            return UNKNOWN
        if simbolo == "|":
            if self.prox_Caractere == "||":
                self.prox_Caractere = self.arquivo.read(1)
                self.caractere += 1
                return OR
            return UNKNOWN
        if simbolo == ".":
            return DOT
        
        return UNKNOWN






codigo_teste = """
int main() {
    int a = 10;
    float b = 20.5;
    if (a < b) {
        return a + b;
    } else {
        return 0;
    }
}
"""

# Cria um arquivo temporário em memória com o código de teste
arquivo_teste = io.StringIO(codigo_teste)

# Cria uma instância da classe Analise_Lexica
analisador = Analise_Lexica(arquivo_teste)

# Executa o analisador léxico
analisador.executar()

# Fecha o arquivo temporário
arquivo_teste.close()