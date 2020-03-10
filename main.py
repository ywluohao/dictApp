from datetime import date, datetime
import os
from pydub import AudioSegment
from bs4 import BeautifulSoup
import requests
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep


# user-defined parameters
DIRECTORY = '/Users/hao/Documents/dict'
directory = DIRECTORY   # to delete

if not os.path.exists(DIRECTORY + '/sound'):
    os.mkdir(DIRECTORY + '/sound')

if not os.path.exists(DIRECTORY + '/backup'):
    os.mkdir(DIRECTORY + '/backup')


# word database
wdb = pd.DataFrame(columns=['word', 'definition', 'comment',
                            'pronunciation', 'status', 'updated_date', 'type'])

wdb = wdb.append({'word': 'one',
                  'definition': 'one_definition',
                  'comment': 'one_comment',
                  'pronunciation': 'one_pronunciation',
                  'status': 'one_status',
                  'updated_date': 'one_created_date',
                  'type': 'one_type'}, ignore_index=True)


# def run(option):
#     cur_time = datetime.now().strftime("%m_%d_%H_%M_%S")
#     os.mkdir(e5.get() + '/NewWord_' + cur_time)
#     os.chdir(e5.get() + '/NewWord_' + cur_time)
#
#     txt_file_name = e1.get()
#
#     with open(txt_file_name, 'r') as t:
#         txt = t.readlines()
#
#     word_list = [t[:-1] for t in txt if t[-1] == '\n']
#
#     concat_mp3 = AudioSegment.empty()
#     wrong_list = []
#
#     for i, word in enumerate(word_list, start=1):
#         web = 'https://www.dictionary.com/browse/' + word
#         page = requests.get(web)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         soup2 = soup.find(class_="audio-wrapper css-48y3p0 e1rg2mtf7")
#         if not soup2:
#             wrong_list.append(word)
#             continue
#         url = list(list(soup2.children)[1].children)[1].attrs['src']
#         file_name = str(i) + '_' + word + '.mp3'
#
#         r = requests.get(url)
#         with open(file_name, 'wb') as fn:
#             fn.write(r.content)
#
#         mp3 = AudioSegment.from_mp3(file_name)
#
#         if option == 'mul':
#             silence = int(e2.get()) * mp3.duration_seconds
#         elif option == 'sec':
#             silence = int(e3.get())
#
#         concat_mp3 += mp3
#         concat_mp3 += AudioSegment.silent(duration=1000 * silence)
#
#     concat_mp3.export("_concat.mp3", format="mp3")

def pron(s):
    web = 'https://www.dictionary.com/browse/' + s
    page = requests.get(web)
    soup = BeautifulSoup(page.content, 'html.parser')

    # for the mp3 file
    soup2 = soup.find(class_="audio-wrapper css-48y3p0 e1rg2mtf7")
    if not soup2:
        return False
    url = list(list(soup2.children)[1].children)[1].attrs['src']
    r = requests.get(url)
    with open(DIRECTORY + '/sound/' + s + '.mp3', 'wb') as fn:
        fn.write(r.content)

    # for the phonetic symbol
    soup3 = soup.find(class_="pron-spell-content css-z3mf2 evh0tcl2")
    text = []
    for a in list(soup3.children):
        if isinstance(a, str):
            a = str(a)
            if '\u2009n' in a:
                a = a.replace('\u2009', ' ')
            text.append(a)
        else:
            if a.attrs['class'][0] == 'bold':
                text.append('<b>' + a.text + '</b>')
            elif a.attrs['class'][0] == 'italic':
                text.append('<i>' + a.text + '</i>')
    return ''.join(text)


# r = Tk()
# r.title('dictionary')
#
# l1 = Label(r, text="From")
# l1.grid(row=0, sticky='E')
# e1 = Entry(r, width=50)
# e1.grid(row=0, column=1, columnspan=10)
# Button(r, text='Select', command=getFileName).grid(row=0, column=11)
#
# l5 = Label(r, text="Save to")
# l5.grid(row=1, sticky='E')
# e5 = Entry(r, width=50)
# e5.insert(0, '/Users/hao/Desktop')
# e5.grid(row=1, column=1, columnspan=10)
# Button(r, text='Select', command=getFileName2).grid(row=1, column=11)
#
# l2 = Label(r, text="By multiple of the word length: ")
# l2.grid(row=2, column=0, sticky='E', columnspan=10)
# e2 = Entry(r, width=2)
# e2.insert(0, 2)
# e2.grid(row=2, column=10)
# Button(r, text='Run', command=lambda: run("mul")).grid(row=2, column=11)
#
# l3 = Label(r, text="By waiting for how many seconds: ")
# l3.grid(row=3, column=0, sticky='E', columnspan=10)
# e3 = Entry(r, width=2)
# e3.insert(0, 1)
# e3.grid(row=3, column=10)
# Button(r, text='Run', command=lambda: run("sec")).grid(row=3, column=11)
#
# e4 = Text(r, height=3)
# e4.grid(row=4, columnspan=12)
# r.mainloop()

