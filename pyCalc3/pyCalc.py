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
    version = "3.0.4"

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
            print(self.calculateRPN(self.convertToRPN(self.textbox.get())))
        elif(btn == 'C'):
            self.textbox.delete(0, END)
        elif(btn == 'AC'):
            self.textbox.delete(len(self.textbox.get())-1, END)
        else:
            self.textbox.insert(END, btn)

    def isOperator(self, char):
        return char in ['+','-','*','/','^']

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
        stack = Stack()
        output = []
        for c in text:
            if(c.isdigit()):
                output.append(c)
            elif(self.isOperator(c)):
                for i in range(stack.size()):
                    if(self.priority(c) == 3 or self.priority(c) > self.priority(stack.top())):
                        break
                    output.append(stack.top())
                    stack.pop()
                stack.push(c)
            elif(c == '('):
                stack.push(c)
            elif(c == ')'):
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
            if(c.isdigit()):
                stack.push(c)
            elif(self.isOperator(c)):
                a = stack.top()
                stack.pop()
                b = stack.top()
                stack.pop()
                stack.push(eval(str(a)+c+str(b)))
        return stack.top()

calc = pyCalc()