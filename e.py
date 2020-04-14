from tkinter import *
from itertools import product

def new_Text(root, w=10, h=2, hb="black", ht=1):
    return Text(master=root, width=w, height=h,
               highlightbackground=hb, highlightthickness=ht)


root = Tk()
text = new_Text(root)
text.grid(row=0, column=0, padx=10)
text.tag_configure("red", foreground="red")
text.highlight_pattern("word", "red")

root.mainloop()
