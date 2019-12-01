from view import GUI
import tkinter as tk
from tkinter.ttk import *
from ttkthemes import ThemedTk

async def render():
    root = ThemedTk(theme='arc')
    app = await GUI(root)
    root.mainloop()

await render()
