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
    version = "3.0.6"

    def __init__(self):
        self.startGui()

    def startGui(self):
        self.root = Tk()
        self.root.title("pyCalc v."+self.version)
        ttk.Style().configure("TButton", padding=(-10,10,-10,10), font=('16'))
        btnLabels = [
            ['C','7','8','9','/'],
            ['AC','4','5','6','*'],
            ['(','1','2','3','-'],
            [')','.','0','=','+']
        ]
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, rowspan=len(btnLabels)+1, columnspan=len(btnLabels[0]))
        self.textbox = ttk.Entry(self.frame, font=('Helvetica', '16'), justify=RIGHT)
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
            #print(self.convertToRPN(self.textbox.get()))
            result = self.calculateRPN(self.convertToRPN(self.textbox.get()))
            self.textbox.delete(0, END)
            self.textbox.insert(END, result)
        elif(btn == 'C'):
            self.textbox.delete(0, END)
        elif(btn == 'AC'):
            self.textbox.delete(len(self.textbox.get())-1, END)
        else:
            self.textbox.insert(END, btn)

    def isOperator(self, char):
        return char in ['+','-','*','/','^']

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
        elif(operator == '^'):
            return 3
        elif(operator == '('):
            return 0

    def convertToRPN(self, text):
        text = text.replace(',', '.')
        stack = Stack()
        output = []
        negative = False
        for i in range(len(text)):
            if(text[i].isdigit()):
                if(i > 0) and (text[i-1].isdigit() or text[i-1] == '.'):
                    output[len(output)-1] += text[i]
                else:
                    if(negative):
                        output.append("-"+text[i])
                        negative = False
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
                    negative = False # temporarily
            elif(text[i] == ')'):
                while stack.top() != '(':
                    output.append(stack.top())
                    stack.pop()
                stack.pop()
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
        return stack.top()

calc = pyCalc()