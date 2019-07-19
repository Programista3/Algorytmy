# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import re
import os
import math
from configparser import ConfigParser
import urllib.request as urllib
import json
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import threading
import webbrowser
from decimal import *
import lang
_ = lang.get

lang.add("locales/pl.xml")
lang.add("locales/en.xml")
lang.select("pl")

class Stack:
	def __init__(self):
		self.stack = []
	
	def push(self, item):
		self.stack.append(item)

	def pop(self):
		self.stack.pop(len(self.stack)-1)

	def top(self):
		return self.stack[len(self.stack)-1]

	def size(self):
		return len(self.stack)

	def get(self):
		return self.stack[::-1]

class Tools:
	def isNumber(self, str):
		if(str.isdigit()):
			return 1
		else:
			try:
				float(str)
				return 2
			except ValueError:
				return 0
	
	def normalizeFraction(self, d):
		normalized = d.normalize()
		sign, digit, exponent = normalized.as_tuple()
		return normalized if exponent <= 0 else normalized.quantize(1)

class StandardWindow:
	def create(self, root, title, text, units1, units2):
		self.window = Toplevel(root)
		self.window.resizable(False, False)
		self.window.title(title)
		self.window.iconbitmap('pycalc.ico')
		self.frame = ttk.Frame(self.window)
		self.labels = []
		for i in range(4):
			self.labels.append(ttk.Label(self.frame, text=text[i]))
		self.value = ttk.Entry(self.frame, width=22)
		self.inCBox = ttk.Combobox(self.frame, values=units1, width=19)
		self.inCBox.current(0)
		self.outCBox = ttk.Combobox(self.frame, values=units2, width=19)
		self.outCBox.current(1)
		self.result = ttk.Label(self.frame)
		self.submit = ttk.Button(self.frame, text=_("calculate"))

	def bind(self, function, *args):
		if(len(args) >= 3):
			self.submit.configure(command=lambda: function(args[0](), args[1](), args[2]()))
			self.value.bind("<Return>", lambda event: function(args[0](), args[1](), args[2]()))
			self.inCBox.bind("<Return>", lambda event: function(args[0](), args[1](), args[2]()))
			self.outCBox.bind("<Return>", lambda event: function(args[0](), args[1](), args[2]()))
		else:
			self.submit.configure(command=lambda: function(self.value.get(), self.inCBox.current(), self.outCBox.current()))
			self.value.bind("<Return>", lambda event: function(self.value.get(), self.inCBox.current(), self.outCBox.current()))
			self.inCBox.bind("<Return>", lambda event: function(self.value.get(), self.inCBox.current(), self.outCBox.current()))
			self.outCBox.bind("<Return>", lambda event: function(self.value.get(), self.inCBox.current(), self.outCBox.current()))


	def grid(self):
		self.frame.grid(row=0, column=0, rowspan=5, columnspan=2, padx=20, pady=20)
		for i in range(4):
			self.labels[i].grid(row=i, column=0, pady=5, padx=8)
		self.value.grid(row=0, column=1, padx=20)
		self.inCBox.grid(row=1, column=1)
		self.outCBox.grid(row=2, column=1)
		self.result.grid(row=3, column=1)
		self.submit.grid(row=4, column=0, columnspan=2, pady=(10,0))

class ImageViewer:
	def __init__(self, root, title, image):
		if(os.path.isfile(image)):
			self.window = Toplevel(root)
			self.window.resizable(False, False)
			self.window.title(title)
			self.window.iconbitmap('pycalc.ico')
			self.file = Image.open(image)
			self.image = ImageTk.PhotoImage(self.file)
			self.label = Label(self.window, image=self.image)
			self.label.image = self.image
			self.label.pack()
		else:
			messagebox.showerror(_("error"), _("err3"))

