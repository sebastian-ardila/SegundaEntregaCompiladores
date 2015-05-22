
import ply.lex as lex
import math as math
import decimal

#Recerved Words

reserved = []

IF = 'if'; reserved.append(IF)
ELSE = 'ELSE'; reserved.append(ELSE)
WHILE = 'while'; reserved.append(WHILE)
PRINT = 'print'; reserved.append(PRINT)
READ = 'read'; reserved.append(READ)
RETURN = 'RETURN'; reserved.append(RETURN)
FOR = 'for'; reserved.append(FOR)
#THEN = 'THEN'; reserved.append(THEN)
FUNC = 'func'; reserved.append(FUNC)
FUNCTION = 'function'; reserved.append(FUNCTION)
PROC = 'proc'; reserved.append(PROC)
PROCEDURE = 'procedure'; reserved.append(PROCEDURE)

const = {}

const['PI'] = decimal.Decimal(math.pi),
const['GAMMA'] = decimal.Decimal(0.57721566490153286060),
const['EULER'] = decimal.Decimal(math.e),
const['DEG'] = decimal.Decimal(180/math.pi)


defaults = {}

defaults['sin'] = math.sin
defaults['cos'] = math.cos
defaults['tan'] = math.tan
defaults['asin'] = math.asin
defaults['acos'] = math.acos
defaults['atan'] = math.atan
defaults['abs'] = math.fabs
defaults['exp'] = math.exp
defaults['sqrt'] = math.sqrt
defaults['log10'] = math.log10
defaults['log'] = math.log
defaults['int'] = int
defaults['sinh'] = math.sinh
defaults['cosh'] = math.cosh
defaults['tanh'] = math.tanh

tokens = reserved + [ 
	#Literals  
	'NUMBER',
    'STRING',
	'ID',
	'BLTIN', 
	#'BEGIN',
	#'END',
	#Operators
	#'PLUS',
	#'MINUS', 
	#'TIMES', 
	#'DIVIDE', 
	#'MOD', 
	'OR', 
	'AND', 
	'NOT', 
	'INC',
	'DEC',
	'EQ', 
	'LT', 
	'LE', 
	'GT', 
	'GE', 
	'NE',
	'EXPONENT',
	#Assignment
	#'ASSIGN', 
	'ADDEQ', 
	'SUBEQ', 
	'MULEQ', 
	'DIVEQ', 
	'MODEQ', 
	#Delimeters 
	'LPAREN',
	'RPAREN',
	#'NEWLINE',
	#'COMMENTS',
	#'LBRACKET',
	#'RBRACKET',
	#'PERIOD'
	#'LBRACE',
    #'RBRACE',
    'LKEY',
    'RKEY',
	#'COMMA',
]

#Operators
#t_PLUS		= r'\+'
#t_MINUS	= r'-'
#t_TIMES 	= r'\*'
#t_DIVIDE	= r'\/'
#t_MOD		= r'%'
t_OR 		= r'\|'
t_AND		= r'&&'
t_NOT		= r'\!'
t_LT		= r'\<'
t_GT		= r'\>'
t_LE 		= r'\<\='
t_GE 		= r'\>\='
t_EQ 		= r'\=\='
t_NE 		= r'\!\='
t_EXPONENT  = r'\^'

#Comments
#t_COMMENTS	= r'\#.*'

#NewLine
#t_NEWLINE	= r'\n+'

#Assignment operators

#t_ASSIGN	= r'='
t_ADDEQ		= r'\+\='
t_SUBEQ		= r'-='
t_MULEQ		= r'\*\='
t_DIVEQ		= r'\/\='
t_MODEQ		= r'%='

#Increment/Decrement
t_INC       = r'[\+][\+]'
t_DEC       = r'[-][-]'

#Delimeters

t_LPAREN	= r'\('
t_RPAREN	= r'\)'
t_LKEY = r'\{'
t_RKEY = r'\}'
#t_LBRACKET	= r'\['
#t_RBRACKET	= r'\]'
#t_PERIOD    = r'\.'

#funcion que ignora caracteres
t_ignore = ' \t\r '

PLUS = '+'
MINUS = '-'
TIMES = '*'
DIVIDE = '/'
EQUAL = '='
LPAREN = '('
RPAREN = ')'
MOD = '%'
LKEY = '{'
RKEY = '}'
COMMA = ','
PUNTOYCOMMA = ';'
COMILLAS = '"'

literals = (
	PLUS,
	MINUS,
	TIMES,
	DIVIDE,
	EQUAL,
	LPAREN,
	RPAREN,
	MOD,
	LKEY,
	RKEY,
	COMMA,
	PUNTOYCOMMA,
	COMILLAS
	)



#Number
def t_NUMBER(t):
	r'(([0-9]+\.?[0-9]*)|([0-9]*\.[0-9]+))([Ee]([-+])?[0-9]+)?'
	try:
		t.value = int(t.value)	
	except:
		print "Linea: \""+ str(t.lineno) + "\" -> Expresion invalida \"" + str(t.value) + "\""
	return t

#Var
def t_ID(t):
  r'\w[a-zA-Z0-9_]*'
  if t.value in defaults.keys():
    t.type = "BLTIN"
  if t.value in reserved:
    t.type = str(t.value)
  elif t.value in const.keys():
    t.type = "NUMBER"
    t.value = const(t.value)
  else:
    t.type = "ID"
  return t


#String#

def t_STRING(t):
	r'\'.*\' | ".*"'
	string = ""
	if t.value[0] == '"':
		for i in t.value:
			if not (i == '"'):
				string = string + i
		else:
			if (t.value[0] == "'"):
				for i in t.value:
					if not (i == "'"):
						string = string + i
	t.value = str(string)
	return t



def t_newline(t):
    r'\n+'	
    t.lexer.lineno += len(t.value)

	

#Error
def t_error(t):
	print("Illegal character %s" % repr(t.value[0]))
	t.lexer.skip(1)

"""
with open ("Test.hoc", "r+") as myfile: #Se abre un archivo .hoc para hacer las pruebas. 
    archi=myfile.read()
"""
# print archi
lexer = lex.lex()
"""
lex.input(archi)

while 1:
    tok = lex.token()
    if not tok: break
    print tok
"""










