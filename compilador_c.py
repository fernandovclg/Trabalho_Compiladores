import re

# Definindo palavras-chave, operadores e delimitadores em C
KEYWORDS = {"auto", "break", "case", "char", "const", "continue", "default", "do", "double",
            "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register",
            "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
            "union", "unsigned", "void", "volatile", "while"}

OPERATORS = {'+', '-', '*', '/', '=', '==', '<', '>', '<=', '>='}
DELIMITERS = {';', ',', '(', ')', '{', '}', '[', ']'}

# Função de análise léxica
def lexical_analyzer(code):
    tokens = []
    token_specification = [
        ('KEYWORD', r'\b(?:' + '|'.join(KEYWORDS) + r')\b'),  # Palavras-chave
        ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),                  # Identificadores
        ('NUMBER', r'\b\d+(\.\d+)?\b'),                       # Números
        ('OPERATOR', r'|'.join(re.escape(op) for op in OPERATORS)),  # Operadores
        ('DELIMITER', r'|'.join(re.escape(d) for d in DELIMITERS)),  # Delimitadores
        ('STRING', r'"(?:\\.|[^"\\])*"'),                     # Strings
        ('CHAR', r'\'(?:\\.|[^\'\\])\''),                     # Caracteres
        ('NEWLINE', r'\n'),                                   # Quebra de linha
        ('SKIP', r'[ \t]+'),                                  # Espaços e tabs
        ('MISMATCH', r'.')                                    # Qualquer outra coisa
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado na linha {line_num}')
        else:
            tokens.append((kind, value, line_num, column))
    return tokens

# Função de análise semântica
def semantic_analyzer(tokens):
    symbol_table = {}
    errors = []
    
    for token in tokens:
        kind, value, line_num, column = token
        
        if kind == "KEYWORD" and value in {"int", "float", "char"}:
            var_type = value
            continue_next = False
            for next_token in tokens[tokens.index(token)+1:]:
                if next_token[0] == "IDENTIFIER":
                    var_name = next_token[1]
                    if var_name in symbol_table:
                        errors.append(f"Erro semântico: Variável '{var_name}' já declarada na linha {line_num}.")
                    else:
                        symbol_table[var_name] = var_type
                    continue_next = True
                    break
                elif next_token[0] == "DELIMITER" and next_token[1] == ";":
                    break
            if not continue_next:
                errors.append(f"Erro semântico: Declaração incorreta na linha {line_num}.")
        
        elif kind == "IDENTIFIER":
            if value not in symbol_table:
                errors.append(f"Erro semântico: Variável '{value}' usada sem declaração na linha {line_num}.")
        
        elif kind == "OPERATOR" and value == "=":
            prev_token = tokens[tokens.index(token) - 1]
            next_token = tokens[tokens.index(token) + 1]
            if prev_token[0] == "IDENTIFIER" and next_token[0] in {"NUMBER", "IDENTIFIER"}:
                var_name = prev_token[1]
                assigned_value = next_token[1]
                if var_name in symbol_table:
                    var_type = symbol_table[var_name]
                    if var_type == "int" and "." in assigned_value:
                        errors.append(f"Erro semântico: Atribuição de ponto flutuante à variável inteira '{var_name}' na linha {line_num}.")
                else:
                    errors.append(f"Erro semântico: Variável '{var_name}' usada sem declaração na linha {line_num}.")

    if errors:
        return False, errors
    return True, symbol_table

# Função de geração de Assembly
def generate_assembly(tokens, symbol_table):
    assembly_code = []
    register_count = 0

    for token in tokens:
        kind, value = token[0], token[1]

        # Declaração de variável
        if kind == "KEYWORD" and value in {"int", "float", "char"}:
            continue  # Declaração já registrada no symbol_table

        # Atribuição
        elif kind == "OPERATOR" and value == "=":
            identifier = tokens[tokens.index(token) - 1][1]
            assigned_value = tokens[tokens.index(token) + 1][1]
            assembly_code.append(f"MOV R{register_count}, {assigned_value}")
            assembly_code.append(f"MOV {identifier}, R{register_count}")
            register_count += 1

        # Operações Aritméticas
        elif kind == "OPERATOR" and value in {"+", "-", "*", "/"}:
            operand1 = tokens[tokens.index(token) - 1][1]
            operand2 = tokens[tokens.index(token) + 1][1]
            if value == "+":
                assembly_code.append(f"ADD {operand1}, {operand2}")
            elif value == "-":
                assembly_code.append(f"SUB {operand1}, {operand2}")
            elif value == "*":
                assembly_code.append(f"MUL {operand1}, {operand2}")
            elif value == "/":
                assembly_code.append(f"DIV {operand1}, {operand2}")

        # Estruturas de Controle
        elif kind == "KEYWORD" and value == "if":
            assembly_code.append(f"; IF Statement")
            condition = tokens[tokens.index(token) + 2]
            assembly_code.append(f"CMP {condition[1]}, 0")  # Comparação básica
            assembly_code.append("JNE LABEL_IF")

    assembly_code.append("END")
    return "\n".join(assembly_code)

# Código de exemplo em C
code = '''
int main() {
    int x = 10;
    int y = 5;
    x = x + y;
    if (x > y) {
        x = x - y;
    }
    return 0;
}
'''

# Análise léxica e semântica do código
tokens = lexical_analyzer(code)
semantic_result, symbol_table_or_errors = semantic_analyzer(tokens)

if not semantic_result:
    print("Erros Semânticos Encontrados:")
    for error in symbol_table_or_errors:
        print("  -", error)
else:
    print("Código em Assembly Gerado:")
    assembly_code = generate_assembly(tokens, symbol_table_or_errors)
    print(assembly_code)