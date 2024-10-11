from lexico.analisador import Analise_Lexica
from sintatico.analisador import Syntatical_Analysis
from semantico.analisador import Semantic_Analysis

# Abre o arquivo de código-fonte para análise
file = open('codigo-teste-2.ssl', 'r', encoding='utf-8')

# Cria a instância do analisador léxico
lexical = Analise_Lexica(file)

# Executa a análise léxica
lexical.executar()

# Reinicializa o analisador léxico para a análise sintática
file.seek(0)  # Reseta o ponteiro do arquivo para o início
lexical = Analise_Lexica(file)

# Cria a instância do analisador sintático e executa a análise
syntatical = Syntatical_Analysis(lexical)
syntatical.parse()

# Fecha o arquivo de código-fonte
file.close()
