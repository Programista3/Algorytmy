# -*- coding: utf-8 -*-
import re
import os

class Calc:
	version = 1.0
	pattern_start = r'^([0-9\+\*/-]+)$'
	pattern_result = r'^([0-9]+)$'
	pattern1 = r'([0-9]+)[\*/]([0-9]+)'
	pattern2 = r'([0-9+])[\+-]([0-9]+)'
	
	def __init__(self):
		self.start()
		
	def start(self):
		while True:
			command = raw_input('Calc: ')
			if command == 'exit':
				break
			elif command == 'clear':
				self.Clear()
			else:
				if re.search(self.pattern_start, command):
					self.analysis(command)
				else:
					print(u"Użyto niedozwolonych znaków")
		
	def analysis(self, command):
		calculation1 = re.search(self.pattern1, command)
		calculation2 = re.search(self.pattern2, command)
		if calculation1:
			calculation = calculation1.group()
			symbol = calculation.find('*')
			if symbol != -1:
				elements = map(int, calculation.split('*'))
				result2 = elements[0]*elements[1]
			else:
				symbol = calculation.find('/')
				if symbol != -1:
					elements = map(int, calculation.split('/'))
					if elements[1] != 0:
						result2 = elements[0]/elements[1]
					else:
						print(u"Nie można dzielić przez 0")
				else:
					print(u"Błąd: niezindentyfikowane działanie")
			command = command.replace(calculation, str(result2))
			print(command)
			if re.search(self.pattern_result, command) == None:
				self.analysis(command)
		elif calculation2:
			calculation = calculation2.group()
			symbol = calculation.find('+')
			if symbol != -1:
				elements = map(int, calculation.split('+'))
				result2 = elements[0]+elements[1]
			else:
				symbol = calculation.find('-')
				if symbol != -1:
					elements = map(int, calculation.split('-'))
					result2 = elements[0]-elements[1]
				else:
					print(u"Błąd: niezindentyfikowane działanie")
			command = command.replace(calculation, str(result2))
			print(command)
			if re.search(self.pattern_result, command) == None:
				self.analysis(command)
		else:
			print(u"Niepoprawne działanie")
	
	def Clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
	
kalkulator = Calc()