class LengthCalculator(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("millimeters"),_("centimeters"),_("decimeters"),_("meters"),_("kilometers"),_("inches"),_("foots"),_("yards"),_("miles"),_("nautical miles")]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.values = [Decimal(str(i)) for i in [0.001, 0.01, 0.1, 1, 1000, 0.0254, 0.3048, 0.9144, 1609.344, 1852]]
		self.create(root, _("menu1.5"), text, units, units)
		self.bind(self.convertLength)
		self.grid()

	def convertLength(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(value)
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class TemperatureCalculator(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("celsius"),_("fahrenheit"),_("kelvin")]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.4"), text, units, units)
		self.bind(self.convertTemperature)
		self.grid()

	def convertTemperature(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(value)
			if(unitIn != unitOut):
				if(unitIn == 1):
					value = Decimal('5')/9*(value-32)
				elif(unitIn == 2):
					value -= Decimal('273.15')
				if(unitOut == 1):
					value = 32+Decimal('9')/5*value
				elif(unitOut == 2):
					value += Decimal('273.15')
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class NumberSystemCalculator(StandardWindow):
	def __init__(self, root):
		text = [_("number"),_("inputSystem"),_("targetSystem"),_("result")]
		systems = [_("2ns"),_("8ns"),_("10ns"),_("16ns")]
		self.create(root, _("menu1.3"), text, systems, systems)
		self.bind(self.convertNumberSystem)
		self.grid()
	
	def convertNumberSystem(self, number, systemIn, systemOut):
		if(systemIn == 0):
			if(re.match(r'^[01]+$', number)):
				number = int(number,2)
			else:
				messagebox.showerror(_("error"), _("err2"))
				return
		elif(systemIn == 1):
			if(re.match(r'^[0-7]+$', number)):
				number = int(number,8)
			else:
				messagebox.showerror(_("error"), _("err2"))
				return
		elif(systemIn == 2):
			if(re.match(r'^[0-9]+$', number)):
				number = int(number)
			else:
				messagebox.showerror(_("error"), _("err2"))
				return
		elif(systemIn == 3):
			if(re.match(r'^[0-9a-fA-F]+$', number)):
				number = int(number,16)
			else:
				messagebox.showerror(_("error"), _("err2"))
				return
		if(systemOut == 0):
			self.result['text'] = str(bin(number))[2:]
		elif(systemOut == 1):
			self.result['text'] = str(oct(number))[2:]
		elif(systemOut == 2):
			self.result['text'] = str(number)
		elif(systemOut == 3):
			self.result['text'] = str(hex(number))[2:]

class TrigonometricFunctions(StandardWindow, Tools):
	def __init__(self, root):
		text = [_("function"),_("value"),_("unit"),_("result")]
		functions = ['sin','cos','tg','ctg']
		units = [_("degree"),_("radian")]
		self.create(root, _("menu1.2"), text, functions, units)
		self.bind(self.calcTrigonometricFunc, self.value.get, self.inCBox.get, self.outCBox.current)
		self.grid()

	def calcTrigonometricFunc(self, value, function, unit):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(value)
			if(unit == 0):
				value = math.radians(value)
			if(function == 'sin'):
				value = math.sin(value)
			elif(function == 'cos'):
				value = math.cos(value)
			elif(function == 'tg'):
				value = math.tan(value)
			elif(function == 'ctg'):
				value = 1/math.tan(value)
			self.result['text'] = str(round(value,10))
		else:
			messagebox.showerror(_("error"), _("err2"))

class ScreenSizeCalculator(Tools):
	def __init__(self, root):
		self.root = root
		self.ssActiveEntry = None
		self.create()
		self.bind()
		self.grid()

	def create(self):
		ratio = ['16:9','16:10','4:3','3:2','5:4','21:9','2:1']
		text = [_('ratio'), _('diagonal'), _('width'), _('height')]
		self.window = Toplevel(self.root)
		self.window.resizable(False, False)
		self.window.title(_("menu1.1"))
		self.window.iconbitmap('pycalc.ico')
		self.frame = ttk.Frame(self.window)
		self.frame.focus_set()
		self.ratioCBox = ttk.Combobox(self.frame, values=ratio, width=12)
		self.ratioCBox.current(0)
		self.label = []
		self.entry = []
		for i in range(4):
			self.label.append(ttk.Label(self.frame, text=text[i]))
		for i in range(1,4):
			self.entry.append(ttk.Entry(self.frame, width=6))
		for i in range(4,7):
			self.label.append(ttk.Label(self.frame, text=_("inch")))
		for i in range(3,6):
			self.entry.append(ttk.Entry(self.frame, width=6))
		for i in range(7,10):
			self.label.append(ttk.Label(self.frame, text="cm"))
		self.submit = ttk.Button(self.frame, text=_("calculate"), command=lambda: self.calcScreenSize(self.ssActiveEntry))
		self.reset = ttk.Button(self.frame, text=_("clear"), command=self.clearScreenSizeForm)

	def bind(self):
		self.frame.bind("<Button>", lambda event: self.calcScreenSize(self.ssActiveEntry))
		for i in range(3):
			self.entry[i].bind("<FocusIn>", lambda event, index=i: self.screenSizeActiveEntry(index))
			self.entry[i].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
			self.entry[i].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))
		for i in range(3,6):
			self.entry[i].bind("<FocusIn>", lambda event, index=i: self.screenSizeActiveEntry(index))
			self.entry[i].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
			self.entry[i].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))

	def grid(self):
		self.frame.grid(row=0, column=0, rowspan=3, columnspan=5, padx=30, pady=20)
		self.ratioCBox.grid(row=0, column=1, columnspan=4)
		for i in range(4):
			self.label[i].grid(row=i, column=0, pady=5)
		for i in range(3):
			self.entry[i].grid(row=i+1, column=1, padx=(10, 0))
		for i in range(4,7):
			self.label[i].grid(row=i-3, column=2)
		for i in range(3,6):
			self.entry[i].grid(row=i-2, column=3, padx=(10,0))
		for i in range(7,10):
			self.label[i].grid(row=i-6, column=4)
		self.submit.grid(row=4, column=0, columnspan=2, pady=(10,0))
		self.reset.grid(row=4, column=2, columnspan=2, pady=(10,0))

	def calcScreenSizeDiagonal(self, diagonal, ratio):
		result = ((ratio[0]**2+ratio[1]**2)**Decimal(0.5))/diagonal
		return (round(ratio[0]/result,2), round(ratio[1]/result,2))

	def calcScreenSizeWidth(self, width, ratio):
		height = round(width*ratio[1]/ratio[0],2)
		diagonal = round((width**2+height**2)**Decimal(0.5),2)
		return (height, diagonal)

	def calcScreenSizeHeight(self, height, ratio):
		width = round(height*ratio[0]/ratio[1],2)
		diagonal = round((width**2+height**2)**Decimal(0.5),2)
		return (width, diagonal)

	def clearScreenSizeForm(self):
		for i in range(0,6):
			self.entry[i].delete(0, END)   

	def calcScreenSize(self, index):
		if(index != None):
			ratio = list(map(Decimal, self.ratioCBox.get().split(':')))
			if(index == 0):
				if(self.isNumber(self.entry[0].get())):
					result = self.calcScreenSizeDiagonal(Decimal(self.entry[0].get()), ratio)
					for i in range(1,6):
						self.entry[i].delete(0, END)
					self.entry[1].insert(0, result[0])
					self.entry[2].insert(0, result[1])
					self.entry[3].insert(0, round(Decimal(self.entry[0].get())*Decimal(2.54),2))
					self.entry[4].insert(0, round(result[0]*Decimal(2.54),2))
					self.entry[5].insert(0, round(result[1]*Decimal(2.54),2))
			elif(index == 1):
				if(self.isNumber(self.entry[1].get())):
					result = self.calcScreenSizeWidth(Decimal(self.entry[1].get()), ratio)
					for i in [0,2,3,4,5]:
						self.entry[i].delete(0, END)
					self.entry[0].insert(0, result[1])
					self.entry[2].insert(0, result[0])
					self.entry[3].insert(0, round(result[1]*Decimal(2.54),2))
					self.entry[4].insert(0, round(Decimal(self.entry[1].get())*Decimal(2.54),2))
					self.entry[5].insert(0, round(result[0]*Decimal(2.54),2))
			elif(index == 2):
				if(self.isNumber(self.entry[2].get())):
					result = self.calcScreenSizeHeight(Decimal(self.entry[2].get()), ratio)
					for i in [0,1,3,4,5]:
						self.entry[i].delete(0, END)
					self.entry[0].insert(0, result[1])
					self.entry[1].insert(0, result[0])
					self.entry[3].insert(0, round(result[1]*Decimal(2.54),2))
					self.entry[4].insert(0, round(result[0]*Decimal(2.54),2))
					self.entry[5].insert(0, round(Decimal(self.entry[2].get())*Decimal(2.54),2))
			elif(index == 3):
				if(self.isNumber(self.entry[3].get())):
					result = self.calcScreenSizeDiagonal(Decimal(self.entry[3].get()), ratio)
					for i in [0,1,2,4,5]:
						self.entry[i].delete(0, END)
					self.entry[0].insert(0, round(Decimal(self.entry[3].get())/Decimal(2.54),2))
					self.entry[1].insert(0, round(result[0]/Decimal(2.54),2))
					self.entry[2].insert(0, round(result[1]/Decimal(2.54),2))
					self.entry[4].insert(0, round(result[0],2))
					self.entry[5].insert(0, round(result[1],2))
			elif(index == 4):
				if(self.isNumber(self.entry[4].get())):
					result = self.calcScreenSizeWidth(Decimal(self.entry[4].get()), ratio)
					for i in [0,1,2,3,5]:
						self.entry[i].delete(0, END)
					self.entry[0].insert(0, round(result[1]/Decimal(2.54),2))
					self.entry[1].insert(0, round(Decimal(self.entry[4].get())/Decimal(2.54),2))
					self.entry[2].insert(0, round(result[0]/Decimal(2.54),2))
					self.entry[3].insert(0, result[1])
					self.entry[5].insert(0, result[0])
			elif(index == 5):
				if(self.isNumber(self.entry[5].get())):
					result = self.calcScreenSizeHeight(Decimal(self.entry[5].get()), ratio)
					for i in [0,1,2,3,4]:
						self.entry[i].delete(0, END)
					self.entry[0].insert(0, round(result[1]/Decimal(2.54),2))
					self.entry[1].insert(0, round(result[0]/Decimal(2.54),2))
					self.entry[2].insert(0, round(Decimal(self.entry[5].get())/Decimal(2.54),2))
					self.entry[3].insert(0, result[1])
					self.entry[4].insert(0, result[0])

	def screenSizeActiveEntry(self, index):
		self.ssActiveEntry = index

