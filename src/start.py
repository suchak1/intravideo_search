from view import GUI
import tkinter as tk
from tkinter.ttk import *
from ttkthemes import ThemedTk

def render():
    root = ThemedTk(theme='arc')
    app = GUI(root)
    root.mainloop()

render()
