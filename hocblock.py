# -*- coding: utf-8 -*-
class BasicBlock():

	def __init__(self):
		self.block = []
		self.next_block = None

	def append(self, data):
		self.block.append(data)

class WhileBlock():

	def __init__(self):
		self.block = []
		self.next_block = None

	def append(self, data):
		self.block.append(data)

class IfBlock():

	def __init__(self):
		self.block = []
		self.truebranch = None
		self.falsebranch = None

	def append(self, data):
		self.block.append(data)