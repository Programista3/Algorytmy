# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import os
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
        self.version = "3.1.2"
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

        menuLanguage.add_radiobutton(label=_("menu2.1.1"), var=vLang, value="pl", command=lambda: self.selectLanguage("pl"))
        menuLanguage.add_radiobutton(label=_("menu2.1.2"), var=vLang, value="en", command=lambda: self.selectLanguage("en"))
        for i in self.style.theme_names():
            menuTheme.add_radiobutton(label=i.capitalize(), var=vTheme, value=i, command=lambda th=i: self.changeTheme(th))

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, rowspan=len(btnLabels)+1, columnspan=len(btnLabels[0]))
        self.textbox = ttk.Label(self.frame, text="0", font=('Helvetica', '18'), anchor="e")
        self.root.bind("<Return>", lambda event: self.click("="))
        self.root.bind("<BackSpace>", lambda event: self.click("AC"))
        self.root.bind("<Delete>", lambda event: self.click("C"))
        self.root.bind("<Key>", lambda event: self.click(event.char))
        self.root.config(menu=menu)
        self.textbox.grid(row=0, columnspan=len(btnLabels[0]), sticky=W+E, padx=3, pady=3)
        self.btn = []
        for r in range(1,len(btnLabels)+1):
            for c in range(len(btnLabels[0])):
                self.btn.append(ttk.Button(self.frame, text=btnLabels[r-1][c], style='big.TButton'))
                self.btn[len(self.btn)-1].grid(row=r, column=c, padx=2, pady=2)
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
            self.number[i].delete(0, END)

    def calcScreenSize(self, index):
        if(index != None):
            ratio = list(map(int, self.combobox.get().split(':')))
            if(index == 0):
                if(self.isNumner(self.number[0].get())):
                    result = self.calcScreenSizeDiagonal(float(self.number[0].get()), ratio)
                    for i in range(1,6):
                        self.number[i].delete(0, END)
                    self.number[1].insert(0, result[0])
                    self.number[2].insert(0, result[1])
                    self.number[3].insert(0, round(float(self.number[0].get())*2.54,2))
                    self.number[4].insert(0, round(result[0]*2.54,2))
                    self.number[5].insert(0, round(result[1]*2.54,2))
            elif(index == 1):
                if(self.isNumner(self.number[1].get())):
                    result = self.calcScreenSizeWidth(float(self.number[1].get()), ratio)
                    for i in [0,2,3,4,5]:
                        self.number[i].delete(0, END)
                    self.number[0].insert(0, result[1])
                    self.number[2].insert(0, result[0])
                    self.number[3].insert(0, round(result[1]*2.54,2))
                    self.number[4].insert(0, round(float(self.number[1].get())*2.54,2))
                    self.number[5].insert(0, round(result[0]*2.54,2))
            elif(index == 2):
                if(self.isNumner(self.number[2].get())):
                    result = self.calcScreenSizeHeight(float(self.number[2].get()), ratio)
                    for i in [0,1,3,4,5]:
                        self.number[i].delete(0, END)
                    self.number[0].insert(0, result[1])
                    self.number[1].insert(0, result[0])
                    self.number[3].insert(0, round(result[1]*2.54,2))
                    self.number[4].insert(0, round(result[0]*2.54,2))
                    self.number[5].insert(0, round(float(self.number[2].get())*2.54,2))
            elif(index == 3):
                if(self.isNumner(self.number[3].get())):
                    result = self.calcScreenSizeDiagonal(self.number[3].get(), ratio)
                    for i in [0,1,2,4,5]:
                        self.number[i].delete(0, END)
                    self.number[0].insert(0, round(float(self.number[3].get())/2.54,2))
                    self.number[1].insert(0, round(result[0]/2.54,2))
                    self.number[2].insert(0, round(result[1]/2.54,2))
                    self.number[4].insert(0, round(result[0],2))
                    self.number[5].insert(0, round(result[1],2))
            elif(index == 4):
                if(self.isNumner(self.number[4].get())):
                    result = self.calcScreenSizeWidth(float(self.number[4].get()), ratio)
                    for i in [0,1,2,3,5]:
                        self.number[i].delete(0, END)
                    self.number[0].insert(0, round(result[1]/2.54,2))
                    self.number[1].insert(0, round(float(self.number[4].get())/2.54,2))
                    self.number[2].insert(0, round(result[0]/2.54,2))
                    self.number[3].insert(0, result[1])
                    self.number[5].insert(0, result[0])
            elif(index == 5):
                if(self.isNumner(self.number[5].get())):
                    result = self.calcScreenSizeHeight(float(self.number[5].get()), ratio)
                    for i in [0,1,2,3,4]:
                        self.number[i].delete(0, END)
                    self.number[0].insert(0, round(result[1]/2.54,2))
                    self.number[1].insert(0, round(result[0]/2.54,2))
                    self.number[2].insert(0, round(float(self.number[5].get())/2.54,2))
                    self.number[3].insert(0, result[1])
                    self.number[4].insert(0, result[0])

    def screenSizeActiveEntry(self, index):
        self.ssActiveEntry = index

    def screenSize(self):
        self.ssActiveEntry = None
        window = Toplevel(self.root)
        window.title(_("screenSizeTitle"))
        window.iconbitmap('pycalc.ico')
        frame = ttk.Frame(window)
        frame.bind("<Button>", lambda event: self.calcScreenSize(self.ssActiveEntry))
        frame.focus_set()
        frame.grid(row=0, column=0, rowspan=3, columnspan=5, padx=30, pady=20)
        boxVal = StringVar()
        ratio = ['16:9','16:10','4:3','3:2','5:4','21:9','2:1']
        self.combobox = ttk.Combobox(frame, values=ratio, width=12)
        self.combobox.current(0)
        self.combobox.grid(row=0, column=1, columnspan=4)
        text = [_('ratio'), _('diagonal'), _('width'), _('height')]
        label = []
        self.number = []
        for i in range(4):
            label.append(ttk.Label(frame, text=text[i]))
            label[i].grid(row=i, column=0, pady=5)
        for i in range(1,4):
            self.number.append(ttk.Entry(frame, width=6))
            self.number[i-1].bind("<FocusIn>", lambda event, index=i-1: self.screenSizeActiveEntry(index))
            self.number[i-1].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.number[i-1].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.number[i-1].grid(row=i, column=1, padx=(10, 0))
        for i in range(4,7):
            label.append(ttk.Label(frame, text=_("inch")))
            label[i].grid(row=i-3, column=2)
        for i in range(4,7):
            self.number.append(ttk.Entry(frame, width=6))
            self.number[i-1].bind("<FocusIn>", lambda event, index=i-1: self.screenSizeActiveEntry(index))
            self.number[i-1].bind("<FocusOut>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.number[i-1].bind("<Return>", lambda event: self.calcScreenSize(self.ssActiveEntry))
            self.number[i-1].grid(row=i-3, column=3, padx=(10,0))
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
        elif(btn == 'C'):
            self.textbox['text'] = "0"
        elif(btn == 'AC'):
            if(len(self.textbox['text']) > 1):
                self.textbox['text'] = self.textbox['text'][:-1]
            else:
                self.textbox['text'] = "0"
        elif(btn == 'ᵪ²'):
            if(self.textbox['text'][-1:].isdigit()):
                self.textbox['text'] += '^2'
        elif(btn == 'ᵪʸ'):
            if(self.textbox['text'][-1:].isdigit()):
                self.textbox['text'] += '^'
        elif(btn in self.chars):
            if(self.textbox['text'] == "0"):
                if(btn in ['1','2','3','4','5','6','7','8','9','(','-','√']):
                    self.textbox['text'] = btn
                elif(btn in [',','.','+','-','*','/','^']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] == '0' and self.textbox['text'][-2:][0] in ['+','-','*','/','^']):
                self.textbox['text'] = self.textbox['text']+btn
            elif(self.textbox['text'][-1:].isdigit()):
                if(btn in [',','.','+','-','*','/','^',')','%','‰'] or btn.isdigit()):
                    self.textbox['text'] += btn
                elif(btn == '('):
                    self.textbox['text'] += '*('
            elif(self.textbox['text'][-1:] == ')'):
                if(btn in ['+','-','*','/','^']):
                    self.textbox['text'] += btn
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

    def isNumner(self, str):
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
                stack.pop()
                brackets.pop()
        output.extend(stack.get())
        return output

    def calculateRPN(self, rpn):
        stack = Stack()
        output = []
        for c in rpn:
            if(self.isNumner(c) == 1):
                stack.push(int(c))
            elif(self.isNumner(c) == 2):
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
        return int(stack.top()) if float(stack.top()).is_integer() else stack.top()

calc = pyCalc()