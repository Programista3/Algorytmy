# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk

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
    version = "3.0.7"

    def __init__(self):
        self.startGui()

    def startGui(self):
        self.chars = ['1','2','3','4','5','6','7','8','9','0','-','+','*','/','^',',','.','(',')','√']
        self.root = Tk()
        self.root.title("pyCalc v."+self.version)
        self.root.resizable(False, False)
        ttk.Style().configure("TButton", padding=(-10,10,-10,10), font=('16'))
        btnLabels = [
            ['ᵪ²','ᵪʸ','C','AC','/'],
            ['√','7','8','9','*'],
            ['%','4','5','6','-'],
            ['‰','1','2','3','+'],
            ['(',')','0','.','=']
        ]
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, rowspan=len(btnLabels)+1, columnspan=len(btnLabels[0]))
        self.textbox = ttk.Label(self.frame, text="0", font=('Helvetica', '18'), anchor="e")
        self.root.bind("<Return>", lambda event: self.click("="))
        self.root.bind("<BackSpace>", lambda event: self.click("AC"))
        self.root.bind("<Delete>", lambda event: self.click("C"))
        self.root.bind("<Key>", lambda event: self.click(event.char))
        self.textbox.grid(row=0, columnspan=len(btnLabels[0]), sticky=W+E, padx=3, pady=3)
        self.btn = []
        for r in range(1,len(btnLabels)+1):
            for c in range(len(btnLabels[0])):
                self.btn.append(ttk.Button(self.frame, text=btnLabels[r-1][c]))
                self.btn[len(self.btn)-1].grid(row=r, column=c, padx=2, pady=2)
                self.btn[len(self.btn)-1].configure(command=lambda text=btnLabels[r-1][c]:self.click(text))
        self.root.mainloop()

    def click(self, btn):
        if(btn == '='):
            #print(self.convertToRPN(self.textbox['text']))
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
                elif(btn in [',','.']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:].isdigit()):
                if(btn in [',','.','+','-','*','/','^',')'] or btn.isdigit()):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] == ')'):
                if(btn in ['+','-','*','/','^']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] in ['+','-','*','/','^']):
                if(btn.isdigit() or btn in ['√','(']):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] in [',','.','√']):
                if(btn.isdigit()):
                    self.textbox['text'] += btn
            elif(self.textbox['text'][-1:] == '('):
                if(btn.isdigit() or btn == '√'):
                    self.textbox['text'] += btn

    def isOperator(self, char):
        return char in ['+','-','*','/','^','√']

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
                        stack.push(b/a)
                    elif(c == "^"):
                        stack.push(b**a)
        return int(stack.top()) if stack.top().is_integer() else stack.top()

calc = pyCalc()