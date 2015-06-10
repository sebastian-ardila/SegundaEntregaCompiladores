# mpasast.py
# -*- coding: utf-8 -*-
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
	'''
	Clase base para todos los nodos del AST.  Cada nodo se espera
	definir el atributo _fields el cual enumera los nombres de los
	atributos almacenados.  El método a continuación __init__() toma
	argumentos posicionales y los asigna a los campos apropiados.
	Cualquier argumento adicional especificado como keywords son
	también asignados.
	'''
	_fields = []
	def __init__(self,*args,**kwargs):
		assert len(args) == len(self._fields)
		for name,value in zip(self._fields,args):
			setattr(self,name,value)
		# Asigna argumentos adicionales (keywords) si se suministran
		for name,value in kwargs.items():
			setattr(self,name,value)

	def pprint(self):
		for depth, node in flatten(self):
			print("%s%s" % (" "*(4*depth),node))

def validate_fields(**fields):
	def validator(cls):
		old_init = cls.__init__
		def __init__(self, *args, **kwargs):
			old_init(self, *args, **kwargs)
			for field,expected_type in fields.items():
				assert isinstance(getattr(self, field), expected_type)
		cls.__init__ = __init__
		return cls
	return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

class PrintStatement(AST):
	'''
	print expression ;
	'''
	_fields = ['expr']

class Literal(AST):
	'''
	Un valor constante como 2, 2.5, o "dos"
	'''
	_fields = ['value']

class Program(AST):
	_fields = ['program']


@validate_fields(statements=list)
class Statements(AST):
	_fields = ['statements']

	def append(self,e):
		self.statements.append(e)
	
class Statement(AST):
	_fields = ['statement']

class Extern(AST):
	_fields = ['func_prototype']

class FuncPrototype(AST):
	_fields = ['id', 'params', 'typename', 'statements']

class ProcPrototype(AST):
	_fields = ['id', 'params', 'typename', 'statements']

class ProcedureCall(AST):
    _fields = ['id','params']


@validate_fields(param_decls=list)
class Parameters(AST):
	_fields = ['param_decls']

	def append(self,e):
		self.param_decls.append(e)

class ParamDecl(AST):
	_fields = ['id', 'typename']

class ID(AST):
	_fields = ['id']

class AssignmentStatement(AST):
	_fields = ['location', 'value']

class AddEqualStatement(AST):
	_fields = ['location', 'value']

class SubEqualStatement(AST):
	_fields = ['location', 'value']

class MulEqualStatement(AST):
	_fields = ['location', 'value']

class DivEqualStatement(AST):
	_fields = ['location', 'value']

class ModEqualStatement(AST):
	_fields = ['location', 'value']


class ConstDeclaration(AST):
	_fields = ['id', 'value']

class VarDeclaration(AST):
	_fields = ['id', 'typename', 'value']

class IfStatement(AST):
	_fields = ['condition', 'then_b', 'else_b']


class WhileStatement(AST):
	_fields = ['condition', 'body']
	
@validate_fields(condition = list)
class ForStatement(AST):
	_fields = ['condition1','condition2', 'condition3', 'body']

class LoadLocation(AST):
	_fields = ['name']

class StoreVar(AST):
	_fields = ['name']

class UnaryOp(AST):
	_fields = ['op', 'left']

class BinaryOp(AST):
	_fields = ['op', 'left', 'right']

class RelationalOp(AST):
	_fields = ['op', 'left', 'right']
	
class Group(AST):
	_fields = ['expression']

class FunCall(AST):
	_fields = ['id', 'params']

@validate_fields(expressions=list)
class List(AST):
	_fields = ['expressions']

	def append(self, e):
		self.expressions.append(e)

@validate_fields(expressions=list)
class stmtList(AST):
	_fields = ['expressions']

	def append(self, e):
		self.expressions.append(e)

@validate_fields(expressions=list)
class asgnList(AST):
	_fields = ['expressions']

	def append(self, e):
		self.expressions.append(e)

@validate_fields(expressions=list)
class ExprList(AST):
	_fields = ['expressions']

	def append(self, e):
		self.expressions.append(e)

class CallReturn(AST):
	_fields = ['stmt_return']

class Empty(AST):
	_fields = []





# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration,
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
	de una clase similar en la librería estándar ast.NodeVisitor.  Para
	cada nodo, el método visit(node) llama un método visit_NodeName(node)
	el cual debe ser implementado en la subclase.  El método genérico
	generic_visit() es llamado para todos los nodos donde no hay coincidencia
	con el método visit_NodeName().

	Es es un ejemplo de un visitante que examina operadores binarios:

		class VisitOps(NodeVisitor):
			visit_Binop(self,node):
				print("Operador binario", node.op)
				self.visit(node.left)
				self.visit(node.right)
			visit_Unaryop(self,node):
				print("Operador unario", node.op)
				self.visit(node.expr)

		tree = parse(txt)
		VisitOps().visit(tree)
	'''
	def visit(self,node):
		'''
		Ejecuta un método de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None
	
	def generic_visit(self,node):
		'''
		Método ejecutado si no se encuentra médodo aplicable visit_.
		Este examina el nodo para ver si tiene _fields, es una lista,
		o puede ser recorrido completamente.
		'''
		for field in getattr(node,"_fields"):
			value = getattr(node,field,None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item,AST):
						self.visit(item)
			elif isinstance(value, AST):
				self.visit(value)



# NO MODIFICAR
class NodeTransformer(NodeVisitor):
	'''
	Clase que permite que los nodos del arbol de sintraxis sean
	reemplazados/reescritos.  Esto es determinado por el valor retornado
	de varias funciones visit_().  Si el valor retornado es None, un
	nodo es borrado. Si se retorna otro valor, reemplaza el nodo
	original.

	El uso principal de esta clase es en el código que deseamos aplicar
	transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
	del compilador o ciertas reescrituras de pasos anteriores a la generación
	de código.
	'''
	def generic_visit(self,node):
		for field in getattr(node,"_fields"):
			value = getattr(node,field,None)
			if isinstance(value,list):
				newvalues = []
				for item in value:
					if isinstance(item,AST):
						newnode = self.visit(item)
						if newnode is not None:
							newvalues.append(newnode)
					else:
						newvalues.append(n)
				value[:] = newvalues
			elif isinstance(value,AST):
				newnode = self.visit(value)
				if newnode is None:
					delattr(node,field)
				else:
					setattr(node,field,newnode)
		return node

# NO MODIFICAR
def flatten(top):
	'''
	Aplana el arbol de sintaxis dentro de una lista para efectos
	de depuración y pruebas.  Este retorna una lista de tuplas de
	la forma (depth, node) donde depth es un entero representando
	la profundidad del arból de sintaxis y node es un node AST
	asociado.
	'''
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self,node):
			self.nodes.append((self.depth,node))
			self.depth += 1
			NodeVisitor.generic_visit(self,node)
			self.depth -= 1

	d = Flattener()
	d.visit(top)
	return d.nodes


