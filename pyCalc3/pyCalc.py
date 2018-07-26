# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk

class pyCalc:
    version = "3.0.2"

    def __init__(self):
        self.startGui()

    def startGui(self):
        self.root = Tk()
        self.root.title("pyCalc v."+self.version)
        ttk.Style().configure("TButton", padding=(-10,10,-10,10), font=('16'))
        self.textbox = ttk.Entry(self.root, font=('Helvetica', '16'), justify=RIGHT)
        self.textbox.grid(row=0, columnspan=4, sticky=W+E, padx=3, pady=3)
        btnLabels = ['7','8','9','/','4','5','6','*','1','2','3','-','.','0','=','+']
        self.btn = []
        i = 0
        for r in range(1,5):
            for c in range(4):
                self.btn.append(ttk.Button(self.root, text=btnLabels[i]))
                self.btn[i].grid(row=r, column=c, padx=2, pady=2)
                i += 1
        self.btn[0].configure(command=lambda:self.click(btnLabels[0]))
        self.btn[1].configure(command=lambda:self.click(btnLabels[1]))
        self.btn[2].configure(command=lambda:self.click(btnLabels[2]))
        self.btn[3].configure(command=lambda:self.click(btnLabels[3]))
        self.btn[4].configure(command=lambda:self.click(btnLabels[4]))
        self.btn[5].configure(command=lambda:self.click(btnLabels[5]))
        self.btn[6].configure(command=lambda:self.click(btnLabels[6]))
        self.btn[7].configure(command=lambda:self.click(btnLabels[7]))
        self.btn[8].configure(command=lambda:self.click(btnLabels[8]))
        self.btn[9].configure(command=lambda:self.click(btnLabels[9]))
        self.btn[10].configure(command=lambda:self.click(btnLabels[10]))
        self.btn[11].configure(command=lambda:self.click(btnLabels[11]))
        self.btn[12].configure(command=lambda:self.click(btnLabels[12]))
        self.btn[13].configure(command=lambda:self.click(btnLabels[13]))
        self.btn[14].configure(command=lambda:self.click(btnLabels[14]))
        self.btn[15].configure(command=lambda:self.click(btnLabels[15]))
        self.root.mainloop()

    def click(self, btn):
        self.textbox.insert(0, btn)

    def convertToRPN(self):
        pass
calc = pyCalc()