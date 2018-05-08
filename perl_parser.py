import ply.yacc as yacc
import os
import codecs
import re
from perl_lexer import tokens
from perl_lexer import errors_arr

'''precedence = (
('right', 'ASSIGN'),
('right', 'EQ'),
('left', 'NEQ'),
('left', 'LESS_THAN', 'LESS_OR_EQUAL', 'GREATER_OR_EQUAL', 'MORE_THAN'),
('left', 'PLUS', 'MINUS'),
('left', 'BETWEEN', 'STAR')
)'''

parse_err = []
semantic_err = []


class Stack:
    def __init__(self, list):
        self.list = list

    def push(self, tup):
        self.list.append(tup)

    def pop(self):
        self.list.pop()

    def delete(self, name):
        self.list.remove(name)

    def find(self, name):
        for item in self.list:
            if item.variable == name:
                return item
        return -1


class Tup:
    def __init__(self, variable='', value='None', type='None'):
        self.variable = variable
        self.value = value
        self.type = type

    def to_string(self):
        return str('name: ' + self.variable + ' value: ' + repr(self.value) + ' type: '+ self.type)

class Node:
    def __init__(self,name,value='None',type='None', children=None):
        self.value = value
        self.name = name
        self.leaf = False
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        if not self.children:
            leaf = True

    def get_values(self):
        if (self.value is not None):
            return '"' + self.name + ' value: ' + repr(self.value) + ' type: ' + self.type + '"'
        else:
         return '"' + self.name + '"'

    def traverse(self):
        if self.children:
            for child in self.children:
                    print(self.name, 'father of', child.get_values())
                    child.traverse()


def p_program(p):
    'program : declarationList'
    p[0] = Node('program', None, None,  [p[1]])


def p_declarationList(p):
    'declarationList :  declaration declarationList'

    p[0] = Node('rec declarationList', None, None, [p[1], p[2]])

def p_declarationList2(p):
    'declarationList : declaration'

    p[0] = Node('declarationList', None, None, [p[1]])

def p_declaration(p):
    'declaration : varDeclaration'

    p[0] = Node('varDeclaration', None, None, [p[1]])

def p_declaration2(p):
    'declaration : statement'

    p[0] = Node('declaration statement', None, None, [p[1]])

def p_declaration3(p):
    'declaration : constDeclaration'

    p[0] = Node('const declaration', None,  None, [p[1]])

def p_declaration4(p):
    'declaration : funcDeclaration'

    p[0] = Node('function declaration', None, None, [p[1]])

def p_variable(p):
    'variable : DOLLAR IDENTIFIER'

    dollar = Node('$', p[1])
    id = Node('ID', p[2])
    p[0] = Node('variable', None, None, [dollar, id])


def p_varDeclaration(p):
    'varDeclaration : variable ASSIGN logicalExp'

    tup = Tup()
    assign = Node('=', p[2])
    p[0] = Node('variable declaration', p[3].value, p[3].type, [p[1], assign, p[3]])
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value
    tup.variable = varname
    tup.value = p[3].value
    tup.type = p[3].type
    temp = 0
    if stack.find(varname) == -1:
        if(tup.value is None or tup.type is None):
            semantic_err.append("variable " + tup.variable + " not well defined")
        else:
            stack.push(tup)
    else:
        temp = stack.find(varname)
        temp.value = p[3].value
        temp.type = p[3].type


def p_varDeclaration1(p):
    'varDeclaration : variable ASSIGN sumExp'

    tup = Tup()
    assign = Node('=', p[2])
    p[0] = Node('variable declaration', p[3].value, p[3].type, [p[1], assign, p[3]])
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value
    tup.variable = varname
    tup.value = p[3].value
    tup.type = p[3].type
    temp = 0
    if stack.find(varname) == -1:
        if(tup.value is None or tup.type is None):
            semantic_err.append("variable " + tup.variable + " not well defined")
        else:
            stack.push(tup)
    else:
        temp = stack.find(varname)
        temp.value = p[3].value
        temp.type = p[3].type
    #code_str = "%s = %s" % (varname,p[3].value)
    #code = 'print('+code_str +')'
    #exec(code)



def p_varDeclaration2(p):
    'varDeclaration : variable ASSIGN STDIN'
    assign = Node('=', p[2])
    stdin = Node('stdin', p[3])
    p[0] = Node('variable to stdin', None,  None, [p[1], assign, stdin])
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value


def p_variableType(p):
    'variableType : number'

    p[0] = Node('numerical variable', p[1].value, p[1].type, [p[1]])

