# Definindo Classes

class Var:
    def __init__(self, pType=None):
        self.pType = pType
        self.pNext = None

class Param:
    def __init__(self, pType=None, nIndex=None, nSize=None):
        self.pType = pType
        self.nIndex = nIndex
        self.nSize = nSize

class Field:
    def __init__(self, pType=None, nIndex=None, nSize=None):
        self.pType = pType
        self.nIndex = nIndex
        self.nSize = nSize

class Struct:
    def __init__(self, pFields=None, nSize=None):
        self.pFields = pFields
        self.nSize = nSize

class Function:
    def __init__(self, pRetType=None, pParams=None, nIndex=None, nParams=None, nVars=None):
        self.pRetType = pRetType
        self.pParams = pParams
        self.nIndex = nIndex
        self.nParams = nParams
        self.nVars = nVars

class object:
    def __init__(self, nName=None, pNext=None, eKind=None, _=None):
        self.nName = nName
        self.pNext = pNext
        self.eKind = eKind
        self._ = _

# Definições de tipos auxiliares usados na análise semântica
class ID:
    def __init__(self, obj=None, name=None):
        self.object = obj
        self.name = name

class IDD:
    def __init__(self, obj=None, name=None):
        self.object = obj
        self.name = name

class IDU:
    def __init__(self, obj=None, name=None):
        self.object = obj
        self.name = name

class T:
    def __init__(self, tipo=None):
        self.type = tipo

class E:
    def __init__(self, tipo=None):
        self.type = tipo

# Classe t_attrib
class t_attrib:
    def __init__(self, t_nont=None, nSize=None, _=None):
        self.t_nont = t_nont  # Não terminal
        self.nSize = nSize     # Tamanho
        self._ = _             # Pode armazenar outros dados, como objetos, tipos, etc.

# Definições adicionais, como LV, MC, etc., podem ser adicionadas conforme necessário
