# -*- coding: utf-8 -*-
import re
import os

class Calc:
	version = '1.3'
	pattern_start = r'^([0-9\+\*/\^(\sroot\s)\(\)\.-]+)$'
	pattern_result = r'^[+-]?[0-9]+(\.[0-9]+)?$'
	pattern1 = r'[+-]?[0-9]+(\.[0-9]+)?[\*/][+-]?[0-9]+(\.[0-9]+)?'
	pattern2 = r'[+-]?[0-9]+(\.[0-9]+)?[+-][+-]?[0-9]+(\.[0-9]+)?'
	pattern3 = r'[+-]?[0-9]+(\.[0-9]+)?(\^|root)[+-]?[0-9]+(\.[0-9]+)?'
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
				self.clear()
			elif command == 'settings':
				self.settings()
			else:
				if re.search(self.pattern_start, command):
					self.analysis(command)
				else:
					print(u"Użyto niedozwolonych znaków")
		
	def calculate(self, command):
		calculation1 = re.search(self.pattern1, command)
		calculation2 = re.search(self.pattern2, command)
		calculation3 = re.search(self.pattern3, command)
		if calculation3:
			calculation = calculation3.group().replace(" ", "")
			symbol = calculation.find('^')
			if symbol != -1:
				elements = map(float, calculation.split('^'))
				result2 = elements[0]**elements[1]
			else:
				symbol = calculation.find('root')
				if symbol != -1:
					elements = map(float, calculation.split('root'))
					if elements[1] < 0:
						if elements[0]%2 == 0:
							print(u"Nie można obliczyć pierwiastka stopnia parzystego z liczby ujemnej!")
							return False, False
						else:
							result2 = -(round((-elements[1])**(1/float(elements[0])), 2))
					else:
						result2 = round(elements[1]**(1/float(elements[0])), 2)
				else:
					print(u"Błąd: niezindentyfikowane działanie")
					return False, False
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
						return False, False
				else:
					print(u"Błąd: niezindentyfikowane działanie")
					return False, False
			return calculation, result2
		elif calculation2:
			calculation = calculation2.group()
			symbol = calculation.find('+')
			if symbol != -1:
				elements = map(float, calculation.split('+'))
				result2 = elements[0]+elements[1]
			else:
				count = calculation.count('-')
				minus = [result.start() for result in re.finditer('-', calculation)]
				if count == 3:
					index = 1
				elif count == 2:
					if calculation[0] == '-':
						index = 1
					else:
						index = 0
				elif count == 1:
					index = 0
				else:
					print(u"Błąd: niezindentyfikowane działanie")
					return False, False
				elements = [float(calculation[:minus[index]]), float(calculation[len(calculation)-minus[index]:])]
				result2 = elements[0]-elements[1]
			return calculation, result2
		else:
			print(u"Niepoprawne działanie")
			return False, False
		
	def analysis(self, command):
		command = command.replace(" ", "")
		calculation = re.search(self.pattern4, command)
		if calculation:
			calculation = calculation.group()
			calculation.replace('(', '').replace(')', '')
			calculation2, result = self.calculate(calculation)
			if calculation2 != False:
				command = command.replace(calculation, str(result))
				if re.search(self.pattern_result, command) == None:
					print(command+" =")
					self.analysis(command)
				else:
					self.print_result(command)
		else:
			calculation2, result = self.calculate(command)
			if calculation2 != False:
				command = command.replace(calculation2, str(result))
				if re.search(self.pattern_result, command) == None:
					print(command+" =")
					self.analysis(command)
				else:
					self.print_result(command)
	
	def clear(self):
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
	
	def settings(self):
		self.clear()
		self.read_settings()
		print(u"Wpisz nową wartość parametru lub pozostaw puste miejsce aby zachować aktualny wartość")
		print(u"Dokładność("+str(self.accuracy)+"):"),
		accuracy = raw_input()
		if accuracy != "" and accuracy != self.accuracy:
			if os.path.isfile('config.dat'):
				config = open('config.dat', 'w')
				config.truncate()
				config.write('accuracy: '+str(accuracy))
				config.close()
				self.accuracy = accuracy
				print(u"Zmiany zostały zapisane")
			else:
				print(u"Nie znaleziono pliku ustawień")
		else:
			print(u"Zmiany zostały zapisane")
			
kalkulator = Calc()