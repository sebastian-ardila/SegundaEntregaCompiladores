import ply.yacc as yacc
from LexicAnalizator import *
from hocast import *
import decimal

precedence = (
	("right", '=', 'ADDEQ', 'SUBEQ', 'MULEQ', 'DIVEQ', 'MODEQ'), 
	("left", 'OR'),
	("left", 'AND'), 
	("left", 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'RETURN'), 
	("left", '+', '-'), 
	("left", '*', '/', '%', ','), 
	("left", 'NOT', 'POSTINC'), 
	("right", 'EXPONENT', 'THEN', 'ELSE', 'PREINC')
	)

#-----------------------------------------------------------
#List#
def p_list_empty(p):
	"list : empty"
	p[0] = List([])

# def p_list_defn(p):
# 	"list : list defn"
# 	p[0] = p[1]
# 	p[0].append(p[2])

def p_list_asgn(p):
	"list : list asgn"
	p[0] = p[1]
	p[0].append(p[2])


def p_list_stmt(p):
	"list : list stmt"
	p[0] = p[1]
	p[0].append(p[2])

#-----------------------------------------------------------

#Assignment#

def p_asgn_assign(p):
	"asgn : ID '=' expr"
	p[0] = AssignmentStatement(ID(p[1]),p[3])

def p_asgn_addeq(p):
	"asgn : ID ADDEQ expr"
	p[0] = AddEqualStatement(ID(p[1]), p[3])

def p_asgn_subeq(p):
	"asgn : ID SUBEQ expr"
	p[0] = SubEqualStatement(ID(p[1]), p[3])

def p_asgn_muleq(p):
	"asgn : ID MULEQ expr"
	p[0] = MulEqualStatement(ID(p[1]), p[3])


def p_asgn_diveq(p):
	"asgn : ID DIVEQ expr"
	p[0] = DivEqualStatement(ID(p[1]), p[3])

def p_asgn_modeq(p):
	"asgn : ID MODEQ expr"
	p[0] = ModEqualStatement(ID(p[1]), p[3])

#-----------------------------------------------------------
def p_stmt_expr(p):
  "stmt : expr"
  p[0] = p[1]

def p_stmt_returnexpr(p):
	"stmt : return '(' expr ')'"
	p[0] = CallReturn(p[3])

def p_stmt_procedure(p):
  "stmt : procedure begin '(' arglist ')'"
  p[0] = ProcedureCall(p[1],p[4]) 

def p_stmt_print(p):
	"stmt : print prlist"
	p[0] = PrintStatement(p[2])

def p_stmt_while(p):
	"stmt : while '(' cond ')' stmt end"
	p[0] = WhileStatement(p[3], p[5])

def p_stmt_for(p):
	"stmt : for '(' cond ';' cond ';' cond ')' stmt end"
	p[0] = ForStatement([p[3], p[5], p[7]], p[9])

def p_stmt_if(p): 
	"stmt :	if '(' cond ')' stmt end %prec THEN"
	p[0] = IfStatement(p[3], p[5], "")

def p_stmt_elif(p):
	"stmt : if '(' cond ')' stmt end ELSE stmt end"
	p[0] = IfStatement(p[3], p[5], p[8])

def p_stmt_stmtlist(p):
	"stmt : '{' stmtlist '}'"
	p[0] = p[2]

#-----------------------------------------------------------
def p_cond(p):
  "cond : expr"
  p[0] = p[1]

def p_begin(p):
	"begin : "
	pass

def p_end(p):
	"end : "
	pass

def p_stmtlist(p):
  "stmtlist : empty"
  p[0] = stmtList([])

# def p_stmtlist_expr(p):
# 	"stmtlist : '\"' STRING '\"'"
#  	p[0] = p[1]

def p_stmtlist_stmtl_stmt(p):
	"stmtlist : stmtlist stmt"
	p[0] = p[1]
	p[0].append(p[2])



#-----------------------------------------------------------

def p_expr_id(p):
	"expr : ID"
	p[0] = ID(p[1])


def p_expr_read(p):
	"term : read '(' ID ')'"
	p[0] = FunCall(p[1], ID(p[3]))

def p_expr_bltin(p):
  "expr : BLTIN '(' expr ')'"
  p[0] = FunCall(p[1],p[3])

def p_expr_asgn(p):
	"expr : asgn"
 	p[0] = p[1]

#Operators#
def p_expr_plus(p):
	"expr : expr '+' expr"
	p[0] = BinaryOp(p[2], p[1], p[3])

	
def p_expr_minus(p):
	"expr : expr '-' expr"
	p[0] = BinaryOp(p[2], p[1], p[3])
	

def p_expr_times(p):
	"expr : expr '*' expr"
	p[0] = BinaryOp(p[2], p[1], p[3])

	

def p_expr_divide(p):
	"expr : expr '/' expr"
	p[0] = BinaryOp(p[2], p[1], p[3])
	

def p_expr_num(p):
	'expr : NUMBER'
	p[0] = Literal(float(p[1]))


