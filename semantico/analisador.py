from sintatico.estados import *
from escopo.analisador import *
from escopo.rules import *
from escopo.classes import *
from escopo.types import *

name = ""
n = ""
rLabel = ""

hasErr = False
StackSem = []

def IS_TYPE_KIND(eKind):
    return eKind in {ARRAY_TYPE_, STRUCT_TYPE_, ALIAS_TYPE_, SCALAR_TYPE_, UNIVERSAL_}


def Semantic_Analysis(lexical, rule):
    generated_code = open("codigo_Gerado.txt", "a+")

    global name, n, rLabel
    global IDD_, IDU_, ID_, T_, LI_, LI0_, LI1_, TRU_, FALS_, STR_, CHR_, NUM_, DC_, DC0_, DC1_, LP_, LP0_, LP1_, E_, E0_, E1_, L_, L0_, L1_, R_, R0_, R1_, Y_, Y0_, Y1_, F_, F0_, F1_, LV_, LV0_, LV1_, MC_, LE_, LE0_, LE1_, MT_, ME_, MW_
    global nFuncs
    global curFunction
    global constPool
    global SymbolTable
    p = None

    if rule == IDD_RULE:
        name = lexical.secondary_Token
        p = Find(name)
        if p is not None:
            Error(lexical, ERR_REDCL)
        else:
            p = Define(name)
        p.eKind = NO_KIND_DEF_
        IDD_.t_nont = IDD
        IDD_._ = ID(p, name)
        StackSem.append(IDD_)

    elif rule == IDU_RULE:
        name = lexical.secondary_Token
        p = Find(name)
        if p is None:
            Error(lexical, ERR_NO_DECL)
            p = Define(name)
        IDU_.t_nont = IDU
        IDU_._ = ID(p, name)
        StackSem.append(IDU_)

    elif rule == ID_RULE:
        name = lexical.secondary_Token
        ID_.t_nont = ID
        ID_._ = ID(None, name)
        StackSem.append(ID_)

    elif rule == T_IDU_RULE:
        IDU_ = StackSem.pop()
        p = IDU_._.object
        if IS_TYPE_KIND(p.eKind) or p.eKind == UNIVERSAL_:
            T_ = t_attrib(T, p._.nSize, T(p))
        else:
            T_ = t_attrib(T, 0, T(universal_))
            Error(lexical, ERR_TYPE_EXPECTED)
        StackSem.append(T_)

    elif rule == T_INTEGER_RULE:
        T_ = t_attrib(T, 1, T(int_))
        StackSem.append(T_)

    elif rule == T_CHAR_RULE:
        T_ = t_attrib(T, 1, T(char_))
        StackSem.append(T_)

    elif rule == T_BOOL_RULE:
        T_ = t_attrib(T, 1, T(bool_))
        StackSem.append(T_)

    elif rule == LI_IDD_RULE:
        IDD_ = StackSem.pop()
        LI_ = t_attrib(LI, None, LI(IDD_._.object))
        StackSem.append(LI_)

    elif rule == LI_COMMA_RULE:
        IDD_ = StackSem.pop()
        LI1_ = StackSem.pop()
        LI0_ = t_attrib(LI, None, LI(LI1_._.list))
        StackSem.append(LI0_)

    elif rule == TRUE_RULE:
        TRU_ = t_attrib(TRUE, None, TRUE(bool_, True))
        StackSem.append(TRU_)

    elif rule == FALSE_RULE:
        FALS_ = t_attrib(FALSE, None, FALSE(bool_, False))
        StackSem.append(FALS_)

    elif rule == CHR_RULE:
        CHR_ = t_attrib(CHR, None, CHR(char_, lexical.get_Cte(lexical.secondary_Token)))
        StackSem.append(CHR_)

    elif rule == STR_RULE:
        STR_ = t_attrib(STR, None, STR(string_, lexical.get_Cte(lexical.secondary_Token), lexical.secondary_Token))
        StackSem.append(STR_)

    elif rule == NUM_RULE:
        NUM_ = t_attrib(NUM, None, NUM(int_, lexical.get_Cte(lexical.secondary_Token), lexical.secondary_Token))
        StackSem.append(NUM_)

    elif rule == DC_LI_RULE:
        T_ = StackSem.pop()
        LI_ = StackSem.pop()
        p = LI_._.list
        t = T_._.type
        n = 0
        while p is not None and p.eKind == NO_KIND_DEF_:
            p.eKind = FIELD_
            p._ = Field(t, n, T_.nSize)
            n = n + T_.nSize
            p = p.pNext
        DC_ = t_attrib(DC, n, DC(LI_._.list))
        StackSem.append(DC_)

    elif rule == NB_RULE:
        NewBlock()

    elif rule == DT_STRUCT_RULE:
        DC_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        p.eKind = STRUCT_TYPE_
        p._ = Struct(DC_._.list, DC_.nSize)
        EndBlock()

    elif rule == LP_IDD_RULE:
        T_ = StackSem.pop()
        IDD_ = StackSem.pop()
        p = IDD_._.object
        p.eKind = PARAM_
        p._ = Param(t, 0, T_.nSize)
        LP_ = t_attrib(LP, T_.nSize, LP(p))
        StackSem.append(LP_)

    elif rule == NF_RULE:
        IDD_ = StackSem[-1]
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(None, None, nFuncs, 0, 0)
        nFuncs += 1
        NewBlock()

    elif rule == MF_RULE:
        T_ = StackSem.pop()
        LP_ = StackSem.pop()
        IDD_ = StackSem.pop()
        f = IDD_._.object
        f.eKind = FUNCTION_
        f._ = Function(T_._.type, LP_._.list, f._.nIndex, LP_.nSize, LP_.nSize)
        curFunction = f
        generated_code.write("BEGIN_FUNC " + str(f._.nIndex) + " " + str(f._.nParams) + "\n")

    elif rule == DF_RULE:
        EndBlock()
        generated_code.write("END_FUNC" + "\n")

    elif rule == U_IF_RULE:
        MT_ = StackSem.pop()
        E_ = StackSem.pop()
        t = E_._.type
        if not CheckTypes(t, bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
            generated_code.write("L" + str(MT_._.label) + "\n")

    elif rule == E_AND_RULE:
        L_ = StackSem.pop()
        E1_ = StackSem.pop()
        if not CheckTypes(E1_._.type, bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        if not CheckTypes(L_._.type, bool_):
            Error(lexical, ERR_BOOL_TYPE_EXPECTED)
        E0_ = t_attrib(E, None, E(bool_))
        StackSem.append(E0_)
        generated_code.write("\tAND" + "\n")

    elif rule == R_PLUS_RULE:
        Y_ = StackSem.pop()
        R1_ = StackSem.pop()
        if not CheckTypes(R1_._.type, Y_._.type):
            Error(lexical, ERR_TYPE_MISMATCH)
        if not CheckTypes(R1_._.type, int_) and not CheckTypes(R1_._.type, string_):
            Error(lexical, ERR_INVALID_TYPE)
        R0_ = t_attrib(R, None, R(R1_._.type))
        StackSem.append(R0_)
        generated_code.write("\tADD" + "\n")

    generated_code.close()