def p_number(p):
    'number : INTEGER'

    p[0] = Node('number',p[1].encode('ascii','ignore'), 'Num')

def p_number2(p):
    'number : FLOAT'
    p[0] = Node('number',p[1].encode('ascii','ignore'), 'Num')

def p_variableType2(p):
    'variableType : STRING'
    string = Node('str', p[1].encode('ascii','ignore'), 'String')
    p[0] = Node('string variable', string.value, string.type, [string])

def p_variableType3(p):
    'variableType : TRUE'

    t = Node('true', p[1].encode('ascii','ignore'), 'Bool')
    p[0] = Node('true variable', t.value, t.type, [t])

def p_variableType4(p):
    'variableType : FALSE'
    f = Node('false', p[1].encode('ascii','ignore'), 'Bool')
    p[0] = Node('false variable', f.value, f.type,  [f])

def p_constDeclaration(p):
    'constDeclaration : USE CONSTANT IDENTIFIER CONST_ASSIGN variableType'
    use = Node('use', p[1])
    c = Node('const', p[2])
    id = Node('id', p[3])
    ca = Node('const assign', p[4])
    p[0] = Node('constant declaration', p[5].value, p[5].type, [use, c, id, ca ,p[5]])

    tup = Tup()
    varname = c.value
    tup.variable = varname
    tup.value = p[5].value
    tup.type = p[5].type
    if stack.find(varname) == -1:
        if(tup.value is None or tup.type is None):
            pass
        else:
            stack.push(tup)
    else:
        temp = stack.find(varname)
        temp.value = p[5].value
        temp.type = p[5].type