def p_expr_exponent(p):
	"expr : expr EXPONENT expr"
	p[0] = BinaryOp(p[2], p[1], p[3])

def p_expr_term(p):
	"expr : term"
	p[0] = p[1]

def p_term_factor(p):
	"term : factor"
	p[0] = p[1]
	

def p_factor_expr(p):
	"factor : '(' expr ')'"
	p[0] = p[2]
	

def p_expr_mod(p):
	"expr : expr '%' expr"
	p[0] = BinaryOp(p[2], p[1], p[3])

	
def p_expr_or(p):
	"expr : expr OR expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_and(p):
	"expr : expr AND expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_not(p):
	"expr : NOT expr"
	p[0] = UnaryOp(p[1], p[2])


def p_expr_lt(p):
	"expr : expr LT expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_gt(p):
	"expr : expr GT expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_le(p):
	"expr : expr LE expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_ge(p):
	"expr : expr GE expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_eq(p):
	"expr : expr EQ expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_ne(p):
	"expr : expr NE expr"
	p[0] = BinaryOp(p[2], p[1], p[3])


def p_expr_incleft(p):
	"expr : INC ID %prec PREINC"
	mensaje = AssignmentStatement(ID(p[2]),BinaryOp('+',ID(p[2]),Literal(decimal.Decimal(1))))
	p[0] = mensaje

def p_expr_decleft(p):
	"expr : DEC ID %prec PREINC"
	mensaje = AssignmentStatement(ID(p[2]),BinaryOp('-',ID(p[2]),Literal(decimal.Deciaml(1))))
	p[0] = mensaje

def p_expr_decright(p):
	"expr : ID DEC %prec POSTINC"
	mensaje = AssignmentStatement(ID(p[1]),BinaryOp('-',ID(p[1]),Literal(decimal.Decimal(1))))
	p[0] = mensaje

def p_expr_incright(p):
	"expr : ID INC %prec POSTINC"
	mensaje = AssignmentStatement(ID(p[1]),BinaryOp('+',ID(p[1]),Literal(decimal.Decimal(1))))
	p[0] = mensaje

#-------------------------------------------------------------------------------------#
"""
def p_expr_prlist(p):
	'prlist : expr'
	p[0] = ExprList(p[1])
"""
def p_prlist_string(p):
	"prlist : STRING"
	p[0] = ExprList([Literal(p[1])])

def p_prlist_prlexpr(p):
	"prlist : prlist ',' expr"
	p[0] = p[1]
	p[0].append(p[3])

def p_prlist_prlstring(p):
	"prlist : prlist ',' STRING"
	p[0] = p[1]
  	p[0].append(Literal(""+p[3]+""))
	

#-----------------------------------------------------------

def p_defn_func(p):
	"defn : func procname '(' arglist ')' stmt"
	p[0] = FuncPrototype(p[2], p[4], "", p[6])

def p_defn_proc(p):
	"defn : proc procname '(' arglist ')' stmt"
	p[0] = ProcPrototype(p[2], p[4], "", p[6])

#-----------------------------------------------------------
"""
def p_procname_ID(p):
	"procname : ID"
	p[0] = ID(p[1])
"""

def p_procname_function(p):
	"procname : function"
	p[0] = p[1]

def p_procname_procedure(p):
	"procname : procedure"
	p[0] = p[1]

#-----------------------------------------------------------

def p_arglist(p):
	"arglist : empty"
	p[0] = Parameters(None)

def p_arglist_arglist(p):
	"arglist : arglist ',' expr"
	p[0] = p[1]
	p[0].append(p[3])

def p_arglist_expr(p):
  "arglist : expr"
  p[0] = Parameters([p[1]])

#-----------------------------------------------------------
#Empty production

def p_empty(p):
    'empty : '
    p[0] = Empty()
    pass	


#-----------------------------------------------------------
#Reserved words#

# def p_if(p):
# 	'if : IF'
# 	p[0] = p[1]

def p_else(p):
	'else : ELSE'
	p[0] = p[1]

# def p_while(p):
# 	'while : while'
# 	p[0] = p[1]

# def p_print(p):
# 	'print : PRINT'
# 	p[0] = p[1]

# def p_read(p):
# 	'read : READ'
# 	p[0] = p[1]

def p_return(p):
	'return : RETURN'
	p[0] = p[1]

# def p_for(p):
# 	'for : FOR'
# 	p[0] = p[1]

#-----------------------------------------------------------

# Error rule for syntax errors
def p_error(p):
  if p:
    print "Syntax error at token ", p.value, "in line", p.lineno
    parser.errok()
  else:
    print("Syntax error at EOF")

   
# Build the parser
parser = yacc.yacc(debug=True, start='list')
"""a
while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   tree = DotVisitor(result)
   tree.generateDot() #Metodo que dibuja el arbol. 

"""
try:
  f = open('input.in', 'r')
  s = f.read()
  f.close()
except EOFError:
  print "Error Leyendo Archivo"

if s:
  lexer.input(s)
  result = parser.parse(s)
  tree = DotVisitor(result)
  tree.generateDot()






