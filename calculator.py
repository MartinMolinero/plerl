import ply.lex as lex
import ply.yacc as yacc

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

tokens = (
'AND','ASSIGN','BACKSLASH','BETWEEN','COLON','DOLLAR','DOUBLEQUOTE',
'EOL','EQ','EXP' ,'FLOAT','GREATER_OR_EQUAL','IDENTIFIER',
'INTEGER','LEFT_BRACE','LEFT_PAR' ,'LESS_OR_EQUAL','LESS_THAN','MINUS',
'MORE_THAN','MULTILINE_COMMENT' ,'NEQ','OR','PLUS','POINT','QUOTE'
'RIGHT_BRACE','RIGHT_PAR' ,'SEMICOLON','SINGLE_LINE_COMMENT',
'STAR','STRING'
)

reserved = {
 'else': 'ELSE',
 'if': 'IF',
 'print': 'PRINT',
 'while': 'WHILE',
 'STDIN': 'STDIN'
}
# Tokens
t_AND = r'&&'
t_ASSIGN = r'='
t_BACKSLASH = r'\\'
t_BETWEEN = r'\/'
t_COLON = r':'
t_DOLLAR = r'\$'
t_DOUBLEQUOTE = r'\"'
t_EOL = r'\n'
t_EQ = r'=='
t_EXP = r'\*\*'
t_FLOAT = r'([0-9])+\.([0.9])+'
t_GREATER_OR_EQUAL = r'>='
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]'
t_INTEGER = r'[0-9]+'
t_LEFT_BRACE = r'\{'
t_LEFT_PAR = r'\('
t_LESS_OR_EQUAL = r'<='
t_LESS_THAN = r'<'
t_MINUS = r'-'
t_MORE_THAN = r'>'
t_MULTILINE_COMMENT = r'(\/\*)(\n)*(.*)+(\n)*(\*\/)'
t_NEQ = r'!='
t_OR = r'\|\|'
t_PLUS = r'\+'
t_POINT = r'\.'
t_QUOTE = r'\''
t_RIGHT_BRACE = r'\}'
t_RIGHT_PAR = r'\)'
t_SEMICOLON = r';'
t_SINGLE_LINE_COMMENT = r'#(.*)\n'
t_STAR = r'\*'
t_STRING = r'\“ (.*)+ \“'
t_ignore  = r' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
