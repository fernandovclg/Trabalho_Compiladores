# Definindo Regras

# Definições de tipos
NO_KIND_DEF_ = -1
VAR_ = 0
PARAM_ = 1
FUNCTION_ = 2
ARRAY_TYPE_ = 3
STRUCT_TYPE_ = 4
ALIAS_TYPE_ = 5
SCALAR_TYPE_ = 6
UNIVERSAL_ = 7
FIELD_ = 8  # Adicionando FIELD_

# Definindo erros
ERR_REDCL = 9
ERR_NO_DECL = 10
ERR_TYPE_EXPECTED = 11
ERR_INVALID_TYPE = 12
ERR_PARAM_TYPE = 13
ERR_TOO_MANY_ARG = 14
ERR_TOO_FEW_ARGS = 15
ERR_BOOL_TYPE_EXPECTED = 16  # Adicionando ERR_BOOL_TYPE_EXPECTED
ERR_TYPE_MISMATCH = 17  # Adicionando ERR_TYPE_MISMATCH
ERR_FIELD_NOT_DECL = 18
ERR_KIND_NOT_ARRAY = 19
ERR_INVALID_INDEX_TYPE = 20

# Regras para a análise semântica
IDD_RULE = 0          # Identificador declarado
IDU_RULE = 1          # Identificador utilizado
ID_RULE = 2           # Adicionando ID_RULE
T_IDU_RULE = 3        # Tipo de identificador
T_INTEGER_RULE = 4    # Tipo inteiro
T_CHAR_RULE = 5       # Tipo caractere
T_BOOL_RULE = 6       # Tipo booleano
T_STRING_RULE = 7     # Tipo string
LI_IDD_RULE = 8       # Lista de identificadores
LI_COMMA_RULE = 9     # Lista de identificadores com vírgula
TRUE_RULE = 10        # Literal verdadeiro
FALSE_RULE = 11       # Literal falso
CHR_RULE = 12         # Literal de caractere
STR_RULE = 13         # Literal de string
NUM_RULE = 14         # Literal numérico
DC_LI_RULE = 15       # Declaração de campos em lista
NB_RULE = 16          # Novo bloco
DT_STRUCT_RULE = 17   # Declaração de struct
LP_IDD_RULE = 18      # Lista de parâmetros
NF_RULE = 19          # Novo função
MF_RULE = 20          # Função com tipo
DF_RULE = 21          # Fim de função
U_IF_RULE = 22        # Estrutura if
E_AND_RULE = 23       # Operador lógico AND
R_PLUS_RULE = 24      # Operador de adição