class DotVisitor(NodeVisitor):

	def __init__(self, node):
		self.dot = "digraph AST{\n"
		self.id = 0
		self.visit(node)

	def generateDot(self):
		import subprocess
		name = "tree"
		name_format = name + ".dot"
		f = open('img/'+name_format+'', 'w+')
		f.write(self.dot+ "\n}")
		f.close()
		subprocess.call("dot -Tpng img/"+name_format+" -o img/"+name+".png")

	def __str__(self):
		return self.dot + "\n}"

	def generateId(self):
		self.id += 1
		return "n"+ str(self.id)

	def visit_BinaryOp(self, node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="' + node.op + '"'+"];\n"
		l = self.visit(node.left)
		r = self.visit(node.right)
		self.dot += "\t" + name + " -> " + l + ";\n"
		self.dot += "\t" + name + " -> " + r + ";\n"
		return name

	def visit_UnaryOp(self, node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="' + node.op + '"'+"];\n"
		l = self.visit(node.left)
		self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_Location(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="Location('+node.name+')"];\n'
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
		return name

	def visit_ID(self, node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="VAR(' + node.id + ')"];\n'
		for depth,node2 in flatten(node):
			if depth==1:
				n = self.visit(node2)
				self.dot += "\t" + name + " -> " + n + ";\n"
		return name


	def visit_List(self,node):
		name = "program"
		self.dot += "\t" + name + '[shape=Msquare,label="program"];\n'
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_Literal(self, node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="Literal(' + str(node.value) + ')"];\n'
		return name


	def visit_AssignmentStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label= "="];\n'
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_AddEqualStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="+="];\n'
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_SubEqualStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="-="];\n'
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_MulEqualStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="*="'+"];\n"
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_DivEqualStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="/="'+"];\n"
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_ModEqualStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="%="'+"];\n"
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name


	def visit_PrintStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="Print"'+"];\n"
		l = self.visit(node.expr)
		self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_WhileStatement(self,node): 
		name = self.generateId()
		self.dot += "\t" + name + '[label= "while"'+"];\n"
		condition = self.visit(node.condition)
		body = self.visit(node.body)

		self.dot += "\t" + name + " -> " + condition + ";\n"
		self.dot += "\t" + name + " -> " + body + ";\n"
		return name


	def visit_ForStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label= "for"];\n'
		self.dot += "\t" + name + '_id[label= "initVar"];\n'
		self.dot += "\t" + name + '_cond[label= "cond"];\n'
		self.dot += "\t" + name + '_increment[label= "increment"];\n'
		self.dot += "\t" + name + " -> " + name + "_id;\n"
		self.dot += "\t" + name + " -> " + name + "_cond;\n"
		self.dot += "\t" + name + " -> " + name + "_increment;\n"

		l = self.visit(node.condition[0])
		self.dot += "\t" + name + "_id -> " + l + ";\n"
		l = self.visit(node.condition[1])
		self.dot += "\t" + name + "_cond -> " + l + ";\n"
		l = self.visit(node.condition[2])
		self.dot += "\t" + name + "_increment -> " + l + ";\n"
		
		body = self.visit(node.body)
		self.dot += "\t" + name + " -> " + body + ";\n"
		return name

	def visit_IfStatement(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label= "if"'+"];\n"

		condition = self.visit(node.condition)
		l = self.visit(node.then_b)

		self.dot += "\t" + name + " -> " + condition + ";\n"
		self.dot += "\t" + name+"_then" + '[label= "then"'+"];\n"
		self.dot += "\t" + name+"_then" + " -> " + l + ";\n"
		self.dot += "\t" + name + " -> " + name+"_then" + ";\n"

		r = self.visit(node.else_b)
		if r != None:
			self.dot += "\t" + name+"_else" + '[label= "else"'+"];\n"
			self.dot += "\t" + name + " -> " + name+"_else" + ";\n"
			self.dot += "\t" + name+"_else" + " -> " + r + ";\n"

		return name

	def visit_stmtList(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="stmtList"'+"];\n"
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_FunCall(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="callFunction"'+"];\n"
		id_func = self.visit(node.id)
		args = self.visit(node.params)
		self.dot += "\t" + name + " -> " + args + ";\n"
		self.dot += "\t" + name + " -> " + id_func + ";\n"
		return name


	def visit_ExprList(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="ExprList"'+"];\n"
		for i in node.expressions:
			l = self.visit(i)
			self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_FuncPrototype(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label= "defFunc"'+"];\n"
		id_func = self.visit(node.id)
		args = self.visit(node.params)
		statements = self.visit(node.statements)
		self.dot += "\t" + name + " -> " + statements + ";\n"
		self.dot += "\t" + name + " -> " + args + ";\n"
		self.dot += "\t" + name + " -> " + id_func + ";\n"
		return name

	def visit_ProcPrototype(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label= "defProc"'+"];\n"
		id_func = self.visit(node.id)
		args = self.visit(node.params)
		statements = self.visit(node.statements)
		self.dot += "\t" + name + " -> " + statements + ";\n"
		self.dot += "\t" + name + " -> " + args + ";\n"
		self.dot += "\t" + name + " -> " + id_func + ";\n"
		return name

	def visit_Parameters(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="args"'+"];\n"
		for depth, node2 in flatten(node):
			if depth == 1:
				l = self.visit(node2)
				self.dot += "\t" + name + " -> " + l + ";\n"
		return name

	def visit_CallReturn(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="return"'+"];\n"
		stmt_return = self.visit(node.stmt_return)
		self.dot += "\t" + name + " -> " + stmt_return + ";\n"
		return name

	def visit_Empty(self,node):
		name = self.generateId()
		self.dot += "\t" + name + '[label="empty"];\n'
		return name
