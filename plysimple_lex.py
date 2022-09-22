from lib2to3.pgen2 import literals
import re
import ply.lex as lex
import sys

states = [('REGEX','exclusive'),('GRAMMAR','exclusive'),('CODE','exclusive'),('YFUNC','exclusive'),('SYMBOLS','exclusive')]

literals = ['=',',']

tokens = ["LEX","LTS","IG","TKS","LFUNC",
"RT","ER","TVAL","TYPE","YACC","PRCD","LTRG",
"GRM","PREC","YFUNCS","DEF","PA","PF",
"PCA","PCF","PRA","PRF","DS",
"aspval","pelval","cod","id","nt","symbol","name","rgx","num"]

t_INITIAL_REGEX_GRAMMAR_YFUNC_SYMBOLS_ignore = " \t\n "
t_CODE_ignore = " "

def t_LEX(t):
    r'LEX:'
    return t

def t_LTS(t):
    r"literals"
    return t

def t_IG(t):
    r"ignore"
    return t

def t_TKS(t):
    r"tokens"
    return t

def t_LFUNC(t):
    r"lfunc:"
    t.lexer.push_state('REGEX')
    return t

def t_RT(t):
    r"return"
    return t

def t_ER(t):
    r"lerror\("
    t.lexer.push_state('CODE')
    return t

def t_TVAL(t):
    r"t.value"
    return t

def t_TYPE(t):
    r"(float)|(int)|(str)"
    return t

def t_YACC(t):
    r"YACC:"
    return t

def t_PRCD(t):
    r"precedend"
    return t

def t_LTRG(t):
    r"('left')|('right')"
    return t

def t_GRM(t):
    r"grammar:"
    t.lexer.push_state('GRAMMAR')
    return t

def t_SYMBOLS_PREC(t):
    r"%prec"
    return t

def t_GRAMMAR_YFUNCS(t):
    r"yfuncs:"
    t.lexer.pop_state()
    return t

def t_DEF(t):
    r"def"
    t.lexer.push_state('YFUNC')
    return t

def t_YFUNC_DEF(t):
    r"def"
    return t

def t_INITIAL_YFUNC_PA(t):
    r"\("
    return t

def t_CODE_PA(t):
    r"\("
    t.lexer.push_state('CODE')
    return t

def t_INITIAL_YFUNC_PF(t):
    r"\)"
    return t

def t_CODE_PF(t):
    r"\)"
    t.lexer.pop_state()
    return t

def t_PCA(t):
    r"{"
    return t

def t_REGEX_PCA(t):
    r"{"
    t.lexer.pop_state()
    return t

def t_SYMBOLS_PCA(t):
    r"{"
    t.lexer.pop_state()
    t.lexer.push_state('CODE')
    return t

def t_YFUNC_CODE_PCA(t):
    r"{"
    t.lexer.push_state('CODE')
    return t

def t_PCF(t):
    r"}"
    return t

def t_CODE_PCF(t):
    r"}"
    t.lexer.pop_state()
    return t

def t_PRA(t):
    r"\["
    return t

def t_CODE_PRA(t):
    r"\["
    t.lexer.push_state('CODE')
    return t

def t_PRF(t):
    r"\]"
    return t

def t_CODE_PRF(t):
    r"\]"
    t.lexer.pop_state()
    return t

def t_DS(t):
    r":"
    return t

def t_REGEX_DS(t):
    r":"
    t.lexer.pop_state()
    return t

def t_GRAMMAR_DS(t):
    r":"
    t.lexer.push_state("SYMBOLS")
    return t

def t_aspval(t):
    r'"((\\")|[^0-9\n"])+"'
    return t

def t_pelval(t):
    r"'((\\')|[^0-9\n'])+'"
    return t

def t_CODE_cod(t):
    r'((("[^"]+")|(\'[^\']+\'))|([^{}\(\)\[\]]))+'
    return t

def t_id(t):
    r"[A-Za-z]+"
    return t

def t_GRAMMAR_nt(t):
    r"[A-Za-z]+"
    return t

def t_SYMBOLS_symbol(t):
    r"([A-Za-z]+)|('.')|('\'')"
    return t

def t_YFUNC_name(t):
    r"[A-Za-z]\w*"
    return t

def t_REGEX_rgx(t):
    r"((\\:)|[^:])+" #TODO: ver isto melhor
    return t

def t_num(t):
    r"(\+|-)?\d+(\.\d+)?"
    return t

def t_ANY_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)


lexer = lex.lex()
"""
file = open("t.txt","r",encoding="utf-8",errors="surrogateescape")
lexer.input(file.read())
for token in lexer:
    print(token)
"""
