import re
import ply.yacc as yacc 
from plysimple_lex import tokens, literals 

def p_Ply(p):
    "Ply : Lexer Yc"
    p[0] = "import ply.lex as lex\n" + p[1] + "\n\nlexer = lex.lex()\n\nimport ply.yacc as yacc\n\n" + p[2] + "\n\nparser = yacc.yacc()"

def p_Lexer(p):
    "Lexer : LEX Literals Ignore Tokens Lfuncs Lerror"
    p[0] = p[2] + "\n" + p[3] +"\n" + p[4] + "\n" + p[5] + "\n" + p[6]

def p_Yc(p):
    "Yc : YACC Precedents Declarations Grammar Yfs"
    p[0] = p[2] + "\n\n" + p[3] + "\n" + p[4] + "\n" + p[5]

def p_Grammar(p):
    "Grammar : GRM Productions"
    p[0] = p[2]

def p_Yfs(p):
    "Yfs : YFUNCS Funcs"
    p[0] = p[2]

def p_Literals(p):
    "Literals : LTS '=' aspval"
    p[3] = p[3][1:-1] #remove as aspas
    lits = [char for char in p[3]] #transforma a string numa lista de chars
    for lit in lits:
        parser.tt[lit] = False #add literal, value False (not used)
    p[0] = "literals = " + str(lits)

def p_Literals_empty(p):
    "Literals : "
    p[0] = ""

def p_Ignore(p):
    "Ignore : IG '=' aspval"
    p[0] = "t_ignore = " + p[3]

def p_Ignore_empty(p):
    "Ignore : "
    p[0] = ""

def p_Tokens(p):
    "Tokens : TKS '=' PRA Tokl PRF"
    p[0] = "tokens = " + str(p[4])

def p_Tokl(p):
    "Tokl : Tokl ',' pelval"
    p[0] = p[1] + [p[3][1:-1]]

    parser.tt[p[3][1:-1]] = False #adiciona token com valor a False(n usado)

def p_Tokl_single(p):
    "Tokl : pelval"
    p[0] = [p[1][1:-1]]
    parser.tt[p[1][1:-1]] = False #adiciona token com valor a False(n usado)

def p_Lfuncs(p):
    "Lfuncs : Lfuncs Lfunc"
    p[0] = p[1] + "\n" + p[2]

def p_Lfuncs_empty(p):
    "Lfuncs : "
    p[0] = ""

def p_Lfunc(p):
    "Lfunc : LFUNC rgx DS RT PA pelval ',' Tv PF "
    p[2] = re.sub(r'(\\:)',r':',p[2])
    p[0] = "def t_" + p[6][1:-1] + "(t):\n\tr'" + p[2] + "'\n" + p[8]

def p_Tv(p):
    "Tv : TVAL"
    p[0] = "\treturn t"

def p_Tv_type(p):
    "Tv : TYPE PA TVAL PF"
    p[0] = "\tt.value = " + p[1] + "(t.value)\n\treturn t"

def p_Lerror(p):
    "Lerror : ER Codes PF" #o lexer n está a apanhar tudo para o ER,rever
    p[0] = "def t_error(t):\n\tprint(" + p[2] + ")"

def p_Lerror_empty(p):
    "Lerror : "
    p[0] = 'def t_ANY_error(t):\n\tprint(f"Illegal character \'{t.value[0]}\', [{t.lexer.lineno}]")\n\tt.lexer.skip(1)'

def p_Precedents(p):
    "Precedents : PRCD '=' PRA Prcdlist PRF"
    p[0] = "precedent = [" + p[4] + "]"

def p_Precedents_empty(p):
    "Precedents : "
    p[0] = ""

def p_Declarations(p):
    "Declarations : Declarations Declaration"
    p[0] = p[1] + p[2] + "\n"

def p_Declarations_empty(p):
    "Declarations : "
    p[0] = ""

def p_Declaration(p): #TODO: ver o que fazer com isto
    "Declaration : id '=' Values"
    p[0] = p[1] + "=" + p[3]

def p_Productions(p):
    "Productions : Productions Production"
    p[0] = p[1] + p[2] + "\n\n"

def p_Productions_empty(p):
    "Productions : "
    p[0] = ""

def p_Production(p):
    "Production : nt DS Symbols PCA Codes PCF"
    if p[1] in parser.tntDef:
        p[0] = "def p_" + p[1] + "_" + str(parser.tntDef[p[1]]) + "(p):\n\t" + '"' + p[1] + " : " + p[3] + '"\n\t' + p[5]
        parser.tntDef[p[1]] += 1
    else:
        p[0] = "def p_" + p[1] + "(p):\n\t" + '"' + p[1] + " : " + p[3] + '"\n\t' + p[5]
        parser.tntDef[p[1]] = 1