# general functions for GUI

# m is the message
# w is the text window
# ww is the window


def show_message(m, w, ww):
    w.delete(1.0, tk.END)
    w.insert(tk.END, m)
    ww.update()


def update_entry(m, w):
    w.delete(0, tk.END)
    w.insert(0, m)


# main window functions
def update_directory():
    global directory
    directory = e0.get()
    os.chdir(directory)
    show_message(f'Working directory is updated to {directory}', msg, w1)
    os.system('say "Working directory is updated"')


def load_db():
    if not os.path.isfile(directory + '/db.csv'):
        f = open('db.csv', mode='x')
        f.close()
    global wdb
    wdb = pd.read_csv(directory + '/db.csv')
    show_message('database is loaded!', msg, w1)
    os.system('say "database is loaded"')


def save_db():
    wdb.to_csv(directory + '/db.csv', index=False)


def backup_db():
    wdb.to_csv(directory + '/backup/' +
               str(datetime.now()) + '.csv', index=False)


# to delete
directory = DIRECTORY

# main window GUI


w1 = tk.Tk()
w1.title('dictApp')
w1.geometry('{}x{}'.format(460, 350))

f1 = tk.Frame(w1, bg='cyan', width=450, height=50)
f1.grid(row=0, column=0)
f2 = tk.Frame(w1, bg='blue', width=450, height=300)
f2.grid(row=1, column=0)


l0 = tk.Label(f1, text='directory: ')
l0.grid(row=0, column=0)
e0 = tk.Entry(f1)
e0.grid(row=0, column=1)
e0.insert(0, DIRECTORY)
directory = e0.get()
os.chdir(directory)

b0 = tk.Button(f1, text='Update', command=update_directory)
b0.grid(row=0, column=2)


b1 = tk.Button(f2, text='Load',  command=load_db)
b1.grid(row=1, column=0)


ba = tk.Button(f2, text='Add', command=add)
ba.grid(row=2, column=0)
ea = tk.Entry(f2)
ea.grid(row=2, column=1)
ea.insert(0, 10)


bp = tk.Button(f2, text='Practice')
bp.grid(row=3, column=0)

bt = tk.Button(f2, text='Test')
bt.grid(row=4, column=0)

bm = tk.Button(f2, text='Test Messgae',
               command=lambda: show_message(directory, msg, w1))
bm.grid(row=6, column=0)

msg = tk.Text(f2, height=3)
msg.grid(row=5, column=0, columnspan=3)


w1.mainloop()

# # load window
#
#
# def create_window():
#     w11 = tk.Toplevel(root)
#     w11e = tk.Entry(w11)
#     w11e.grid(row=0, column=0)
#     w11e.insert(0, 1)
#     l.insert(0, w11e.get())
#
#
# root = tk.Tk()
# b = tk.Button(root, text="Create new window", command=create_window)
# l = tk.Entry(root)
#
#
# b.pack()
# l.pack()
#
# root.mainloop()





te = tk.Tk()
sound_icon_ = Image.open("/Users/hao/Documents/dict/icon/sound.png")
sound_icon_.thumbnail((2, 2), Image.ANTIALIAS)
sound_icon = ImageTk.PhotoImage(sound_icon_)

b = tk.Button(te, image=sound_icon,  width='3')

b.grid(row=0, column=0)

te.mainloop()


