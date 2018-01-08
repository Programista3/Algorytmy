# -*- coding: utf-8 -*-
import re
import os
import math
import tkinter.scrolledtext as tkst
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

class Calc:
	version = '2.1'
	pattern_start = r'^([a-z0-9\+\*/\^(\sroot\s)\(\)\.-]+)$'
	pattern_result = r'^[-]?[0-9]+(\.[0-9]+)?$'
	pattern1 = r'[-]?[0-9]+(\.[0-9]+)?[\*/][-]?[0-9]+(\.[0-9]+)?'
	pattern2 = r'[-]?[0-9]+(\.[0-9]+)?[+-][-]?[0-9]+(\.[0-9]+)?'
	pattern3 = r'[-]?[0-9]+(\.[0-9]+)?(\^|root)[-]?[0-9]+(\.[0-9]+)?'
	pattern4 = r'\(((?![\(\)]).)+\)'
	accuracy = 6 # Set default accuracy
	constants = {'pi':math.pi, 'fi':(1_5**0.5)/2, 'e':math.e}
	history = []
	history_pos = 0
	
	def __init__(self):
		self.set_win = False
		self.read_settings()
		self.start_gui()
		
	def btnClick(self, e=None):
		self.warning['text'] = ""
		command = self.textbox.get()
		if len(command) > 1:
			if re.search(self.pattern_start, command):
				self.textarea.delete(1.0, END)
				self.textarea.insert(END, command)
				if len(self.history) >= 10:
					del self.history[0]
				self.history.append(command)
				self.analysis(command)
			else:
				self.warning['text'] = "Użyto niedozwolonych znaków"
		else:
			self.warning['text'] = "Wpisz działanie!"

	def clearText(self):
		self.textbox.delete(0, END)
		self.textarea.delete(1.0, END)		
	
	def clearTextbox(self, e=None):
		self.textbox.delete(0, END)
	
	def showInfo(self):
		messagebox.showinfo("Kalkulator - informacje", "Kalkulator v."+self.version+"\nGrzegorz Babiarz 2017-2018\nGNU General Public License v3.0\nhttps://github.com/Programista3/Algorytmy/tree/master/Python/kalkulator")

	def quit(self):
		self.root.destroy()

	def historyKey(self, e):
		if e.keysym == "Up":
			if self.history_pos < 9:
				self.history_pos += 1
			self.textbox.delete(0, END)
			self.textbox.insert(0, self.history[len(self.history)-self.history_pos-1])
		elif e.keysym == "Down":
			if self.history_pos > 0:
				self.history_pos -= 1
			self.textbox.delete(0, END)
			self.textbox.insert(0, self.history[len(self.history)-self.history_pos-1])

	def start_gui(self):
		self.root = Tk()
		self.root.geometry('{}x{}'.format(550, 250))
		self.root.title("Kalkulator")
		menu = Menu(self.root)
		options = Menu(menu)
		options.add_command(label="Ustawienia", command=self.settings)
		options.add_command(label="Informacje", command=self.showInfo)
		options.add_command(label="Wyjście", command=self.quit)
		menu.add_cascade(label="Opcje", menu=options)
		self.textbox = ttk.Entry(self.root, width=85)
		self.textbox.bind("<Return>", self.btnClick)
		self.textbox.bind("<Delete>", self.clearTextbox)
		self.textbox.bind("<Up>", self.historyKey)
		self.textbox.bind("<Down>", self.historyKey)
		self.textbox.pack(pady=10)
		self.textarea = tkst.ScrolledText(self.root, width=62, height=9)
		self.textarea.pack()
		self.warning = ttk.Label(self.root, text="")
		self.warning.pack()
		bottom = Frame(self.root)
		bottom.pack()
		clear = ttk.Button(self.root, command=self.clearText, text="Wyczyść")
		clear.pack(in_=bottom, side=LEFT)
		button = ttk.Button(self.root, command=self.btnClick, text='Oblicz')
		button.pack(in_=bottom, padx=4, pady=4)
		self.root.config(menu=menu)
		self.root.resizable(0,0)
		self.root.mainloop()

	def calculate(self, command):
		calculation1 = re.search(self.pattern1, command)
		calculation2 = re.search(self.pattern2, command)
		calculation3 = re.search(self.pattern3, command)
		if calculation3:
			calculation = calculation3.group().replace(" ", "")
			symbol = calculation.find('^')
			if symbol != -1:
				elements = list(map(float, calculation.split('^')))
				result2 = elements[0]**elements[1]
			else:
				symbol = calculation.find('root')
				if symbol != -1:
					elements = list(map(float, calculation.split('root')))
					if elements[1] < 0:
						if elements[0]%2 == 0:
							self.warning['text'] = "Nie można obliczyć pierwiastka stopnia parzystego z liczby ujemnej!"
							return False, False
						else:
							result2 = -(round((-elements[1])**(1/float(elements[0])), self.accuracy))
					else:
						result2 = round(elements[1]**(1/float(elements[0])), self.accuracy)
				else:
					self.warning['text'] = "Błąd: niezindentyfikowane działanie"
					return False, False
			return calculation, result2
		elif calculation1:
			calculation = calculation1.group()
			symbol = calculation.find('*')
			if symbol != -1:
				elements = list(map(float, calculation.split('*')))
				result2 = elements[0]*elements[1]
			else:
				symbol = calculation.find('/')
				if symbol != -1:
					elements = list(map(float, calculation.split('/')))
					if elements[1] != 0:
						result2 = elements[0]/elements[1]
					else:
						self.warning['text'] = "Nie można dzielić przez 0"
						return False, False
				else:
					self.warning['text'] = "Błąd: niezindentyfikowane działanie"
					return False, False
			return calculation, result2
		elif calculation2:
			calculation = calculation2.group()
			symbol = calculation.find('+')
			if symbol != -1:
				elements = list(map(float, calculation.split('+')))
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
					self.warning['text'] = "Błąd: niezindentyfikowane działanie"
					return False, False
				elements = [float(calculation[:minus[index]]), float(calculation[minus[index]+1:])]
				result2 = elements[0]-elements[1]
			return calculation, result2
		else:
			self.warning['text'] = "Niepoprawne działanie"
			return False, False
		
	def analysis(self, command):
		command = command.replace(" ", "")
		for key, val in self.constants.items():
			command = command.replace(key, str(round(val, self.accuracy)))
		calculation = re.search(self.pattern4, command)
		if calculation:
			calculation = calculation.group()
			calculation.replace('(', '').replace(')', '')
			calculation2, result = self.calculate(calculation)
			if calculation2 != False:
				command = command.replace(calculation, str(self.format_result(result)))
				if re.search(self.pattern_result, command) == None:
					self.textarea.insert(END, "="+command)
					self.analysis(command)
				else:
					self.textbox.delete()
					self.textbox.insert(0, command)
					self.textarea.insert(END, "="+command)
			else:
				self.textarea.delete(1.0, END)
		else:
			calculation2, result = self.calculate(command)
			if calculation2 != False:
				command = command.replace(calculation2, str(self.format_result(result)))
				if re.search(self.pattern_result, command) == None:
					self.textarea.insert(END, "="+command)
					self.analysis(command)
				else:
					self.textbox.delete(0, END)
					self.textbox.insert(0, command)
					self.textarea.insert(END, "="+command)
			else:
				self.textarea.delete(1.0, END)
			
	def read_settings(self):
		if os.path.isfile('config.dat'):
			config = open("config.dat", "r").read()
			ac_pattern = r'accuracy: [0-9]+'
			search = re.search(ac_pattern, config)
			if search:
				accuracy = int(search.group().split(': ')[1])
				if accuracy >= 0 and accuracy <= 10:
					self.accuracy = accuracy
			
	def format_result(self, number):
		number = float(number)
		if number.is_integer():
			return int(number)
		else:
			return round(number, self.accuracy)
	
	def close(self):
		self.window.destroy()
		self.set_win = False

	def save_settings(self):
		ac_pattern = r'accuracy: [0-9]+'
		config_text = self.configText.get(1.0, END).strip()
		search = re.search(ac_pattern, config_text)
		if search:
			accuracy = int(search.group().split(': ')[1])
			if accuracy >= 0 and accuracy <= 10:
				self.accuracy = accuracy
				if os.path.isfile("config.dat"):
					config = open("config.dat", "w")
					config.write(config_text)
				else:
					config = open("config.dat", "w+")
					config.write(config_text)
				messagebox.showinfo("Zapisywanie ustawień", "Zmiany zostały zapisane")
				config.close()
			else:
				messagebox.showinfo("Błąd", "Dokładność nie może być większa niż 10")

	def settings(self):
		if not self.set_win:
			self.set_win = True
			self.window = Toplevel()
			self.window.geometry("400x300")
			self.window.wm_title("Zmień ustawienia")
			self.configText = tkst.ScrolledText(self.window, width=50, height=16)
			self.configText.pack()
			if os.path.isfile("config.dat"):
				config = open("config.dat", "r")
				self.configText.insert(END, config.read())
			else:
				config = open("config.dat", "w+")
				text = "accuracy: "+str(self.accuracy)
				config.write(text)
				self.configText.insert(END, text)
			config.close()
			frame = ttk.Frame(self.window)
			frame.pack(pady=6)
			btn = ttk.Button(self.window, text="Zapisz", command=self.save_settings)
			btn.pack(in_=frame, side=LEFT)
			exit = ttk.Button(self.window, text="Zamknij", command=self.close)
			exit.pack(in_=frame)
			self.window.resizable(0,0)
			self.window.protocol("WM_DELETE_WINDOW", self.close)
			
kalkulator = Calc()