def p_Symbols(p):
    "Symbols : Symbols S"
    p[0] = p[1] + p[2] + " "

def p_Symbols_empty(p):
    "Symbols : "
    p[0] = ""

def p_S(p):
    "S : symbol"
    p[0] = p[1]

    if p[1] in parser.tt:
        parser.tt[p[1]] = True #token used
    elif p[1][1:-1] in parser.tt:
        parser.tt[p[1][1:-1]] = True #literal used
    else:
        parser.tntUsed[p[1]] = 0 #non terminal symbol used

def p_S_Prec(p):
    "S : PREC symbol"
    p[0] = "%prec " + p[2]

def p_Prcdlist(p):
    "Prcdlist : Prcdlist PA LTRG ',' Pelvals pelval PF ','"
    p[0] = p[1] + "(" + p[3] + "," + p[5] + p[6] + "),"

def p_Prcdlist_empty(p):
    "Prcdlist : "
    p[0] = ""

def p_Pelvals(p):
    "Pelvals : Pelvals pelval ','"
    p[0] = p[1] + p[2] + ','

def p_Pelvals_empty(p):
    "Pelvals : "
    p[0] = ""

def p_Funcs(p):
    "Funcs : Funcs Func"
    p[0] = p[1] + p[2] + "\n"

def p_Funcs_empty(p):
    "Funcs : "
    p[0] = ""

def p_Func(p):
    "Func : DEF name PA name PF PCA Codes PCF"
    p[0] = "def " + p[2] + "(" + p[4] + "):" + p[7]

def p_Codes(p):
    "Codes : Codes Code"
    p[0] = p[1] + p[2]

def p_Codes_empty(p):
    "Codes : "
    p[0] = ""

def p_Code(p):
    "Code : cod"
    p[0] = p[1]

def p_Code_p(p):
    "Code : PA Codes PF"
    p[0] = "(" + p[2] + ")"

def p_Code_pr(p):
    "Code : PRA Codes PRF"
    p[0] = "[" + p[2] + "]"

def p_Code_pc(p):
    "Code : PCA Codes PCF"
    p[0] = "{" + p[2] + "}"

def p_Values(p):
    "Values : Values ',' Type"
    p[0] = p[1] + "," + p[3]

def p_Values_type(p):
    "Values : Value"
    p[0] = p[1]

def p_Value_num(p):
    "Value : num"
    p[0] = p[1]

def p_Value_aspval(p):
    "Value : aspval"
    p[0] = p[1]

def p_Value_pelval(p):
    "Value : pelval"
    p[0] = p[1]

def p_Value_lists(p):
    "Value : PRA Cont PRF"
    p[0] = "[" + p[2] + "]"

def p_Value_tuples(p):
    "Value : PA Cont PF"
    p[0] = "(" + p[2] + ")"

def p_Value_dict(p):
    "Value : PCA Cont PCF"
    p[0] = "{" + p[2] + "}"

def p_Cont(p):
    "Cont : Values"
    p[0] = p[1]

def p_Cont_empty(p):
    "Cont : "
    p[0] = ""

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

"""Variaveis de estado"""

#Terminal symbols table
parser.tt = {}
#Defined Non-terminal symbols table (left side of the production)
parser.tntDef = {}
#Used Non-terminal symbols table (right side of the production)
parser.tntUsed = {}

import sys
parser.success = True

#arguments
#python3 plysimple_sin.py [plysimple.txt] [plyfile.py]
if len(sys.argv)<3:
    print("Not enough arguments...")

elif len(sys.argv)>3:
    print("Too many arguments")
else:
    simpleFile = open(sys.argv[1],"r",encoding="utf-8",errors="surrogateescape")



    warnings = 0 
    errors = 0
    program = simpleFile.read()
    codigo = parser.parse(program)
    if parser.success:

        #verify unused tokens/literals
        for key in parser.tt:
            if not parser.tt[key]:
                print("WARNING! :: Terminal symbol",key,"defined but not used.")
                warnings +=1
            
        #verify used but not defined 
        for key in parser.tntUsed:
            if key not in parser.tntDef:
                print("ERROR! :: Non-terminal",key,"symbol used but not defined.")
                errors+=1

        if errors > 0:
            print("Couldn't generate PLY :: Total",warnings,"warnings and",errors,"errors")
        else:
            print("PLY generated successfully :: Total",warnings,"warnings and",errors,"errors")
            result_final = open(sys.argv[2],"w+",encoding="utf-8",errors="surrogateescape")
            result_final.write(codigo)
            result_final.close()
    else:
        print("Programa com erros... Corrija e tente novamente!")
