# -*- coding: utf-8 -*-
import re
import os

class Calc:
	version = 1.2
	pattern_start = r'^([0-9\+\*/\^(\sroot\s)\(\)\.-]+)$'
	pattern_result = r'^([0-9]+)(\.[0-9]+)?$'
	pattern1 = r'([0-9]+(\.[0-9]+)?)[\*/]([0-9]+(\.[0-9]+)?)'
	pattern2 = r'([0-9]+(\.[0-9]+)?)[\+-]([0-9]+(\.[0-9]+)?)'
	pattern3 = r'([0-9]+(\.[0-9]+)?)(\^|\sroot\s)([0-9]+(\.[0-9]+)?)'
	pattern4 = r'\(((?![\(\)]).)+\)'
	accuracy = 2 # Set default accuracy
	
	def __init__(self):
		self.read_settings()
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
					print(command+" =")
					self.analysis(command)
				else:
					print(u"Użyto niedozwolonych znaków")
		
	def calculate(self, command):
		calculation1 = re.search(self.pattern1, command)
		calculation2 = re.search(self.pattern2, command)
		calculation3 = re.search(self.pattern3, command)
		if calculation3:
			calculation = calculation3.group()
			symbol = calculation.find('^')
			if symbol != -1:
				elements = map(float, calculation.split('^'))
				result2 = elements[0]**elements[1]
			else:
				symbol = calculation.find(' root ')
				if symbol != -1:
					elements = map(float, calculation.split(' root '))
					result2 = round(elements[1]**(1/float(elements[0])), 2)
				else:
					print(u"Błąd: niezindentyfikowane działanie")
			return calculation, result2
		elif calculation1:
			calculation = calculation1.group()
			symbol = calculation.find('*')
			if symbol != -1:
				elements = map(float, calculation.split('*'))
				result2 = elements[0]*elements[1]
			else:
				symbol = calculation.find('/')
				if symbol != -1:
					elements = map(float, calculation.split('/'))
					if elements[1] != 0:
						result2 = elements[0]/elements[1]
					else:
						print(u"Nie można dzielić przez 0")
				else:
					print(u"Błąd: niezindentyfikowane działanie")
			return calculation, result2
		elif calculation2:
			calculation = calculation2.group()
			symbol = calculation.find('+')
			if symbol != -1:
				elements = map(float, calculation.split('+'))
				result2 = elements[0]+elements[1]
			else:
				symbol = calculation.find('-')
				if symbol != -1:
					elements = map(float, calculation.split('-'))
					result2 = elements[0]-elements[1]
				else:
					print(u"Błąd: niezindentyfikowane działanie")
			return calculation, result2
		else:
			print(u"Niepoprawne działanie")
		
	def analysis(self, command):
		calculation = re.search(self.pattern4, command)
		if calculation:
			calculation = calculation.group()
			calculation.replace('(', '').replace(')', '')
			calculation2, result = self.calculate(calculation)
			if result:
				command = command.replace(calculation, str(result))
				if re.search(self.pattern_result, command) == None:
					print(command+" =")
					self.analysis(command)
				else:
					self.print_result(command)
		else:
			calculation2, result = self.calculate(command)
			if result:
				command = command.replace(calculation2, str(result))
				if re.search(self.pattern_result, command) == None:
					print(command+" =")
					self.analysis(command)
				else:
					self.print_result(command)
	
	def Clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
			
	def read_settings(self):
		if os.path.isfile('config.dat'):
			config = open("config.dat", "r")
			self.accuracy = int(config.readline().split(': ')[1])
		else:
			print(u"Nie znaleziono pliku ustawień")
			
	def print_result(self, result):
		result = float(result)
		if result.is_integer():
			print(str(int(result)))
		else:
			print(str(round(result, self.accuracy)))
			
kalkulator = Calc()