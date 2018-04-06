import ply.yacc as yacc
import os
import codecs
import re
from perl_lexer import tokens
from perl_lexer import errors_arr

precedence = (
('right', 'ASSIGN'),
('right', 'EQ'),
('left', 'NEQ'),
('left', 'LESS_THAN', 'LESS_OR_EQUAL', 'GREATER_OR_EQUAL', 'MORE_THAN'),
('left', 'PLUS', 'MINUS'),
('left', 'BETWEEN', 'STAR')
)

parse_err = []

class Node:
    def __init__(self,name,value='None',children=None):
        self.value = value
        self.name = name
        self.leaf = False
        if children:
            self.children = children
        else:
            self.children = []
        if not self.children:
            leaf = True

    def get_values(self):
        if (self.value is not None):
            return '"' + self.name + ' value: ' + self.value +'"'
        else:
         return '"' + self.name + '"'

    def traverse(self):
        if self.children:
            for child in self.children:
                    print(self.name, 'father of', child.get_values())
                    child.traverse()


def p_program(p):
    'program : declarationList'
    p[0] = Node('program', None, [p[1]])
    #print(p[0].traverse())

def p_declarationList(p):
    'declarationList :  declaration declarationList'
    #print("declaration list 1")
    p[0] = Node('rec declarationList', None, [p[1], p[2]])

def p_declarationList2(p):
    'declarationList : declaration'
    #print("declaration list 2")
    p[0] = Node('declarationList', None, [p[1]])

def p_declaration(p):
    'declaration : varDeclaration'
    #print("dec")
    p[0] = Node('varDeclaration', None, [p[1]])

def p_declaration2(p):
    'declaration : statement'
    #print("dec2")
    p[0] = Node('declaration statement', None, [p[1]])

def p_declaration3(p):
    'declaration : constDeclaration'
    #print("dec3")
    p[0] = Node('const declaration', None, [p[1]])

def p_declaration4(p):
    'declaration : funcDeclaration'
    #print("dec4")
    p[0] = Node('function declaration', None, [p[1]])

def p_variable(p):
    'variable : DOLLAR IDENTIFIER'
    #print("var")
    dollar = Node('$', p[1])
    id = Node('ID', p[1])
    p[0] = Node('variable', None, [dollar, id])

def p_varDeclaration(p):
    'varDeclaration : variable ASSIGN variableType'
    #print("vardec")
    assign = Node('=', p[2])
    p[0] = Node('variable declaration', None, [p[1], assign, p[3]])

def p_varDeclaration2(p):
    'varDeclaration : variable ASSIGN STDIN'
    #print("vardec2")
    assign = Node('=', p[2])
    stdin = Node('stdin', p[3])
    p[0] = Node('variable to stdin', None, [p[1], assign, stdin])

def p_number(p):
    'number : INTEGER'
    #print("num")
    p[0] = Node('number int',p[1])

def p_number2(p):
    'number : FLOAT'
    p[0] = Node('number float',p[1])

def p_variableType(p):
    'variableType : number'
    #print("type number")
    p[0] = Node('numerical variable', None, [p[1]])

def p_variableType2(p):
    'variableType : STRING'
    #print("type string")
    string = Node('str', p[1])
    p[0] = Node('string variable', None, [string])

def p_variableType3(p):
    'variableType : TRUE'
    #print("type true")
    t = Node('true', p[1])
    p[0] = Node('true variable', None, [t])

def p_variableType4(p):
    'variableType : FALSE'
    #print("type false")
    f = Node('false', p[1])
    p[0] = Node('false variable', None, [f])

def p_constDeclaration(p):
    'constDeclaration : USE CONSTANT IDENTIFIER CONST_ASSIGN variableType'
    use = Node('use', p[1])
    c = Node('const', p[2])
    id = Node('id', p[3])
    ca = Node('const assign', p[4])
    p[0] = Node('constant declaration', None, [use, c, id, ca ,p[5]])
    #print("constant")

