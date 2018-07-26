# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk

class pyCalc:
    version = "3.0.1"

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
        self.root.mainloop()

calc = pyCalc()