def p_funcDeclaration(p):
    'funcDeclaration : PRINT LEFT_PAR factor RIGHT_PAR'
    pr = Node('print', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    p[0] = Node('print variable vt', None, None, [pr, lp, p[3] ,rp])
    temp = stack.find(p[3])
    varname = ''
    var_node = p[3].children[0]
    factor_type = p[3].type
    if(factor_type == 'Bool' or factor_type == 'Num' or factor_type == 'String'):
        factor_type = 'VAR'
    for i in range(len(var_node.children)):
        varname += var_node.children[i].value
    if(factor_type == 'None'):
        print(p[3].value)
    elif(factor_type == 'Var'):
        if stack.find(varname) == -1:
            semantic_err.append("undefined variable " + varname)
        else:
            temp = stack.find(varname)
            print("result ", temp.value)


def p_funcDeclaration2(p):
    'funcDeclaration : PRINT LEFT_PAR sumLessExpression RIGHT_PAR'

    pr = Node('print', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    p[0] = Node('print sum less', None, None, [pr, lp, p[3], rp])



def p_sumLessExpression(p):
    'sumLessExpression : variable PLUS_ONE'
    #print("++")
    p_one = Node('++', p[2], 'Num')
    p[0] = Node('plus one', None, [p[1], p_one ])
    tup = Tup()
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value
    tup.variable = varname
    if stack.find(varname) == -1:
        semantic_err.append("undefined variable " + varname)
    else:
        temp = stack.find(varname)
        temp.value = float(temp.value) + 1
        temp.type = temp.type
    #code_str = '' + varname + '=' + p[3].value + ''

def p_sumLessExpression1(p):
    'sumLessExpression : variable MINUS_ONE'
    #print("--")
    p_one = Node('--', p[2], 'Num')
    p[0] = Node('minus one', None, [p[1], p_one ])
    tup = Tup()
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value
    tup.variable = varname
    if stack.find(varname) == -1:
        semantic_err.append("undefined variable " + varname)
    else:
        temp = stack.find(varname)
        temp.value = float(temp.value) -1
        temp.type = temp.type

def p_statement(p):
    'statement : expression'
    p[0] = Node('statement - expression', None, None, [p[1]])

def p_statement2(p):
    'statement : conditionalStmt'
    p[0] = Node('statement - conditional', None, None, [p[1]])

def p_statement3(p):
    'statement : loopStmt'
    p[0] = Node('loop statement', None,  None,[p[1]])

def p_conditionalStmt(p):
    'conditionalStmt : matchedif'
    p[0] = Node('conditional mif', None, None,[p[1]])

def p_conditionalStmt2(p):
    'conditionalStmt : unmatchedif'
    p[0] = Node('conditional uif', None, None, [p[1]])

def p_matchedif(p):
    'matchedif : IF LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE ELSE LEFT_BRACE declarationList RIGHT_BRACE'
    i = Node('if', p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace', p[7])
    el = Node('else', p[8])
    lb2 = Node('left brace2', p[9])
    rb2 = Node('right brace2', p[11])

    p[0] = Node('matched if', None,None ,[i, lp, p[3], rp,lb, p[6], rb, el, lb2, p[10],rb2])

def p_unmatchedif(p):
    'unmatchedif : IF LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE'
    i = Node('if',p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace', p[7])
    p[0] = Node('unmatched if', None, None,  [i, lp, p[3], rp,lb, p[6], rb])

def p_loopStmt(p):
    'loopStmt : WHILE LEFT_PAR logicalExp RIGHT_PAR LEFT_BRACE declarationList RIGHT_BRACE'
    wh = Node('if',p[1])
    lp = Node('left par', p[2])
    rp = Node('right par', p[4])
    lb = Node('left brace', p[5])
    rb = Node('right brace',p[7])
    p[0] = Node('while', None, None, [wh, lp, p[3], rp,lb, p[6], rb])

def p_expression2(p):
    'expression : logicalExp'
    p[0] = Node('expression logical', None, None,  [p[1]])

def p_expression3(p):
    'expression : sumLessExpression'
    p[0] = Node('expression sumless ++ -- ', None, None, [p[1]])

def p_logicalExp3(p):
    'logicalExp : factor OR andExp'

    t = Node('true',p[1], 'Bool')
    o = Node('or',p[2],"logical")
    p[0] = Node('logical exp true', None, 'Bool', [t,o, p[3]])
    temp_bool_value = False
    temp_type = p[3].type
    if (temp_type == p[1].type and p[1].type == 'Bool'):
        if (True and p[3].value):
            temp_bool_value = True
        p[0].value = temp_bool_value
    else:
        str_error = "Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + o.value
        semantic_err.append(str_error)

def p_logicalExp5(p):
    'logicalExp : andExp'
    p[0] = Node('logical exp and', p[1].value, 'Bool', [p[1]])



def p_andExp3(p):
    'andExp : factor AND compExp'
    t = Node('true', p[1], 'Bool')
    a = Node('and',  p[2])
    p[0] = Node('and exp true', None, t.type, [t,a, p[3]])
    temp_bool_value = False
    temp_type = p[3].type
    if (temp_type == p[1].type and p[1].type == 'Bool'):
        if (True and p[3].value):
            temp_bool_value = True
        p[0].value = temp_bool_value
    else:
        str_error = "Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + a.value
        semantic_err.append(str_error)

def p_andExp5(p):
    'andExp : compExp'

    p[0] = Node('and exp comparison', p[1].value, 'Bool', [p[1]])

def p_compExp(p):
    'compExp : sumExp compSign sumExp'

    p[0] = Node('compexp', None, None, [p[1], p[2], p[3]])

    temp_bool_value  = False
    comp = p[2].value
    if comp == '<=':
        if(p[1].value <= p[3].value):
            temp_bool_value = True
    elif comp == '<':
        if(p[1].value < p[3].value):
            temp_bool_value = True
    elif comp == '>':
        if(p[1].value > p[3].value):
            temp_bool_value = True
    elif comp == '>=':
        if(p[1].value >= p[3].value):
            temp_bool_value = True
    elif comp == '==':
        if(p[1].value == p[3].value):
            temp_bool_value = True
    p[0].type = 'Bool'
    p[0].value = temp_bool_value


def p_compExp2(p):
    'compExp : sumExp'

    p[0] = Node('compExp to sumExp', p[1].value, p[1].type, [p[1]])

def p_compSign(p):
    'compSign : LESS_OR_EQUAL'

    p[0] = Node('<=',  p[1])

def p_compSign2(p):
    'compSign : LESS_THAN'

    p[0] = Node('<',  p[1])

def p_compSign3(p):
    'compSign : MORE_THAN'

    p[0] = Node('>',  p[1])

def p_compSign4(p):
    'compSign : GREATER_OR_EQUAL'

    p[0] = Node(' >=', p[1])

def p_compSign5(p):
    'compSign : EQ'

    p[0] = Node('== ', p[1])

def p_compSign6(p):
    'compSign : NEQ'
    p[0] = Node('!= ', p[1])

def p_sumExp(p):
    'sumExp : term sumSign sumExp'
    p[0] = Node('sumExp', None, None, [p[1], p[2], p[3]])
    aux_type = p[1].type
    aux_val = 0
    if p[3].type == aux_type:
        p[0].type = aux_type
        if p[2].value == '+':
            if p[3].type == 'Num' and p[3].type == p[1].type:
                aux_val = float(p[1].value) + float(p[3].value)
                p[0].value = aux_val
            else:
                semantic_err.append("Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value)

        if p[2].value == '-':
            if p[3].type == 'Num' and p[3].type == p[1].type:
                aux_val = float(p[1].value) - float(p[3].value)
                p[0].value = aux_val
            else:
                semantic_err.append("Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value)
    else:
        str_error = "Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value
        semantic_err.append(str_error)


def p_sumExp2(p):
    'sumExp : term'

    p[0] = Node('sumExp term', p[1].value, p[1].type, [p[1]])


def p_sumSign(p):
    'sumSign : MINUS'

    p[0] = Node('-',  p[1])
    #p[0] = Node('MINUS', None, [min])

def p_sumSign2(p):
    'sumSign : PLUS'

    p[0] = Node('+',  p[1])
    #p[0] = Node('PLUS', None, [plus])

def p_term(p):
    'term : multiNegExp multiSign term'
    p[0] = Node('term to multiNegExp', None, None, [p[1], p[2], p[3]])
    aux_type = p[1].type
    aux_val = 0
    if p[3].type == aux_type:
        p[0].type = aux_type
        if p[2].value == '*':
            if p[3].type == 'Num' and p[3].type == p[1].type:
                aux_val = float(p[1].value) * float(p[3].value)
                p[0].value = aux_val
            else:
                semantic_err.append("Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value)
        if p[2].value == '/':
            if p[3].type == 'Num' and p[3].type == p[1].type:
                aux_val = float(p[1].value) / float(p[3].value)
                p[0].value = aux_val
            else:
                semantic_err.append("Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value)
    else:
        str_error = "Semantic error not matching type " + p[1].type + " and " + p[3].type + " for operator " + p[2].value
        semantic_err.append(str_error)


def p_term2(p):
    'term : multiNegExp'

    p[0] = Node('term - multiNegExp', p[1].value, p[1].type, [p[1]])




def p_multiSign2(p):
    'multiSign : STAR'

    p[0] = Node('*', p[1])

def p_multiSign3(p):
    'multiSign : BETWEEN'

    p[0] = Node('/',  p[1])

def p_multiNegExp(p):
    'multiNegExp : unaryOp multiNegExp'
    p[0] = Node('multineg - unary', None, p[2].type, [p[1], p[2]])
    aux_val = p[2].value
    aux_op = p[1].value
    if aux_op == '-':
        aux_val = -int(aux_val)
        p[0].value = aux_val


def p_multiNegExp2(p):
    'multiNegExp : factor'

    p[0] = Node('multineg - factor', p[1].value, p[1].type, [p[1]])


def p_unaryOp(p):
    'unaryOp : MINUS'

    p[0] = Node('-', p[1])

def p_unaryOp2(p):
    'unaryOp : PLUS'

    p[0] = Node('+', p[1])

def p_factor(p):
    'factor : variable'

    p[0] = Node('factor - variable', None, 'Var', [p[1]])
    varname = ''
    for i in range(len(p[1].children)):
        varname += p[1].children[i].value
    tup_val = stack.find(varname)
    if tup_val == -1:
        semantic_err.append("Variable "+ varname + " is not declared")
    else:
        p[0].type = tup_val.type
        p[0].value = tup_val.value


def p_factor2(p):
    'factor : variableType'
    p[0] = Node('factor - variableType', p[1].value, p[1].type, [p[1]])


def p_factor3(p):
    'factor : IDENTIFIER'
    p[0] = Node('ID', p[1], 'ID')
    varname = p[1]
    tup_val = stack.find(varname)
    if tup_val == -1:
        semantic_err.append("identifier "+ varname + " is not declared")
    else:
        p[0].type = tup_val.type
        p[0].value = tup_val.value


def p_factor4(p):
    'factor : LEFT_PAR expression RIGHT_PAR'
    lp = Node('left par', p[1])
    rp = Node('right par', p[3])
    p[0] = Node('factor - exp', None, None, [lp, p[2], rp])

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

def semantic_errors(arr):
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
stack = Stack([])
parser = yacc.yacc(start="program", method="SLR")
result = parser.parse(str)
print("Stack\n")
for item in stack.list[::-1]:
    print(item.__dict__)

print("\n\n AST")
if (not errors_arr):
    pass
    if (not parse_err):
        print(result.traverse())
        if(not semantic_err):
            print("No semantic errors")
        else:
            print("Semantic errors")
            semantic_errors(semantic_err)

    else:
        if(len(parse_err) == 1 and "Syntax error at EOF" in parse_err):
            pass
        else:
            parsing_errors(parse_err)
else:
    lexer_errors(errors_arr)