class CurrencyConverter(StandardWindow):
	def __init__(self, root):
		currencies = ["AED","AFN","ALL","AMD","ANG","AQA","ARS","AUD","AWG","AZN","BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BRL","BSD","BTC","BTN","BWP","BYN","BZD","CAD","CDF","CHF","CLF","CLP","CNH","CNY","COP","CRC","CUC","CUP","CVE","CZK","DJF","DKK","DOP","DZD","EGP","ERN","ETB","EUR","FJD","FKP","GBP","GEL","GGP","GHS","GIP","GMD","GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS","IMP","INR","IQD","IRR","ISK","JEP","JMD","JOD","JPY","KES","KGS","KHR","KMF","KPW","KRW","KWD","KYD","KZT","LAK","LBP","LKR","LRD","LSL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRO","MRU","MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO","NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN","PYG","QAR","RON","RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLL","SOS","SRD","SSP","STD","STN","SVC","SYP","SZL","THB","TJS","TMT","TND","TOP","TRY","TTD","TWD","TZS","UAH","UGX","USD","UYU","UZS","VEF","VES","VND","VUV","WST","XAF","XAG","XAU","XCD","XDR","XOF","XPD","XPF","XPT","YER","ZAR","ZMW","ZWL"]
		text = [_("value"),_("currency"),_("targetCurrency"),_("result")]
		self.create(root, _("menu1.6"), text, currencies, currencies)
		self.status = ttk.Label(self.window)
		self.bind(self.convertCurrency, self.value.get, self.inCBox.get, self.outCBox.get)
		self.grid()
		self.status.grid(row=6, column=0, sticky=W)

	def convertCurrency(self, value, currencyIn, currencyOut):
		self.status["text"] = _("status01")
		self.submit.config(state=DISABLED)
		self.status.update_idletasks()
		with urllib.urlopen("http://currencyconverterfree.000webhostapp.com/api/convert?from="+currencyIn+"&to="+currencyOut+"&value="+value) as url:
			data = json.loads(url.read().decode())
			self.result["text"] = data['value']
			self.status["text"] = _("status02")
			self.submit.config(state=NORMAL)

class TimeConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("nanoseconds"),_("microseconds"),_("milliseconds"),_("seconds"),_("minutes"),_("hours"),_("days"),_("weeks"),_("months"),_("years")]
		self.values = [Decimal(str(i)) for i in [0.000000001, 0.000001, 0.001, 1, 60, 3600, 86400, 604800, 2592000, 31536000]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.7"), text, units, units)
		self.bind(self.convertTime)
		self.grid()

	def convertTime(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class SpeedConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("mm/s"),_("cm/s"),_("m/s"),_("km/s"),_("mm/min"),_("cm/min"),_("m/min"),_("km/min"),_("mm/h"),_("cm/h"),_("m/h"),_("km/h"),_("ft/s"),_("ft/min"),_("ft/h"),_("yd/s"),_("yd/min"),_("yd/h"),_("mi/s"),_("mi/min"),_("kn"),_("mach")]
		self.values = [Decimal(str(i)) for i in [0.001, 0.01, 1, 1000, 1.66667E-5, 0.0001666667, 0.0166666667, 16.6666666667, 2.7777777777778E-7, 2.7777777777778E-6, 0.0002777778, 0.2777777778, 0.3048, 0.00508, 8.46667E-5, 0.9144, 0.01524, 0.000254, 1609.344, 26.8224, 0.5144444444, 295.0464000003]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.8"), text, units, units)
		self.bind(self.convertSpeed)
		self.grid()

	def convertSpeed(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class AreaConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("mm^2"),_("cm^2"),_("in^2"),_("dm^2"),_("ft^2"),_("yd^2"),_("m^2"),_("km^2"),_("a"),_("ac"),_("ha"),_("mile^2")]
		self.values = [Decimal(str(i)) for i in [0.000001, 0.0001, 0.00064516, 0.01, 0.09290304, 0.83612736, 1, 1000000, 100, 4046.8564224, 10000, 2589988.110336]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.9"), text, units, units)
		self.bind(self.convertArea)
		self.grid()

	def convertArea(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class EnergyConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("GJ"),_("MJ"),_("kJ"),_("j"),_("cal"),_("kcal"),_("kWh"),_("Btu"),_("kGm"),_("eV"),_("MT")]
		self.values = [Decimal(str(i)) for i in [1e+9, 1e+6, 1000, 1, 4.1868, 4187, 3.6e+6, 1055.06, 9.80665, 1.60218e-19, 4e+15]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.10"), text, units, units)
		self.bind(self.convertEnergy)
		self.grid()

	def convertEnergy(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class WeightAndMassConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("ct"),_("cg"),_("dag"),_("gr"),_("g"),_("cwt"),_("cwtUK"),_("kg"),_("mg"),_("oz"),_("lb"),_("stone"),_("tonUS"),_("tonUK")]
		self.values = [Decimal(str(i)) for i in [0.0002, 0.00001, 0.01, 0.00006479891, 0.001, 45.359237, 50.80234544, 1, 0.000001, 0.028349523125, 0.45359237, 6.35029318, 907.18474, 1016.0469088]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.11"), text, units, units)
		self.bind(self.convertWeightAndMass)
		self.grid()

	def convertWeightAndMass(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class DataConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("b"),_("B"),_("Kb"),_("KB"),_("Mb"),_("MB"),_("Gb"),_("GB"),_("Tb"),_("TB"),_("Pb"),_("PB"),_("Eb"),_("EB")]
		self.values = [Decimal(str(i)) for i in [0.125, 1, 125, 1000, 125000, 1000000, 125000000, 1000000000, 125000000000, 1000000000000, 125000000000000]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.12"), text, units, units)
		self.bind(self.convertData)
		self.grid()

	def convertData(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class VolumeConverter(StandardWindow, Tools):
	def __init__(self, root):
		units = [_("mm^3"),_("cm^3"),_("dm^3"),_("m^3"),_("km^3"),_("L"),_("μL"),_("mL"),_("cL"),_("dL"),_("daL"),_("hL"),_("bbl oil"),_("bblUS"),_("bblUK"),_("galUS"),_("galUK"),_("qtUS"),_("qtUK"),_("ptUS"),_("ptUK"),_("cup metric"),_("cupUS"),_("cupUK"),_("fl ozUS"),_("fl ozUK"),_("tablespoonUS"),_("tablespoonUK"),_("dessertspoonUS"),_("dessertspoonUK"),_("teaspoonUS"),_("teaspoonUK"),_("giUS"),_("giUK"),_("minimUS"),_("minimUK"),_("mi^3"),_("yd^3"),_("ft^3"),_("in^3"),_("dr")]
		self.values = [Decimal(str(i)) for i in [0.000001, 0.001, 1, 1000, 1e+12, 1, 0.000001, 0.001, 0.01, 0.1, 10, 100, 158.987294928, 119.240471196, 163.65924, 3.785411784, 4.54609, 0.946352946, 1.1365225, 0.473176473, 0.56826125, 0.25, 0.236588236, 0.284130625, 0.02957353, 0.028413063, 0.014786765, 0.017758164, 0.009857843, 0.011838776, 0.004928922, 0.005919388, 0.118294118, 0.142065312, 0.000061612, 0.000059194, 4.168181825e+12, 764.554857984, 28.316846592, 0.016387064, 0.003696691]]
		#self.values = [Decimal(str(i)) for i in [1000000, 1000, 1, 0.001, 1e-12, 1, 1000000, 1000, 100, 10, 0.1, 0.01, 0.006289811, 0.008386414, 0.006110257, 0.264172052, 0.219969248, 1.056688209, 0.879876993, 2.113376419, 1.759753986, 4, 4.226752838, 3.519507973, 33.814022702, 35.195079728, 67.628045404, 56.312127565, 101.442068106, 84.468191347, 202.884136211, 168.936382694, 8.453505675, 7.039015946, 16230.730896885, 16893.63826937, 2.399127586e-13, 0.001307951, 0.035314667, 61.023744095, 270.512181615]]
		text = [_("value"),_("unit"),_("targetUnit"),_("result")]
		self.create(root, _("menu1.13"), text, units, units)
		self.bind(self.convertVolume)
		self.grid()

	def convertVolume(self, value, unitIn, unitOut):
		value = value.replace(',','.')
		if(self.isNumber(value)):
			value = Decimal(str(value))
			value *= self.values[unitIn]
			value /= self.values[unitOut]
			self.result['text'] = self.normalizeFraction(value)
		else:
			messagebox.showerror(_("error"), _("err2"))

class pyCalc(Tools):
	def __init__(self):
		self.settingsTemplate = {
			'Personalization': {
				'language': 'pl',
				'theme': 'vista'
			},
			'Settings': {
				'resultPreview': 'true',
				'history': 'false',
				'continuityOfCalculations': 'true',
				'autoUpdate': 'true'
			}
		}
		self.version = "3.1.16"
		self.languages = ['pl','en']
		self.lang = "pl"
		self.end = False
		self.checkSettings()
		self.startGui()

	def startGui(self):
		self.root = Tk()
		self.root.title("pyCalc3")
		self.root.iconbitmap('pycalc.ico')
		self.root.resizable(False, False)
		self.style = ttk.Style()
		self.style.configure("big.TButton", padding=(-10,10,-10,10), font=('16'))
		self.btnLabels = [
			['ᵪ²','ᵪʸ','C','AC','/'],
			['√','7','8','9','*'],
			['%','4','5','6','-'],
			['‰','1','2','3','+'],
			['(',')','0','.','=']
		]
		vTheme = StringVar(value=self.style.theme_use())
		vLang = StringVar(value=self.lang)
		vShowPreview = BooleanVar(value=True)
		vShowHistory = BooleanVar(value=False)
		self.vContinuity = BooleanVar(value=True)
		vAutoUpdate = BooleanVar(value=True)

		config = ConfigParser()
		cfgpath = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc','settings.ini')
		if(os.path.isfile(cfgpath)):
			config.read(cfgpath)
			if(config['Personalization']['language'] in self.languages and config['Personalization']['theme'] in self.style.theme_names() and config['Settings']['resultPreview'] in ['true','false','True','False','0','1'] and config['Settings']['history'] in ['true','false','True','False','0','1'] and config['Settings']['continuityOfCalculations'] in ['true','false','True','False','0','1'] and config['Settings']['autoUpdate'] in ['true','false','True','False','0','1']):
				self.lang = config['Personalization']['language']
				lang.select(config['Personalization']['language'])
				vLang.set(self.lang)
				vTheme = StringVar(value=config['Personalization']['theme'])
				self.style.theme_use(config['Personalization']['theme'])
				if(config['Settings']['resultPreview'] in ['true','True','1']):
					vShowPreview.set(True)
				else:
					vShowPreview.set(False)
				if(config['Settings']['history'] in ['true','True','1']):
					vShowHistory.set(True)
				else:
					vShowHistory.set(False)
				if(config['Settings']['continuityOfCalculations'] in ['true', 'True', '1']):
					self.vContinuity.set(True)
				else:
					self.vContinuity.set(False)
				if(config['Settings']['autoUpdate'] in ['true', 'True', '1']):
					vAutoUpdate.set(True)
				else:
					vAutoUpdate.set(False)
			else:
				self.createDefaultSettingsFile()
		else:
			self.createDefaultSettingsFile()

		if(vAutoUpdate.get()):
			check = threading.Thread(target=self.checkForUpdates, args=(False,))
			check.start()

		menu = Menu(self.root)
		menuFunctions = Menu(self.root, tearoff=0)
		menuFormulas = Menu(self.root, tearoff=0)
		menuArea = Menu(self.root, tearoff=0)
		menuOptions = Menu(self.root, tearoff=0)
		menuLanguage = Menu(self.root, tearoff=0)
		menuTheme = Menu(self.root, tearoff=0)
		menuHelp = Menu(self.root, tearoff=0)

		menu.add_cascade(label=_("menu1"), menu=menuFunctions)
		menu.add_cascade(label=_("menu2"), menu=menuFormulas)
		menu.add_cascade(label=_("menu3"), menu=menuOptions)
		menu.add_cascade(label=_("menu4"), menu=menuHelp)

		menuFormulasItems = {
			_("menu2.1"): menuArea,
			_("menu2.2"): "absolute-value",
			_("menu2.3"): "short-multiplication",
			_("menu2.4"): "exponents",
			_("menu2.5"): "radicals",
			_("menu2.6"): "logarithms",
			_("menu2.7"): "arithmetic_sequences",
			_("menu2.8"): "geometric_sequences",
			_("menu2.9"): "quadratic_function"
		}
		for item in sorted(menuFormulasItems.keys()):
			if(type(menuFormulasItems[item]) is str):
				menuFormulas.add_command(label=item, command=lambda func=menuFormulasItems[item]: self.function(func))
			else:
				menuFormulas.add_cascade(label=item, menu=menuFormulasItems[item])
		menuAreaItems = {
			_("rectangle"): "rectangle",
			_("parallelogram"): "parallelogram",
			_("triangle"): "triangle",
			_("rhombus"): "rhombus",
			_("trapezoid"): "trapezoid",
			_("circle"): "circle"
		}
		for item in sorted(menuAreaItems.keys()):
			menuArea.add_command(label=item, command=lambda func=menuAreaItems[item]: self.function(func))

		menuOptions.add_cascade(label=_("menu3.1"), menu=menuLanguage)
		menuOptions.add_cascade(label=_("menu3.2"), menu=menuTheme)
		menuOptions.add_separator()
		menuOptions.add_checkbutton(label=_("menu3.3"), onvalue=True, offvalue=False, variable=vShowPreview, command=lambda: self.changeSettings('resultPreview', vShowPreview.get()))
		menuOptions.add_checkbutton(label=_("menu3.4"), onvalue=True, offvalue=False, variable=vShowHistory, command=lambda: self.changeSettings('history', vShowHistory.get()))
		menuOptions.add_checkbutton(label=_("menu3.5"), onvalue=True, offvalue=False, variable=self.vContinuity, command=lambda: self.changeSettings('continuity', self.vContinuity.get()))
		menuOptions.add_checkbutton(label=_("menu3.6"), onvalue=True, offvalue=False, variable=vAutoUpdate, command=lambda: self.changeSettings('autoUpdate', vAutoUpdate.get()))
		menuHelp.add_command(label=_("menu4.1"), command=self.info)
		menuHelp.add_command(label=_("menu4.2"), command=lambda: threading.Thread(target=self.checkForUpdates, args=(True,)).start())
		menuFunctionsItems = {
			_("menu1.1"): "screenSize",
			_("menu1.2"): "trigonometricFunc",
			_("menu1.3"): "numberSystems",
			_("menu1.4"): "temperature",
			_("menu1.5"): "length",
			_("menu1.6"): "currency",
			_("menu1.7"): "time",
			_("menu1.8"): "speed",
			_("menu1.9"): "area",
			_("menu1.10"): "energy",
			_("menu1.11"): "weightAndMass",
			_("menu1.12"): "data",
			_("menu1.13"): "volume"
		}
		for item in sorted(menuFunctionsItems.keys()):
			menuFunctions.add_command(label=item, command=lambda func=menuFunctionsItems[item]: self.function(func))
		menuLanguage.add_radiobutton(label=_("menu3.1.1"), var=vLang, value="pl", command=lambda: self.selectLanguage("pl"))
		menuLanguage.add_radiobutton(label=_("menu3.1.2"), var=vLang, value="en", command=lambda: self.selectLanguage("en"))
		for i in self.style.theme_names():
			menuTheme.add_radiobutton(label=i.capitalize(), var=vTheme, value=i, command=lambda th=i: self.changeTheme(th))

		self.frame = ttk.Frame(self.root)
		self.frame.grid(row=0, column=0, rowspan=len(self.btnLabels)+2, columnspan=len(self.btnLabels[0])+1)
		self.textbox = ttk.Label(self.frame, text="0", font=('Helvetica', '19'), anchor="e")
		self.root.bind("<Return>", lambda event: self.click("="))
		self.root.bind("<BackSpace>", lambda event: self.click("AC"))
		self.root.bind("<Delete>", lambda event: self.click("C"))
		self.root.bind("<Key>", lambda event: self.click(event.char))
		self.root.config(menu=menu)
		self.textbox.grid(row=0, columnspan=len(self.btnLabels[0]), sticky=W+E, padx=5, pady=0)
		self.resultPreview = ttk.Label(self.frame, text="0", anchor="e")
		if(vShowPreview.get()):
			self.resultPreview.grid(row=1, columnspan=len(self.btnLabels[0]), sticky=W+E, padx=5, pady=0)
		self.btn = []
		for r in range(1,len(self.btnLabels)+1):
			for c in range(len(self.btnLabels[0])):
				self.btn.append(ttk.Button(self.frame, text=self.btnLabels[r-1][c], style='big.TButton'))
				self.btn[len(self.btn)-1].grid(row=r+1, column=c, padx=2, pady=2)
				self.btn[len(self.btn)-1].configure(command=lambda text=self.btnLabels[r-1][c]:self.click(text))
		self.history = ttk.Label(self.frame, width=30, font=('13'), anchor='e', justify=RIGHT, wraplength=270)
		if(vShowHistory.get()):
			self.history.grid(row=0, column=len(self.btnLabels[0]), rowspan=len(self.btnLabels)+2, sticky='N', padx=10)
		self.root.mainloop()

	def info(self):
		messagebox.showinfo(_("menu3.1"), ("pyCalc v."+self.version+"\nGNU AGPL v.3.0\nhttps://github.com/Programista3/pyCalc"))

	def function(self, function):
		if(function == "length"):
			calc = LengthCalculator(self.root)
		elif(function == "temperature"):
			calc = TemperatureCalculator(self.root)
		elif(function == "numberSystems"):
			calc = NumberSystemCalculator(self.root)
		elif(function == "trigonometricFunc"):
			calc = TrigonometricFunctions(self.root)
		elif(function == "screenSize"):
			calc = ScreenSizeCalculator(self.root)
		elif(function == "currency"):
			calc = CurrencyConverter(self.root)
		elif(function == "parallelogram"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("parallelogram"), "images/parallelogram.png")
		elif(function == "rectangle"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("rectangle"), "images/rectangle.png")
		elif(function == "triangle"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("triangle"), "images/triangle.png")
		elif(function == "rhombus"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("rhombus"), "images/rhombus.png")
		elif(function == "trapezoid"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("trapezoid"), "images/trapezoid.png")
		elif(function == "circle"):
			image = ImageViewer(self.root, _("formulas")+" - "+_("circle"), "images/circle.png")
		elif(function == "absolute-value"):
			image = ImageViewer(self.root, _("menu2.2"), "images/absolute_value.png")
		elif(function == "short-multiplication"):
			image = ImageViewer(self.root, _("menu2.3"), "images/short_multiplication.png")
		elif(function == "exponents"):
			image = ImageViewer(self.root, _("menu2.4"), "images/exponents.png")
		elif(function == "radicals"):
			image = ImageViewer(self.root, _("menu2.5"), "images/radicals.png")
		elif(function == "time"):
			calc = TimeConverter(self.root)
		elif(function == "speed"):
			calc = SpeedConverter(self.root)
		elif(function == "logarithms"):
			image = ImageViewer(self.root, _("menu2.6"), "images/logarithms.png")
		elif(function == "arithmetic_sequences"):
			image = ImageViewer(self.root, _("menu2.7"), "images/arithmetic_sequences.png")
		elif(function == "geometric_sequences"):
			image = ImageViewer(self.root, _("menu2.8"), "images/geometric_sequences.png")
		elif(function == "quadratic_function"):
			image = ImageViewer(self.root, _("menu2.9"), "images/quadratic_function.png")
		elif(function == "area"):
			calc = AreaConverter(self.root)
		elif(function == "energy"):
			calc = EnergyConverter(self.root)
		elif(function == "weightAndMass"):
			calc = WeightAndMassConverter(self.root)
		elif(function == "data"):
			calc = DataConverter(self.root)
		elif(function == "volume"):
			calc = VolumeConverter(self.root)
 
	def changeSettings(self, setting, value):
		if(setting == 'resultPreview'):
			if(value):
				self.resultPreview.grid(row=1, columnspan=len(self.btnLabels[0]), sticky=W+E, padx=5, pady=0)
			else:
				self.resultPreview.grid_forget()
		elif(setting == 'history'):
			if(value):
				self.history.grid(row=0, column=len(self.btnLabels[0]), rowspan=len(self.btnLabels)+2, sticky='N', padx=10)
			else:
				self.history.grid_forget()
		config = ConfigParser()
		cfgpath = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc','settings.ini')
		config.read(cfgpath)
		if(not config.has_section('Settings')):
			config.add_section('Settings')
		config['Settings'][setting] = str(value)
		with open(cfgpath, 'w') as cfgfile:
			config.write(cfgfile)
			cfgfile.close()

	def changeTheme(self, theme):
		self.style.theme_use(theme)
		config = ConfigParser()
		cfgpath = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc','settings.ini')
		config.read(cfgpath)
		if(not config.has_section('Personalization')):
			config.add_section('Personalization')
		config['Personalization']['theme'] = theme
		with open(cfgpath, 'w') as cfgfile:
			config.write(cfgfile)
			cfgfile.close()

	def selectLanguage(self, language):
		lang.select(language)
		self.lang = language
		config = ConfigParser()
		cfgpath = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc','settings.ini')
		config.read(cfgpath)
		if(not config.has_section('Personalization')):
			config.add_section('Personalization')
		config['Personalization']['language'] = language
		with open(cfgpath, 'w') as cfgfile:
			config.write(cfgfile)
			cfgfile.close()
		self.root.destroy()
		self.checkSettings()
		self.startGui()

	def addHistoryItem(self, item):
		linesInThemes = [10,12,11,10,14,15,10]
		items = self.history['text'].split('\n')
		lines = 0
		for i in items:
			lines += math.ceil(len(i)/30)
		while True:
			if(lines+math.ceil(len(item)/30) < linesInThemes[self.style.theme_names().index(self.style.theme_use())]):
				self.history['text'] = item+'\n'+'\n'.join(items)
				break
			else:
				lines -= math.ceil(len(items[len(items)-1])/30)
				items.pop()

	def calculate(self, operation, preview=True):
		try:
			result = self.calculateRPN(self.convertToRPN(operation))
			if(preview):
				self.resultPreview['text'] = result
			else:
				self.resultPreview['text'] = '0'
				self.addHistoryItem(operation+'='+str(result))
				self.textbox['text'] = str(result)
				self.end = True
		except ZeroDivisionError:
			if(preview):
				self.resultPreview['text'] = '-'
			else:
				messagebox.showerror(_("error"), _("err1"))
				self.resultPreview['text'] = '0'
				self.textbox['text'] = '0'
		except Overflow:
			messagebox.showerror(_("error"), _("err4"))
			self.resultPreview['text'] = '0'
			self.textbox['text'] = '0'

	def click(self, btn):
		if(self.vContinuity.get() == False and self.end):
			self.textbox['text'] = '0'
			self.end = False
		if(btn == '=' and self.textbox['text'] != '0'):
			self.calculate(self.textbox['text'], False)
		elif(btn == 'C'):
			self.textbox['text'] = '0'
			self.resultPreview['text'] = '0'
		elif(btn == 'AC'):
			if(len(self.textbox['text']) > 1):
				self.textbox['text'] = self.textbox['text'][:-1]
				if(self.textbox['text'][-1:].isdigit()):
					self.calculate(self.textbox['text'])
			else:
				self.textbox['text'] = '0'
				self.resultPreview['text'] = '0'
		elif(btn == 'ᵪ²' and self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0',')','%','‰']):
			self.textbox['text'] += '^2'
			self.calculate(self.textbox['text'])
		elif(btn == 'ᵪʸ' and self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0',')','%','‰']):
			self.textbox['text'] += '^'
		elif(self.textbox['text'] == '0'):
			if(btn in ['1','2','3','4','5','6','7','8','9','0','-','(','√']):
				self.textbox['text'] = btn
			elif(btn in [',', '.']):
				self.textbox['text'] += '.'
		elif(btn.isdigit()):
			if(self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0','-','+','*','/','^',',','.','(','√']):
				self.textbox['text'] += btn
				self.calculate(self.textbox['text'])
		elif(btn in ['+', '*', '/', '^',] and self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0',')','%','‰']):
			self.textbox['text'] += btn
		elif(btn == '-' and self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0','(',')','%','‰']):
			self.textbox['text'] += btn
		elif(btn in ['%', '‰'] and self.textbox['text'][-1:].isdigit()):
			self.textbox['text'] += btn
			self.calculate(self.textbox['text'])
		elif(btn in [',','.'] and self.textbox['text'][-1:].isdigit()):
			if(not re.match(r'\d+[,.]\d+$', self.textbox['text'])):
				self.textbox['text'] += btn
		elif(btn == '√' and self.textbox['text'][-1:] in ['-','+','*','/','(']):
			self.textbox['text'] += btn
		elif(btn == '(' and self.textbox['text'][-1:] in ['-','+','*','/','^','√','(']):
			self.textbox['text'] += btn
		elif(btn == '(' and self.textbox['text'][-1:].isdigit()):
			self.textbox['text'] += '*('
		elif(btn == ')' and self.textbox['text'][-1:] in ['1','2','3','4','5','6','7','8','9','0',')','%','‰']):
			if(self.textbox['text'].count('(') > self.textbox['text'].count(')')):
				self.textbox['text'] += btn

	def isOperator(self, char):
		return char in ['+','-','*','/','^','√']

	def isFunction(self, char):
		return char in ['%','‰']

	def priority(self, char):
		if(char == '+' or char == '-'):
			return 1
		elif(char == '*' or char == '/'):
			return 2
		elif(char == '^' or char == '√'):
			return 3
		elif(char == '('):
			return 0
		else:
			return 4

	def convertToRPN(self, text):
		text = text.replace(',', '.')
		stack = Stack()
		output = []
		negative = False
		brackets = []
		for i in range(len(text)):
			if(text[i].isdigit()):
				if(i > 0) and (text[i-1].isdigit() or text[i-1] == '.'):
					output[len(output)-1] += text[i]
				else:
					if(negative):
						if(len(brackets) > 0 and brackets[len(brackets)-1] == True):
							output.append(text[i])
						else:
							output.append("-"+text[i])
						negative = False
					else:
						if(len(brackets) > 0 and brackets[len(brackets)-1] == True):
							output.append("-"+text[i])
						else:
							output.append(text[i])
			elif(text[i] == '.'):
				output[len(output)-1] += text[i]
			elif(self.isFunction(text[i])):
				stack.push(text[i])
			elif(self.isOperator(text[i])):
				if(text[i] == '-'):
					if((i == 0) or (self.isOperator(text[i-1])) or text[i-1] == '(') and negative == False:
						negative = True
						continue
				for j in range(stack.size()):
					if(self.priority(text[i]) == 3 or self.priority(text[i]) > self.priority(stack.top())):
						break
					output.append(stack.top())
					stack.pop()
				stack.push(text[i])
			elif(text[i] == '('):
				stack.push(text[i])
				if(negative):
					negative = False
					brackets.append(True)
				else:
					brackets.append(False)
			elif(text[i] == ')'):
				while stack.top() != '(':
					output.append(stack.top())
					stack.pop()
					if(stack.size() == 0):
						return 0
				stack.pop()
				brackets.pop()
		output.extend(stack.get())
		return output

	def calculateRPN(self, rpn):
		if(rpn == 0):
			return 0
		stack = Stack()
		output = []
		for c in rpn:
			if(self.isNumber(c) == 1 or self.isNumber(c) == 2):
				stack.push(Decimal(c))
			elif(self.isFunction(c)):
				a = stack.top()
				stack.pop()
				if(c == '%'):
					stack.push(a/100)
				elif(c == '‰'):
					stack.push(a/1000)
			elif(self.isOperator(c)):
				if(c == '√'):
					a = stack.top()
					stack.pop()
					stack.push(a**Decimal('0.5'))
				else:
					if(stack.size() > 1):
						a = stack.top()
						stack.pop()  
						b = stack.top()
						stack.pop()
						if(c == "+"):
							stack.push(b+a)
						elif(c == "-"):
							stack.push(b-a)
						elif(c == "*"):
							stack.push(b*a)
						elif(c == "/"):
							if(a != 0):
								stack.push(b/a)
							else:
								raise ZeroDivisionError
						elif(c == "^"):
							stack.push(b**a)
					else:
						return 0
		return int(stack.top()) if float(stack.top()).is_integer() else stack.top()
		#return self.normalizeFraction(stack.top())

	def checkSettings(self):
		path = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc')
		if(os.path.isdir(path)):
			if(os.path.isfile(os.path.join(path,'settings.ini'))):
				config = ConfigParser()
				cfgpath = os.path.join(path,'settings.ini')
				config.read(cfgpath)
				for section in self.settingsTemplate:
					if(config.has_section(section)):
						for option in self.settingsTemplate[section]:
							if(not config.has_option(section,option)):
								config.set(section,option,self.settingsTemplate[section][option])
					else:
						self.createDefaultSettingsFile()
						return
				with open(cfgpath, 'w') as cfgfile:
					config.write(cfgfile)
					cfgfile.close()
			else:
				self.createDefaultSettingsFile()
		else:
			os.makedirs(path)
			self.createDefaultSettingsFile()

	def createDefaultSettingsFile(self):
		path = os.path.join(os.getenv('LOCALAPPDATA'),'pyCalc','settings.ini')
		open(path, 'w+').close()
		config = ConfigParser()
		config.read(path)
		for section in self.settingsTemplate:
			config.add_section(section)
			for option in self.settingsTemplate[section]:
				config.set(section,option,self.settingsTemplate[section][option])
		with open(path, 'w') as cfgfile:
			config.write(cfgfile)
			cfgfile.close()

	def checkForUpdates(self, *args):
		latest = urllib.urlopen('https://github.com/Programista3/pyCalc/releases/latest')
		parse = BeautifulSoup(latest, 'html.parser')
		version = parse.select_one('div.release-header > div > div > a').text
		if(version > self.version):
			window = Toplevel(self.root, padx=20, pady=10)
			window.resizable(False, False)
			window.transient(self.root)
			window.title(_("update available"))
			window.iconbitmap('pycalc.ico')
			label = Label(window, text=_("actual version")+'  '+self.version+'\n'+_("available version")+'  '+version+'\r\n'+_("download update"), justify=LEFT)
			label.pack(pady=(0, 10))
			buttons = ttk.Frame(window)
			buttons.pack()
			btnYes = ttk.Button(buttons, text=_("yes"), command=lambda: (webbrowser.open('https://github.com/Programista3/pyCalc/releases/latest'), window.destroy))
			btnYes.pack(side=LEFT, padx=(0, 10))
			btnNo = ttk.Button(buttons, text=_("no"), command=window.destroy)
			btnNo.pack(side=LEFT)
		elif(args[0]):
			window = Toplevel(self.root, padx=20, pady=10)
			window.resizable(False, False)
			window.transient(self.root)
			window.title(_("up to date"))
			window.iconbitmap('pycalc.ico')
			label = Label(window, text=_("up to date msg")+'\r\n'+_("actual version")+'  '+self.version, justify=LEFT)
			label.pack(pady=(0, 10))
			buttons = ttk.Frame(window)
			buttons.pack()
			btnOk = ttk.Button(buttons, text="OK", command=window.destroy)
			btnOk.pack()

calc = pyCalc()