# add word
def add():
    wa = tk.Toplevel(w1)
    wa = tk.Tk()
    n_word = 10  # int(ea.get())

    sound_icon = ImageTk.PhotoImage(Image.open(
        "/Users/hao/Documents/dict/icon/sound.png"))
    sound_icon.subsample(20, 20)

    def add_ck():
        if (ck_var.get() == 1):
            for i in range(1, 1 + n_word):
                if len(word_d['w' + str(i)].get()) > 0:
                    word_d['ck' + str(i)].select()
        else:
            for i in range(1, 1 + n_word):
                word_d['ck' + str(i)].deselect()

    def add_pron(i):
        word = word_d['w' + str(i)].get()
        spelling = pron(word)
        if spelling == False:
            show_message(word + ' is not found!', addt, wa)
            os.system('say "word is not found"')
        else:
            update_entry(spelling, word_d['p' + str(i)])

    def add_prons():
        word_na = ''
        for i in range(1, 1 + n_word):
            if word_d['ckv' + str(i)].get() == 1:
                word = word_d['w' + str(i)].get()
                spelling = pron(word)
                if spelling == False:
                    word_na += word + ' \n'
                else:
                    update_entry(spelling, word_d['p' + str(i)])
        if len(word_na) == 0:
            show_message('all words are found!', addt, wa)
            os.system('say "all words are found"')
        else:
            show_message(word_na + 'are not found!', addt, wa)
            os.system('say "words are not found"')

    def add_check_db():
        cur_window = []
        for i in range(1, 1 + n_word):
            add_check_db_w = word_d['w' + str(i)].get()
            if len(add_check_db_w) > 0:
                if add_check_db_w in wdb['word'].values:
                    update_entry('found', word_d['in' + str(i)])
                elif add_check_db_w in cur_window:
                    update_entry('dup', word_d['in' + str(i)])
                else:
                    cur_window.append(add_check_db_w)
                    update_entry('NEW', word_d['in' + str(i)])
            else:
                update_entry('', word_d['in' + str(i)])

    def add_delete(i):
        for j in 'wdcpt':
            update_entry('', word_d[j + str(i)])
        update_entry('', word_d['' + str(i)])
        word_d['ck' + str(i)].deselect()

    def add_append():
        # double check the world is not three
        add_append_status = True
        global wdb
        add_check_db()
        for i in range(1, 1 + n_word):
            if word_d['in' + str(i)].get() == 'found':
                show_message("Already in database!")
                os.system('say "Already in database"')
                add_append_status = False
        if add_append_status == True:
            for i in range(1, 1 + n_word):
                if word_d['ckv' + str(i)].get() == 1:
                    new_record = {'word': word_d['w' + str(i)].get(),
                                  'definition': word_d['d' + str(i)].get(),
                                  'comment': word_d['c' + str(i)].get(),
                                  'pronunciation': word_d['p' + str(i)].get(),
                                  'type': word_d['t' + str(i)].get(),
                                  'updated_date': date.today(),
                                  'status': '0'}
                    wdb = wdb.append(new_record, ignore_index=True)
        # backup_db() # to enable this later

    tk.Button(wa, text='in_db', command=add_check_db).grid(row=0, column=0)
    tk.Label(wa, text='word', width=10).grid(row=0, column=2)
    tk.Label(wa, text='definition', width=20).grid(row=0, column=3)
    tk.Label(wa, text='comment', width=10).grid(row=0, column=4)
    tk.Label(wa, text='pronunciation', width=10).grid(row=0, column=5)
    tk.Label(wa, text='type', width=10).grid(row=0, column=7)
    ck_var = tk.IntVar()
    tk.Checkbutton(wa, variable=ck_var, command=add_ck).grid(row=0, column=8)
    tk.Button(wa, text='ALL', command=add_prons).grid(row=0, column=9)

    word_d = {}
    for i in range(1, 1 + n_word):
        for n, j in enumerate('wdcp', start=2):
            word_d[j + str(i)] = tk.Entry(wa)
            word_d[j + str(i)].grid(row=i, column=n)
        word_d['s' + str(i)] = tk.Button(wa, image=sound_icon, width=5,
                                         command=lambda jj=i: add_pron(str(jj)))
        word_d['s' + str(i)].grid(row=i, column=6)
        word_d['t' + str(i)] = tk.Entry(wa)
        word_d['t' + str(i)].grid(row=i, column=7)
        word_d['ckv' + str(i)] = tk.IntVar()
        word_d['ck' + str(i)] = tk.Checkbutton(wa, var=word_d['ckv' + str(i)])
        word_d['ck' + str(i)].grid(row=i, column=8)
        word_d['b' + str(i)] = tk.Button(wa, text='get',
                                         command=lambda jj=i: add_pron(str(jj)))
        word_d['b' + str(i)].grid(row=i, column=9)
        word_d['e' + str(i)] = tk.Button(wa, text='delete',
                                         command=lambda jj=i: add_delete(str(jj)))
        word_d['e' + str(i)].grid(row=i, column=1)
        word_d['in' + str(i)] = tk.Entry(wa, width=5)
        word_d['in' + str(i)].grid(row=i, column=0)

    addt = tk.Text(wa, height=5)
    addt.grid(row=1 + n_word, column=0, columnspan=6)
    addb = tk.Button(wa, command=add_append, text='APPEND', height=2)
    addb.grid(row=1 + n_word, column=7, columnspan=2)
    wa.mainloop()
