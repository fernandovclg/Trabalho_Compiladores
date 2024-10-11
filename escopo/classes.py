class Var:
    def __init__(self, pType=None):
        self.pType = pType
        self.pNext = None

class Function:
    def __init__(self, pRetType=None, pParams=None):
        self.pRetType = pRetType
        self.pParams = pParams
        self.pNext = None

class object:
    def __init__(self, nName=None, pNext=None, eKind=None):
        self.nName = nName
        self.pNext = pNext
        self.eKind = eKind

# Classe t_attrib
class t_attrib:
    def __init__(self, t_nont=None, nSize=None, _=None):
        self.t_nont = t_nont
        self.nSize = nSize
        self._ = _
