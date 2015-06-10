
# hoccode.py
# -*- coding: utf-8 -*-

import hocast
#import hocblock
from hocblock import *
from collections import defaultdict

# diccionarios:

binary_ops = {
	'+' : 'add',
	'-' : 'sub',
	'*' : 'mul',
	'/' : 'div',
	'<' : 'lt',
	'>' : 'gt',
	'==': 'eq',
	'!=': 'ne',
	'<=': 'le',
	'>=': 'ge',
	'&&': 'land',
	'||': 'lor',
}

unary_ops = {
	'+' : 'uadd',
	'-' : 'usub',
	'!' : 'lnot',
}

ops = {
	'+=' : 'addeq',
	'-=' : 'subeq',
	'*=' : 'muleq',
	'/=' : 'diveq',
	'%=' : 'modeq',
}

#paso 2:
class GenerateCode(hocast.NodeVisitor):

    def __init__(self):
        super(GenerateCode, self).__init__()

        self.versions = defaultdict(int)

        self.code = BasicBlock()
        self.start_block = self.code
        self.externs = []

    def new_temp(self,typeobj):
        name = "__%s_%d" % (typeobj, self.versions[typeobj])
        self.versions[typeobj] += 1
        return name

    def printCode(self):
        print "\n El codigo maquina SSA es\n"
        for i in range(len(self.code.block)):
            print (self.code.block[i])

    def printCodeIF(self, j):
        print "\n IF SSA \n"
        if j == 1:
            print "Condicion: "
        elif j == 2:
            print "True: "
        elif j == 3:
            print "False: "
        for i in range(len(self.code.block)):
            print (self.code.block[i])

    def printCodeWHILE(self, j):
        print "\n WHILE SSA \n"
        if j == 1:
            print "Condicion: "
        elif j == 2:
            print "Body: "
        for i in range(len(self.code.block)):
            print(self.code.block[i])

    def printCodeFOR(self, j):
        print "\n FOR SSA \n"
        if j == 1:
            print "Condicion: "
        elif j == 2:
            print "Body: "
        for i in range(len(self.code.block)):
            print(self.code.block[i])

    def ADDCode(self, code):
        for i in range(len(code.block)):
            self.start_block.append(code.block[i])

    def visit_List(self,node):
        for expr in node.expressions:
            self.visit(expr)
        self.printCode()

    def visit_stmtExpression(self,node):
        self.visit(node.expressions)

    def visit_ID(self,node):
        target = self.new_temp("Float")
        inst = ('Load'+"Float",node.id,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_StoreVar(self,node):
        target = self.new_temp(node.type)
        inst = ('Store'+node.type,node.id,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_Assignment(self,node):
        self.visit(node.expressions)
        target = self.new_temp(node.type)
        code = node.op
        if code in ops:
            if code == '+=':
                op=ops[code]+"_"+node.type
            elif code == '-=':
                op=ops[code]+"_"+node.type
            elif code == '*=':
                op=ops[code]+"_"+node.type
            elif code == '/=':
                op=ops[code]+"_"+node.type
            elif opcode == '%=':
                op=ops[code]+"_"+node.type

        inst = (op,node.id.id,node.expressions.gen_location,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_Literal(self,node):
        if type(node.value) == float:
            node.type = "Float"
        elif type(node.value) == str:
            node.type = "String"

        target = self.new_temp(node.type)
        inst = ('Literal_'+node.type, node.value,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_BinaryOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        node.type = "Float"

        target = self.new_temp("Float")

        if node.op in binary_ops:
            opcode = binary_ops[node.op] + "_"+"Float"
        elif node.op in binary_ops_logics:
            opcode = "cmp" + "_"+"Float"

        inst = (opcode, node.left.gen_location, node.right.gen_location, target)
        self.code.append(inst)

        node.gen_location = target

    def visit_RelationalOp(self,node):
        self.visit(node.left)
        self.visit(node.right)

        target = self.new_temp(node.type)

        opcode = "cmp" + "_"+node.left.type.name
        inst = (opcode, binary_ops[node.op], node.left.gen_location, node.right.gen_location, target)
        self.code.append(inst)
        node.gen_location = target

    def visit_PrintStatement(self,node):

        self.visit(node.expr)

        #inst = ('print_'+node.expr.type.name, node.expr.gen_location)
        #self.code.append(inst)

    def visit_Program(self,node):
        self.visit(node.program)

    def visit_ConstDeclaration(self,node):

        inst = ('alloc_'+node.type.name,node.id)
        self.code.append(inst)

        self.visit(node.value)
        inst = ('store_'+node.type.name,node.value.gen_location,node.id)
        self.code.append(inst)

    def visit_VarDeclaration(self,node):

        inst = ('alloc_'+node.type.name,node.id)
        self.code.append(inst)
        if node.value:
            self.visit(node.value)
            inst = ('store_'+node.type.name,node.value.gen_location,node.id)
            self.code.append(inst)

    def visit_LoadLocation(self,node):
        target = self.new_temp(node.type)
        inst = ('load_'+node.type.name,node.name,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_AssignmentStatement(self,node):
        self.visit(node.value)
        inst = ('Store_'+node.value.type,node.value.gen_location,node.location.id)
        self.code.append(inst)

    def visit_UnaryOp(self,node):
        self.visit(node.left)
        target = self.new_temp(node.type)
        opcode = unary_ops[node.op] + "_" + node.left.type.name
        inst = (opcode, node.left.gen_location)
        self.code.append(inst)
        node.gen_location = target

    def visit_IfStatement(self,node):
        if_block = IfBlock()
        self.code.next_block = if_block
        self.switch_block(if_block)
        self.visit(node.condition)
        if_block.test = node.condition.gen_location

        if_block.if_branch = BasicBlock()
        self.switch_block(if_block.if_branch)
        self.visit(node.then_b)

        if node.else_b:
            if_block.else_branch = BasicBlock()
            self.switch_block(if_block.else_branch)
            self.visit(node.else_b)

        if_block.next_block = BasicBlock()
        self.switch_block(if_block.next_block)

    def visit_WhileStatement(self, node):
        while_block = WhileBlock()
        self.code.next_block = while_block

        self.switch_block(while_block)
        self.visit(node.condition)
        while_block.test = node.condition.gen_location

        while_block.body = BasicBlock()
        self.switch_block(while_block.body)
        self.visit(node.body)
        while_block.next_block = BasicBlock()
        self.switch_block(while_block.next_block)

    def visit_ForStatement(self,node):
        for_block = BasicBlock()
        self.code.next_block = for_block
        self.switch_block(for_block)
        self.visit(node.condition1); self.visit(node.condition2); self.visit(node.condition3)
        self.printCodeFOR(1)
        for_block.test = node.condition2.gen_location

        for_block.for_branch = BasicBlock()
        self.switch_block(for_block.for_branch)
        self.visit(node.condition3)
        self.addCode(self.code)

        for_block.body = BasicBlock()
        self.switch_block(for_block.body)
        self.visit(node.body)
        self.printCodeFOR(2)
        self.addCode(self.code)

        for_block.next_block = BasicBlock()
        self.switch_block(for_block.next_block)

    def visit_NotCondition(self,node):
        self.visit(node.left)
        target = self.new_temp(node.type)
        opcode = "cmp" + "_"+node.type
        inst = (opcode, unary_ops[node.op], node.left.gen_location,target)
        self.code.append(inst)
        node.gen_location = target

    def visit_sttlist(self,node):
        self.visit(node.body)

    def visit_stmtList(self,node):
        for expr in node.expressions:
            self.visit(expr)

    def visit_ReturnStatement(self,node):
        self.visit(node.value)

    def visit_Exprlist(self,node):
        for expr in node.expressions:
            if type(expr) == float:
                expr.type = "float"
            elif type(expr) == str:
                expr.type = "string"
            self.visit(expr)
            inst = ('print_'+expr.type, expr.gen_location)

            target = self.new_temp(expr.type)
            node.gen_location=target
            self.code.append(inst)


    def switch_block(self, next_block):
        self.code = next_block

    def visit_Group(self,node):
        self.visit(node.expression)
        node.gen_location = node.expression.gen_location

# STEP 3: Probar
#
# Trate de correr este programa con un archivo adecuado para tal efecto y vea
# la secuencia del codigo SSA resultante.
#
#     bash % python hoccode.py good.pas
#     ... vea la salida ...
#
# ----------------------------------------------------------------------
#            NO MODIFIQUE NADA DE AQUI EN ADELANTE
# ----------------------------------------------------------------------
def generate_code(node):

	gen = GenerateCode()
	gen.visit(node)
	return gen

if __name__ == '__main__':
	import hoclex
	import hocparse
	import hoccheck
	import sys
	from errors import subscribe_errors, errors_reported
	lexer = hoclex.make_lexer()
	parser = hocparse.make_parser()
	with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
		program = parser.parse(open(sys.argv[1]).read())
		# Revise el programa
		hoccheck.check_program(program)

		if not errors_reported():
			code = generate_code(program)

			hocblock.PrintBlocks().visit(code.start_block)
			#for inst in code.code:
			#    print(inst)
