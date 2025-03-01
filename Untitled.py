import time
import tkinter as tk


window = tk.Tk()
window.title('My Window')
window.geometry('100x100')

l = tk.Label(window, bg='white', width=20, text='empty')
l.pack()


def print_selection():
    if (var1.get() == 1) & (var2.get() == 0):
        l.config(text='I love Python ')
    elif (var1.get() == 0) & (var2.get() == 1):
        l.config(text='I love C++')
    elif (var1.get() == 0) & (var2.get() == 0):
        l.config(text='I do not anything')
    else:
        l.config(text='I love both')


var1 = tk.IntVar(value=1)
var2 = tk.IntVar(value=1)
c1 = tk.Checkbutton(window, text='Python', variable=var1,
                    onvalue=1, offvalue=0, command=print_selection)
c1.pack()
c2 = tk.Checkbutton(window, text='C++', variable=var2,
                    onvalue=1, offvalue=0, command=print_selection)
c2.pack()

window.mainloop()


for i in range(2):
    print(type(i))


a = {}
a['as'] = 123
a


def p():
    # a = {}
    a['b'] = 11
    print(a)


p()
a


app = tk.Tk()


chkExample = tk.Checkbutton(app, text='Check Box')
chkExample.grid(column=0, row=0)
print(str(chkExample))


app.mainloop()


aa = 'abs \n  bb \n'
print(aa)


top = tk.Tk()
top.geometry('{}x{}'.format(460, 350))

def addText():

    # make first change
    oldText = L.cget("text")
    newText = oldText + '\nfirst change'
    L.configure(text=newText)

    # wait 2 seconds
    top.update_idletasks()
    # time.sleep(2)

    # make second change
    newText += '\nsecond change'
    L.configure(text=newText)

B = tk.Button(top, text="Change text", command=addText)
L = tk.Label(top, text='orignal text')

B.pack()
L.pack()
top.mainloop()


aa = 'asd'
if aa:
    print(True)
else:
    print(False)