def p_funcDeclaration(p):
    'funcDeclaration : PRINT LEFT_PAR factor RIGHT_PAR'
    #print("print factor")
    pr = Node('print', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    p[0] = Node('print variable vt', None, [pr, lp, p[3] ,rp, ])


def p_funcDeclaration2(p):
    'funcDeclaration : PRINT LEFT_PAR sumLessExpression RIGHT_PAR'
    #print("print expr")
    pr = Node('print', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    p[0] = Node('print sum less', None, [pr, lp, p[3], rp])


def p_sumLessExpression(p):
    'sumLessExpression : variable PLUS_ONE'
    #print("++")
    p_one = Node('++', p[2])
    p[0] = Node('plus one', None, [p[1], p_one ])

def p_sumLessExpression1(p):
    'sumLessExpression : variable MINUS_ONE'
    #print("--")
    p_one = Node('--', p[2])
    p[0] = Node('minus one', None, [p[1], p_one ])

def p_statement(p):
    'statement : expression'
    #print("print statement")
    p[0] = Node('statement - expression', None, [p[1]])

def p_statement2(p):
    'statement : conditionalStmt'
    #print("print conditionalStmt")
    p[0] = Node('statement - conditional', None, [p[1]])

def p_statement3(p):
    'statement : loopStmt'
    #print("print loopStmt")
    p[0] = Node('loop statement', None, [p[1]])

def p_conditionalStmt(p):
    'conditionalStmt : matchedif'
    #print("if-m")
    p[0] = Node('conditional mif', None, [p[1]])

def p_conditionalStmt2(p):
    'conditionalStmt : unmatchedif'
    #print("if-u")
    p[0] = Node('conditional uif', None, [p[1]])

def p_matchedif(p):
    'matchedif : IF LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE ELSE LEFT_BRACE declarationList RIGHT_BRACE'
    #print("matched-if")
    i = Node('if', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace', p[7])
    el = Node('else', p[8])
    lb2 = Node('left brace2', p[9])
    rb2 = Node('right brace2', p[11])

    p[0] = Node('matched if', None, [i, lp, p[3], rp,lb, p[6], rb, el, lb2, p[10],rb2])

def p_unmatchedif(p):
    'unmatchedif : IF LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE'
    #print("unmatched-if")
    i = Node('if',p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace', p[7])
    p[0] = Node('unmatched if', None, [i, lp, p[3], rp,lb, p[6], rb])

def p_loopStmt(p):
    'loopStmt : WHILE LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE'
    #print("while")
    wh = Node('if',p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace',p[7])
    p[0] = Node('while', None, [wh, lp, p[3], rp,lb, p[6], rb])

'''def p_expression(p):
    'expression : variable EQ expression'
    #print("assignation")
    wh = Node('eq', p[2])
    p[0] = Node('expression equal', None, [p[1], eq , p[3]])'''

def p_expression2(p):
    'expression : logicalExp'
    #print("logicalExp")
    p[0] = Node('expression logical', None, [p[1]])

def p_expression3(p):
    'expression : sumLessExpression'
    #print("exp to sumless")
    p[0] = Node('expression sumless ++ -- ', None, [p[1]])

'''
def p_logicalExp(p):
    'logicalExp : TRUE'
    #print("log true")

def p_logicalExp2(p):
    'logicalExp : FALSE'
    #print("log false")
'''
def p_logicalExp3(p):
    'logicalExp : TRUE OR andExp'
    #print("true OR")
    t = Node('true',p[1])
    o = Node('or',p[2])
    p[0] = Node('logical exp true', None, [t,o, p[3]])

def p_logicalExp4(p):
    'logicalExp : FALSE OR andExp'
    #print("false OR")
    f = Node('false',p[1])
    o = Node('or', p[2])
    p[0] = Node('logical exp false', None, [f,o, p[3]])

def p_logicalExp5(p):
    'logicalExp : andExp'
    #print("logical to and")
    p[0] = Node('logical exp and', None, [p[1]])

#keep 1-2 or 3-4
#def p_andExp1(p):
#    'andExp : TRUE'
#    #print("and true")

#def p_andExp2(p):
#    'andExp : FALSE'
#    #print("and false")

def p_andExp3(p):
    'andExp : TRUE AND compExp'
    #print("and true")
    t = Node('true', p[1])
    a = Node('and',  p[2])
    p[0] = Node('and exp true', None, [t,a, p[3]])

def p_andExp4(p):
    'andExp : FALSE AND compExp'
    #print("and false")
    f = Node('false',  p[1])
    a = Node('and',  p[2])
    p[0] = Node('and exp false', None, [f,a, p[3]])

def p_andExp5(p):
    'andExp : compExp'
    #print("and to comp")
    p[0] = Node('and exp comparison', None, [p[1]])

def p_compExp(p):
    'compExp : sumExp compSign sumExp'
    #print("comparison")
    p[0] = Node('compexp', None, [p[1], p[2], p[3]])

def p_compExp2(p):
    'compExp : sumExp'
    #print("assignation")
    p[0] = Node('compExp to sumExp', None, [p[1]])

def p_compSign(p):
    'compSign : LESS_OR_EQUAL'
    #print("<=")
    p[0] = Node('<=',  p[1])
    #p[0] = Node('LESS EQUAL', None, [le])

def p_compSign2(p):
    'compSign : LESS_THAN'
    #print("<")
    p[0] = Node('<',  p[1])
    #p[0] = Node('LESS_THAN', None, [lt])

def p_compSign3(p):
    'compSign : MORE_THAN'
    #print(">")
    p[0] = Node('>',  p[1])
    #p[0] = Node('MORE THAN', None, [mt])

def p_compSign4(p):
    'compSign : GREATER_OR_EQUAL'
    #print(">=")
    p[0] = Node(' >=', p[1])
    #p[0] = Node('GREATER_OR_EQUAL', None, [ge])

def p_compSign5(p):
    'compSign : EQ'
    #print("==")
    p[0] = Node('== ', p[1])
    #p[0] = Node('EQ', None, [eq])

def p_compSign6(p):
    'compSign : NEQ'
    #print("!=")
    p[0] = Node('!= ', p[1])
    #p[0] = Node('NEQ', None, [neq])

def p_sumExp(p):
    'sumExp : term sumSign sumExp'
    #print("sum exp")
    p[0] = Node('sumExp', None, [p[1], p[2], p[3]])

def p_sumExp2(p):
    'sumExp : term'
    #print("term")
    p[0] = Node('sumExp term', None, [p[1]])

def p_sumSign(p):
    'sumSign : MINUS'
    #print("-")
    p[0] = Node('-',  p[1])
    #p[0] = Node('MINUS', None, [min])

def p_sumSign2(p):
    'sumSign : PLUS'
    #print("+")
    p[0] = Node('+',  p[1])
    #p[0] = Node('PLUS', None, [plus])

def p_term(p):
    'term : multiNegExp multiSign term'
    #print("term")
    p[0] = Node('term to multiNegExp', None, [p[1], p[2], p[3]])

def p_term2(p):
    'term : multiNegExp'
    #print("multineg")
    p[0] = Node('term - multiNegExp', None, [p[1]])

def p_multiSign(p):
    'multiSign : EXP'
    #print("exp")
    p[0] = Node('** ', p[1])
    #p[0] = Node('EXP', None, [exp])

def p_multiSign2(p):
    'multiSign : STAR'
    #print("star")
    p[0] = Node('*', p[1])
    #p[0] = Node('star', None, [star])

def p_multiSign3(p):
    'multiSign : BETWEEN'
    #print("between")
    p[0] = Node('/',  p[1])
    #p[0] = Node('between', None, [bt])

def p_multiNegExp(p):
    'multiNegExp : unaryOp multiNegExp'
    #print("unary")
    p[0] = Node('multineg - unary', None, [p[1], p[2]])

def p_multiNegExp2(p):
    'multiNegExp : factor'
    #print("factor")
    p[0] = Node('multineg - factor', None, [p[1]])

def p_unaryOp(p):
    'unaryOp : MINUS'
    #print("-")
    p[0] = Node('-', p[1])
    #p[0] = Node('unary MINUS', None, [min])

def p_unaryOp2(p):
    'unaryOp : PLUS'
    #print("+")
    p[0] = Node('+', p[1])
    #p[0] = Node('unary plus', None, [min])

def p_factor(p):
    'factor : variable'
    #print("variable")
    p[0] = Node('factor - variable', None, [p[1]])

def p_factor2(p):
    'factor : variableType'
    #print("VTYPE")
    p[0] = Node('factor - variableType', None, [p[1]])

def p_factor3(p):
    'factor : IDENTIFIER'
    #print("ID")
    p[0] = Node('ID', p[1])
    #p[0] = Node('factor - ID', None, [id])


def p_factor4(p):
    'factor : LEFT_PAR expression RIGHT_PAR'
    #print("expression")
    lp = Node('left par', p[1])
    rp = Node('right par', p[3])
    p[0] = Node('factor - exp', None, [lp, p[2], rp])

def p_error(p):
    if p:
        s= "Syntax error at '%s'" % p.value
        parse_err.append(s)
    else:
        s= "Syntax error at EOF"
        parse_err.append(s)


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

def lexer_errors(arr):
    for i in range(len(arr)):
        print("lexer error " + arr[i])

def parsing_errors(arr):
    for i in range(len(arr)):
        print(arr[i])

#we define the path where we should look for the test
dir = 'tests'
arr = os.listdir(dir)
prepareArray(dir, arr)
a = menuArray(arr)
print ("you chose: " + a + "\n OUTPUT: \n")
file_test = codecs.open(a, 'r', 'utf-8')
str = file_test.read()
file_test.close()
parser = yacc.yacc(start="program", method="SLR")
result = parser.parse(str)
if (not errors_arr):
    pass
    if (not parse_err):
        print(result.traverse())
    else:
        if(len(parse_err) == 1 and "Syntax error at EOF" in parse_err):
            pass
        else:
            parsing_errors(parse_err)
else:
    lexer_errors(errors_arr)
