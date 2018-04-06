# encoding: utf-8
import ply.lex as lex
import ply.yacc as yacc
import os
import codecs


# Token definition
'''
tokens = [
'STDIN','AND','PLUS_ONE', 'MINUS_ONE', 'STRING','ASSIGN','BACKSLASH','BETWEEN','COLON','DOLLAR','DOUBLEQUOTE',
'EOL','EQ','EXP' ,'FLOAT', 'CONST_ASSIGN','GREATER_OR_EQUAL','IDENTIFIER',
'INTEGER','LEFT_BRACE','LEFT_PAR' ,'LESS_OR_EQUAL','LESS_THAN','MINUS',
'MORE_THAN','MULTILINE_COMMENT' ,'NEQ','OR','PLUS','POINT','QUOTE',
'RIGHT_BRACE','RIGHT_PAR' ,'SEMICOLON','SINGLE_LINE_COMMENT',
'STAR'
]
'''
tokens = [
'STDIN','AND','PLUS_ONE', 'MINUS_ONE', 'STRING','ASSIGN','BETWEEN','DOLLAR',
'EQ','EXP' ,'FLOAT', 'CONST_ASSIGN','GREATER_OR_EQUAL','IDENTIFIER',
'INTEGER','LEFT_BRACE','LEFT_PAR' ,'LESS_OR_EQUAL','LESS_THAN','MINUS',
'MORE_THAN' ,'NEQ','OR','PLUS',
'RIGHT_BRACE','RIGHT_PAR',
'STAR'
]
errors_arr = []

# This hash is used to represent the reserved words,
# since the regex is just the word matching, the documentation said
# it was lest expensive to do it this way.
reserved = {
 'use': 'USE',
 'constant': 'CONSTANT',
 'else': 'ELSE',
 'if': 'IF',
 'print': 'PRINT',
 'while': 'WHILE',
 'true': 'TRUE',
 'false': 'FALSE'
}

tokens = tokens + list(reserved.values())

# definition of the regex to define every token in the token list
t_STDIN = r'<STDIN>'
t_STRING = r'\"(.)*\"'
t_AND = r'&&'
t_ASSIGN = r'='
t_CONST_ASSIGN = r'=>'
#t_BACKSLASH = r'\\'
t_BETWEEN = r'\/'
#t_COLON = r':'
t_DOLLAR = r'\$'
#t_DOUBLEQUOTE = r'\"'
#t_EOL = r'\n'
t_PLUS_ONE = r'\+\+'
t_MINUS_ONE = r'--'
t_EQ = r'=='
t_EXP = r'\*\*'
t_FLOAT = r'[+-]?[0-9]+\.[0-9]+'
t_GREATER_OR_EQUAL = r'>='
t_INTEGER = r'[0-9]+'
t_LEFT_BRACE = r'\{'
t_LEFT_PAR = r'\('
t_LESS_OR_EQUAL = r'<='
t_LESS_THAN = r'<'
t_MINUS = r'-'
t_MORE_THAN = r'>'
t_NEQ = r'!='
t_OR = r'\|\|'
t_PLUS = r'\+'
#t_POINT = r'\.'
#t_QUOTE = r'\''
t_RIGHT_BRACE = r'\}'
t_RIGHT_PAR = r'\)'
#t_SEMICOLON = r';'
t_STAR = r'\*'

# characters that are going to be ignored in all the program
# in this case tab and space
t_ignore  = ' \t\n'

#since almost every alphanumeric string can be an identifier,
# we need to make sure that it's not a reserved word
# If so, we need to return it with the correct data type
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

#The comment definition of both comment cases
# 'pass' is just for detecting, but dont returning anything

def t_ignore_SINGLE_LINE_COMMENT(t):
    r'\#.*'
    pass

def t_ignore_MULTILINE_COMMENT(t):
    r'\/\*([^*]|[\r\n])*\*\/+'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#last case, none of the token rules was achieved by a char
def t_error(t):
    s = "Symbol not found '%s'" % t.value[0]
    errors_arr.append(s)
    t.lexer.skip(1)



#now we have to define the function for reading the files
'''
def prepareArray(dir,arr):
    for i in range(len(arr)):
        arr[i] = dir+'/'+arr[i]

    return arr

def menuArray(arr):
    print("Choose test to run\n")
    for i in range(len(arr)):
        print(str(i) + ' ' + arr[i])
    answer = input("Escoge un archivo\n")
    return arr[answer]

#we define the path where we should look for the test
dir = 'tests'
arr = os.listdir(dir)
prepareArray(dir, arr)
a = menuArray(arr)
print ("you chose: " + a + "\n OUTPUT: \n")
file_test = codecs.open(a, 'r', 'utf-8')
str = file_test.read()
file_test.close()
lexer = lex.lex()
lexer.input(str)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
    '''
lexer = lex.lex()
