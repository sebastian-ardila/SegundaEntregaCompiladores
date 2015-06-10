# hoccheck.py
# -*- coding: utf-8 -*-
 
import sys, re, string, types
#from errors import error
from hocast import *
 
class SymbolTable(object):

    def __init__(self, parent=None):

        self.symtab = {}
        self.parent = parent
        if self.parent != None:
            if hasattr(self.parent,"children"):
                self.parent.children.append(self)
            else:
                self.parent.children = [self]

        self.children = []

    def add(self, a, v):

        self.symtab[a] = v

 
    def lookup(self, a):
        if self.symtab.has_key(a):
            return self.symtab[a]
        else:
            if self.parent != None:
                return self.parent.lookup(a)
            else:
                return None
 
class CheckProgramVisitor(NodeVisitor):
    def __init__(self):
        self.errors = []
        self.supSymtable = ""
        pass
         
    def push_symtab(self, node):
        self.current = SymbolTable(self.current)
        node.symtab = self.current
         
    def pop_symbol(self):
        self.current = self.current.parent
    

    def imprimirTabla(self,node,depth):
        print("Tabla de Simbolos: %s%s" % (" "*(4*depth),node.symtab))
        for i in node.children:
            self.printTable(i,depth+1)

    def visit_UnaryOp(self, node):
        node.left.parent = node.parent
        left = self.visit(node.left)
        return float(not left)

    def visit_BinaryOp(self,node):
        node.left.parent = node.op; node.right.parent = node.op
        left = self.visit(node.left); right = self.visit(node.right)
        assert type(left) == type(right), "no coinciden los tpos de datos en esta asignacion"
        return eval(str(left)+node.op+str(right))


    def visit_List(self,node):
        self.supSymtable = SymbolTable()
        self.current = self.supSymtable
        node.symtab = self.supSymtable
        node.symtab.symtab['Funcs'] = {}
        for visitante in node.expressions:
            self.visit(visitante)
        print "Errors: ",len(self.errors)
        for error in range(len(self.errors)):
            print " Error (",error,") =>",self.errors[error]
        self.printTable(node.symtab,0)

    
    def visit_Literal(self,node):
        #value = node.visit(node.value)
        return node.value

    def visit_ID(self,node):
        value = self.current.lookup(node.id)
        if value != None:
            return value
        else:
            self.errors.append("la variable no se encuentra definida ->"+ node.id)

    def visit_PrintStatement(self,node):
        value = self.visit(node.expr)

    def visit_FuncPrototype(self, node):
        if self.supSymtable.lookup(node.id):
            error(node.lineno, "%s <- Este simbolo  ya se encuentra definido" % node.id)
        else:
            lista=[]
            self.push_symtab(node)
            node.parent = self.supSymtable
            for identificador in node.params.param_decls:
                lista.append(identificador.id)
            for objeto in lista:
                node.symtab.add(objeto,0.0)
            self.supSymtable.symtab["Funcs"][node.id.id]={"args":lista}
            node.statements.parent = self.current.symtab
            self.visit(node.statements)
            self.pop_symbol()

    def visit_Assignment(self,node):
        expr = self.visit(node.expressions)
        var = self.current.lookup(node.id.id)
        op = node.op
        if var != None:
            if op == '+=':
                self.current.symtab[node.id.id] = var + expr
            if op == '-=':
                self.current.symtab[node.id.id] = var - expr
            if op == '*=':
                self.current.symtab[node.id.id] = var * expr
            if op == '/=':
                self.current.symtab[node.id.id] = var / expr
            if op == '%=':
                self.current.symtab[node.id.id] = var % expr

    def visit_AssignmentStatement(self,node):
        identificadores  = self.current.lookup(node.location.id)
        expr = self.visit(node.value)
        if identificadores != None:
            self.current.symtab[node.location.id] = expr
        else :
            self.current.add(node.location.id, expr)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.then_b)
        if node.else_b:
            self.visit(node.else_b)
 
    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ForStatement(self,node):
        self.visit(node.condition1)
        self.visit(node.condition2)
        self.visit(node.condition3)
        self.visit(node.body)


    def visit_ReturnStatement(self,node):
        self.visit(node.value)


    def visit_ExprList(self, node):
        for expresssion in node.expressions:
            print str(self.visit(expression))

        

# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA DE LO DE ABAJO
# ----------------------------------------------------------------------
 
def check_program(node):
    '''
    Comprueba el programa suministrado (en forma de un AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(node)
