# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import re
import os
import math
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

class pyCalc:
    def __init__(self):
        self.chars = ['1','2','3','4','5','6','7','8','9','0','-','+','*','/','^',',','.','(',')','√','%','‰']
        self.version = "3.1.5"
        self.languages = ['pl','en']
        self.lang = "pl"
        self.startGui()

    def startGui(self):
        self.root = Tk()
        self.root.title("pyCalc3")
        self.root.iconbitmap('pycalc.ico')
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("big.TButton", padding=(-10,10,-10,10), font=('16'))
        btnLabels = [
            ['ᵪ²','ᵪʸ','C','AC','/'],
            ['√','7','8','9','*'],
            ['%','4','5','6','-'],
            ['‰','1','2','3','+'],
            ['(',')','0','.','=']
        ]
        vTheme = StringVar(value=self.style.theme_use())
        if(os.path.isfile('settings.dat')):
            file = open('settings.dat')
            text = file.read()
            file.close()
            if(len(text) == 2):
                if(int(text[0]) < len(self.languages)):
                    self.lang = self.languages[int(text[0])]
                    lang.select(self.lang)
                if(int(text[1]) < len(self.style.theme_names())):
                    vTheme = StringVar(value=self.style.theme_names()[int(text[1])])
                    self.style.theme_use(self.style.theme_names()[int(text[1])])
        vLang = StringVar(value=self.lang)

        menu = Menu(self.root)
        menuFunctions = Menu(self.root, tearoff=0)
        menuOptions = Menu(self.root, tearoff=0)
        menuLanguage = Menu(self.root, tearoff=0)
        menuTheme = Menu(self.root, tearoff=0)
        menuHelp = Menu(self.root, tearoff=0)

        menu.add_cascade(label=_("menu1"), menu=menuFunctions)
        menu.add_cascade(label=_("menu2"), menu=menuOptions)
        menu.add_cascade(label=_("menu3"), menu=menuHelp)

        menuOptions.add_cascade(label=_("menu2.1"), menu=menuLanguage)
        menuOptions.add_cascade(label=_("menu2.2"), menu=menuTheme)
        menuHelp.add_command(label=_("menu3.1"), command=self.info)
        menuFunctions.add_command(label=_("menu1.1"), command=self.screenSize)
        menuFunctions.add_command(label=_("menu1.2"), command=self.trigonometricFunc)
        menuFunctions.add_command(label=_("menu1.3"), command=self.numberSystems)

        menuLanguage.add_radiobutton(label=_("menu2.1.1"), var=vLang, value="pl", command=lambda: self.selectLanguage("pl"))
        menuLanguage.add_radiobutton(label=_("menu2.1.2"), var=vLang, value="en", command=lambda: self.selectLanguage("en"))
        for i in self.style.theme_names():
            menuTheme.add_radiobutton(label=i.capitalize(), var=vTheme, value=i, command=lambda th=i: self.changeTheme(th))

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, rowspan=len(btnLabels)+1, columnspan=len(btnLabels[0]))
        self.textbox = ttk.Label(self.frame, text="0", font=('Helvetica', '19'), anchor="e")
        self.root.bind("<Return>", lambda event: self.click("="))
        self.root.bind("<BackSpace>", lambda event: self.click("AC"))
        self.root.bind("<Delete>", lambda event: self.click("C"))
        self.root.bind("<Key>", lambda event: self.click(event.char))
        self.root.config(menu=menu)
        self.textbox.grid(row=0, columnspan=len(btnLabels[0]), sticky=W+E, padx=5, pady=0)
        self.resultPreview = ttk.Label(self.frame, text="0", anchor="e")
        self.resultPreview.grid(row=1, columnspan=len(btnLabels[0]), sticky=W+E, padx=5, pady=0)
        #self.resultPreview.grid_forget()
        self.btn = []
        for r in range(1,len(btnLabels)+1):
            for c in range(len(btnLabels[0])):
                self.btn.append(ttk.Button(self.frame, text=btnLabels[r-1][c], style='big.TButton'))
                self.btn[len(self.btn)-1].grid(row=r+1, column=c, padx=2, pady=2)
                self.btn[len(self.btn)-1].configure(command=lambda text=btnLabels[r-1][c]:self.click(text))
        self.root.mainloop()

    def info(self):
        messagebox.showinfo(_("menu3.1"), ("pyCalc v."+self.version+"\nGNU AGPL v.3.0\nhttps://github.com/Programista3/pyCalc"))

    def calcScreenSizeDiagonal(self, diagonal, ratio):
        result = ((ratio[0]**2+ratio[1]**2)**0.5)/float(diagonal)
        return (round(ratio[0]/result,2), round(ratio[1]/result,2))

    def calcScreenSizeWidth(self, width, ratio):
        height = round(width*ratio[1]/ratio[0],2)
        diagonal = round((width**2+height**2)**0.5,2)
        return (height, diagonal)

    def calcScreenSizeHeight(self, height, ratio):
        width = round(height*ratio[0]/ratio[1],2)
        diagonal = round((width**2+height**2)**0.5,2)
        return (width, diagonal)

    def clearScreenSizeForm(self):
        for i in range(0,6):
            self.SS_number[i].delete(0, END)

    def numberSystems(self):
        window = Toplevel(self.root)
        window.title(_("menu1.3"))
        window.iconbitmap('pycalc.ico')
        frame = ttk.Frame(window)
        frame.grid(row=0, column=0, rowspan=2, columnspan=5, padx=30, pady=20)
        text = [_("number"),_("inputSystem"),_("targetSystem"),_("result")]
        systems = [_("2ns"),_("8ns"),_("10ns"),_("16ns")]
        labels = []
        for i in range(4):
            labels.append(ttk.Label(frame, text=text[i]))
            labels[i].grid(row=i, column=0, pady=5, padx=8)
        number = ttk.Entry(frame, width=14)
        number.grid(row=0, column=1)
        inCBox = ttk.Combobox(frame, values=systems, width=11)
        inCBox.current(0)
        inCBox.grid(row=1, column=1)
        outCBox = ttk.Combobox(frame, values=systems, width=11)
        outCBox.current(1)
        outCBox.grid(row=2, column=1)
        self.NS_result = ttk.Label(frame)
        self.NS_result.grid(row=3, column=1)
        submit = ttk.Button(frame, text=_("calculate"), command=lambda: self.convertNumberSystem(number.get(),inCBox.current(),outCBox.current()))
        submit.grid(row=4, column=0, columnspan=2, pady=(10,0))

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
            self.NS_result['text'] = str(bin(number))[2:]
        elif(systemOut == 1):
            self.NS_result['text'] = str(oct(number))[2:]
        elif(systemOut == 2):
            self.NS_result['text'] = str(number)
        elif(systemOut == 3):
            self.NS_result['text'] = str(hex(number))[2:]

    def trigonometricFunc(self):
        window = Toplevel(self.root)
        window.title(_("menu1.2"))
        window.iconbitmap('pycalc.ico')
        frame = ttk.Frame(window)
        frame.grid(row=0, column=0, rowspan=5, columnspan=2, padx=30, pady=20)
        text = [_("function"),_("value"),_("unit"),_("result")]
        functions = ['sin','cos','tg','ctg']
        units = [_("degree"),_("radian")]
        labels = []
        for i in range(4):
            labels.append(ttk.Label(frame, text=text[i]))
            labels[i].grid(row=i, column=0, pady=5, padx=8)
        funcCBox = ttk.Combobox(frame, values=functions, width=8)
        funcCBox.current(0)
        funcCBox.grid(row=0, column=1)
        value = ttk.Entry(frame, width=11)
        value.grid(row=1, column=1)
        unitCBox = ttk.Combobox(frame, values=units, width=8)
        unitCBox.current(0)
        unitCBox.grid(row=2, column=1)
        self.TF_result = ttk.Label(frame)
        self.TF_result.grid(row=3, column=1)
        submit = ttk.Button(frame, text=_("calculate"), command=lambda: self.calcTrigonometricFunc(funcCBox.get(),unitCBox.current(),value.get()))
        submit.grid(row=4, column=0, columnspan=2, pady=(10,0))

    def calcTrigonometricFunc(self, function, unit, value):
        if(value.isdigit()):
            value = int(value)
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
            self.TF_result['text'] = str(round(value,10))

    def calcScreenSize(self, index):
        if(index != None):
            ratio = list(map(int, self.SS_combobox.get().split(':')))
            if(index == 0):
                if(self.isNumber(self.SS_number[0].get())):
                    result = self.calcScreenSizeDiagonal(float(self.SS_number[0].get()), ratio)
                    for i in range(1,6):
                        self.SS_number[i].delete(0, END)
                    self.SS_number[1].insert(0, result[0])
                    self.SS_number[2].insert(0, result[1])
                    self.SS_number[3].insert(0, round(float(self.SS_number[0].get())*2.54,2))
                    self.SS_number[4].insert(0, round(result[0]*2.54,2))
                    self.SS_number[5].insert(0, round(result[1]*2.54,2))
            elif(index == 1):
                if(self.isNumber(self.SS_number[1].get())):
                    result = self.calcScreenSizeWidth(float(self.SS_number[1].get()), ratio)
                    for i in [0,2,3,4,5]:
                        self.SS_number[i].delete(0, END)
                    self.SS_number[0].insert(0, result[1])
                    self.SS_number[2].insert(0, result[0])
                    self.SS_number[3].insert(0, round(result[1]*2.54,2))
                    self.SS_number[4].insert(0, round(float(self.SS_number[1].get())*2.54,2))
                    self.SS_number[5].insert(0, round(result[0]*2.54,2))
            elif(index == 2):
                if(self.isNumber(self.SS_number[2].get())):
                    result = self.calcScreenSizeHeight(float(self.SS_number[2].get()), ratio)
                    for i in [0,1,3,4,5]:
                        self.SS_number[i].delete(0, END)
                    self.SS_number[0].insert(0, result[1])
                    self.SS_number[1].insert(0, result[0])
                    self.SS_number[3].insert(0, round(result[1]*2.54,2))
                    self.SS_number[4].insert(0, round(result[0]*2.54,2))
                    self.SS_number[5].insert(0, round(float(self.SS_number[2].get())*2.54,2))
            elif(index == 3):
                if(self.isNumber(self.SS_number[3].get())):
                    result = self.calcScreenSizeDiagonal(self.SS_number[3].get(), ratio)
                    for i in [0,1,2,4,5]:
                        self.SS_number[i].delete(0, END)
                    self.SS_number[0].insert(0, round(float(self.SS_number[3].get())/2.54,2))
                    self.SS_number[1].insert(0, round(result[0]/2.54,2))
                    self.SS_number[2].insert(0, round(result[1]/2.54,2))
                    self.SS_number[4].insert(0, round(result[0],2))
                    self.SS_number[5].insert(0, round(result[1],2))
            elif(index == 4):
                if(self.isNumber(self.SS_number[4].get())):
                    result = self.calcScreenSizeWidth(float(self.SS_number[4].get()), ratio)
                    for i in [0,1,2,3,5]:
                        self.SS_number[i].delete(0, END)
                    self.SS_number[0].insert(0, round(result[1]/2.54,2))
                    self.SS_number[1].insert(0, round(float(self.SS_number[4].get())/2.54,2))
                    self.SS_number[2].insert(0, round(result[0]/2.54,2))
                    self.SS_number[3].insert(0, result[1])
                    self.SS_number[5].insert(0, result[0])
            elif(index == 5):
                if(self.isNumber(self.SS_number[5].get())):
                    result = self.calcScreenSizeHeight(float(self.SS_number[5].get()), ratio)
                    for i in [0,1,2,3,4]:
                        self.SS_number[i].delete(0, END)
                    self.SS_number[0].insert(0, round(result[1]/2.54,2))
                    self.SS_number[1].insert(0, round(result[0]/2.54,2))
                    self.SS_number[2].insert(0, round(float(self.SS_number[5].get())/2.54,2))
                    self.SS_number[3].insert(0, result[1])
                    self.SS_number[4].insert(0, result[0])

    def screenSizeActiveEntry(self, index):
        self.ssActiveEntry = index

    def screenSize(self):
        self.ssActiveEntry = None
        window = Toplevel(self.root)
        window.title(_("menu1.1"))
        window.iconbitmap('pycalc.ico')
        frame = ttk.Frame(window)
        frame.bind("<Button>", lambda event: self.calcScreenSize(self.ssActiveEntry))
        frame.focus_set()
        frame.grid(row=0, column=0, rowspan=3, columnspan=5, padx=30, pady=20)
        ratio = ['16:9','16:10','4:3','3:2','5:4','21:9','2:1']
        self.SS_combobox = ttk.Combobox(frame, values=ratio, width=12)
        self.SS_combobox.current(0)
        self.SS_combobox.grid(row=0, column=1, columnspan=4)
        text = [_('ratio'), _('diagonal'), _('width'), _('height')]
        label = []
        self.SS_number = []
        for i in range(4):
            label.append(ttk.Label(frame, text=text[i]))
            label[i].grid(row=i, column=0, pady=5)
        for i in range(1,4):
            self.SS_number.append(ttk.Entry(frame, width=6))
            self.SS_number[i-1].bind("<FocusIn>", lambda event, index=i-1: self.screenSizeActiveEntry(index))
            self.SS_number[i-1].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.SS_number[i-1].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.SS_number[i-1].grid(row=i, column=1, padx=(10, 0))
        for i in range(4,7):
            label.append(ttk.Label(frame, text=_("inch")))
            label[i].grid(row=i-3, column=2)
        for i in range(4,7):
            self.SS_number.append(ttk.Entry(frame, width=6))
            self.SS_number[i-1].bind("<FocusIn>", lambda event, index=i-1: self.screenSizeActiveEntry(index))
            self.SS_number[i-1].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.SS_number[i-1].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.SS_number[i-1].grid(row=i-3, column=3, padx=(10,0))
        for i in range(7,10):
            label.append(ttk.Label(frame, text="cm"))
            label[i].grid(row=i-6, column=4)
        buttonCalc = ttk.Button(frame, text=_("calculate"), command=lambda: self.calcScreenSize(self.ssActiveEntry))
        buttonCalc.grid(row=4, column=0, columnspan=2, pady=(10,0))
        buttonReset = ttk.Button(frame, text=_("clear"), command=self.clearScreenSizeForm)
        buttonReset.grid(row=4, column=2, columnspan=2, pady=(10,0))

    def changeTheme(self, theme):
        self.style.theme_use(theme)
        file = open('settings.dat', 'w')
        file.write(str(self.languages.index(self.lang))+str(self.style.theme_names().index(self.style.theme_use())))
        file.close()

    def selectLanguage(self, language):
        lang.select(language)
        self.lang = language
        file = open('settings.dat', 'w')
        file.write(str(self.languages.index(self.lang))+str(self.style.theme_names().index(self.style.theme_use())))
        file.close()
        self.root.destroy()
        self.startGui()

    def click(self, btn):
        if(btn == '='):
            result = self.calculateRPN(self.convertToRPN(self.textbox['text']))
            self.textbox['text'] = str(result)
            self.resultPreview['text'] = "0"
        elif(btn == 'C'):
            self.textbox['text'] = "0"
            self.resultPreview['text'] = "0"
        elif(btn == 'AC'):
            if(len(self.textbox['text']) > 1):
                self.textbox['text'] = self.textbox['text'][:-1]
                if(self.textbox['text'][-1:].isdigit()):
                    result = self.calculateRPN(self.convertToRPN(self.textbox['text']))
                    self.resultPreview['text'] = result
            else:
                self.textbox['text'] = "0"
                self.resultPreview['text'] = "0"
        elif(btn == 'ᵪ²'):
            if(self.textbox['text'][-1:].isdigit()):
                self.textbox['text'] += '^2'
                result = self.calculateRPN(self.convertToRPN(self.textbox['text']))
                self.resultPreview['text'] = result
        elif(btn == 'ᵪʸ'):
            if(self.textbox['text'][-1:].isdigit()):
                self.textbox['text'] += '^'
        elif(btn in self.chars):
            if(btn.isdigit() or btn in ['%','‰']):
                result = self.calculateRPN(self.convertToRPN(self.textbox['text']+btn))
                self.resultPreview['text'] = result
            if(self.textbox['text'] == "0"):
                if(btn in ['1','2','3','4','5','6','7','8','9','(','-','√']):
                    self.textbox['text'] = btn
                elif(btn in [',','.','+','-','*','/','^']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] == '0' and self.textbox['text'][-2:][0] in ['+','-','*','/','^']):
                self.textbox['text'] = self.textbox['text']+btn
            elif(self.textbox['text'][-1:].isdigit()):
                if(btn in [',','.','+','-','*','/','^','%','‰'] or btn.isdigit()):
                    self.textbox['text'] += btn
                elif(btn == '('):
                    self.textbox['text'] += '*('
                elif(btn == ')'):
                    if(self.textbox['text'].count('(') > self.textbox['text'].count(')')):
                        self.textbox['text'] += ')'
            elif(self.textbox['text'][-1:] == ')'):
                if(btn in ['+','-','*','/','^']):
                    self.textbox['text'] += btn
                elif(btn == ')'):
                    if(self.textbox['text'].count('(') > self.textbox['text'].count(')')):
                        self.textbox['text'] += ')'
            elif(self.textbox['text'][-1:] in ['+','-','*','/','^']):
                if(btn.isdigit() or btn in ['√','(','-']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] in [',','.','√']):
                if(btn.isdigit()):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] == '('):
                if(btn.isdigit() or btn == '√'):
                    self.textbox['text'] += btn

    def isOperator(self, char):
        return char in ['+','-','*','/','^','√']

    def isFunction(self, char):
        return char in ['%','‰']

    def isNumber(self, str):
        if(str.isdigit()):
            return 1
        else:
            try:
                float(str)
                return 2
            except ValueError:
                return 0

    def priority(self, operator):
        if(operator == '+' or operator == '-'):
            return 1
        elif(operator == '*' or operator == '/'):
            return 2
        elif(operator == '^' or operator == '√'):
            return 3
        elif(operator == '('):
            return 0

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
            if(self.isNumber(c) == 1):
                stack.push(int(c))
            elif(self.isNumber(c) == 2):
                stack.push(float(c))
            elif(self.isFunction(c)):
                a = stack.top()
                stack.pop()
                if(c == '%'):
                    stack.push(a/100)
                elif(c == '‰'):
                    stack.push(1/1000)
            elif(self.isOperator(c)):
                if(c == '√'):
                    a = stack.top()
                    stack.pop()
                    stack.push(a**0.5)
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
                                messagebox.showerror(_("error"), _("err1"))
                                return 0
                        elif(c == "^"):
                            stack.push(b**a)
                    else:
                        return 0
        return int(stack.top()) if float(stack.top()).is_integer() else stack.top()

calc = pyCalc()