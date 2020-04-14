from datetime import date, datetime
import os
from pydub import AudioSegment
from pydub.playback import play
from bs4 import BeautifulSoup
import requests
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep


# user-defined parameters
DIRECTORY = '/Users/hao/Documents/dict'
directory = DIRECTORY   # to delete


def check_path(n):
    if not os.path.exists(DIRECTORY + n):
        os.mkdir(DIRECTORY + n)


check_path('/sound')
check_path('/pic')
check_path('/backup')

sound_icon_ = Image.open("/Users/hao/Documents/dict/icon/sound.png")
sound_icon_.thumbnail((20, 20), Image.ANTIALIAS)

# word database
wdb = pd.DataFrame(columns=['word', 'definition', 'comment', 'picture',
                            'pronunciation', 'status', 'updated_date', 'type'])

wdb = wdb.append({'word': 'one',
                  'definition': 'one_definition',
                  'comment': 'one_comment',
                  'picture': 'one_picture',
                  'pronunciation': 'one_pronunciation',
                  'status': 'one_status',
                  'updated_date': 'one_created_date',
                  'type': 'one_type'}, ignore_index=True)
wdb = wdb.append({'word': 'two',
                  'definition': 'two_definition',
                  'comment': 'two_comment',
                  'picture': 'two_picture',
                  'pronunciation': 'two_pronunciation',
                  'status': 'two_status',
                  'updated_date': 'two_created_date',
                  'type': 'two_type'}, ignore_index=True)
wdb = wdb.append({'word': 'three',
                  'definition': 'three_definition',
                  'comment': 'three_comment',
                  'picture': 'three_picture',
                  'pronunciation': 'three_pronunciation',
                  'status': 'three_status',
                  'updated_date': 'three_created_date',
                  'type': 'three_type'}, ignore_index=True)


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


# tkinter setting:
def Text_new(root, w=10, h=3, hb="black", ht=1):
    return tk.Text(master=root, width=w, height=h,
                   highlightbackground=hb, highlightthickness=ht)


def Text_get(t):
    return t.get('1.0', tk.END).strip()


def Text_update(t, m, w):
    t.delete('1.0', tk.END)
    t.insert(tk.END, m)
    w.update()


def Entry_update(e, m):
    e.delete(0, tk.END)
    e.insert(0, m)


# [ he-<b>loh</b>, h<i>uh</i>-, <b>hel</b>-oh ]
orignal = "[ he-<b>loh</b>, h<i>uh</i>-, <b>hel</b>-oh ]"
bold = []
italics = []

for index, char in enumerate(orignal):
    if char == "<":
        if orignal[index+1] == 'b':
            bold.append(index)
        elif orignal[index+1:index+3] == '/b':
            bold.append(index)
        elif orignal[index+1] == 'i':
            italics.append(index)
        elif orignal[index+1:index+3] == '/i':
            italics.append(index)

orignal[bold[0]:bold[0]+3]
orignal[bold[1]:bold[1]+4]


bold

def Text_format(t):
    orignal = Text_get(t)
    bold = []
    for _ in range(orignal.count('<b>')):
        bold.append()

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


# main window functions
def update_directory():
    global directory
    directory = e0.get()
    os.chdir(directory)
    Text_update(msg, f'Working directory is updated to {directory}', w1)
    os.system('say "Working directory is updated"')


def load_db():
    if not os.path.isfile(directory + '/db.csv'):
        f = open('db.csv', mode='x')
        f.close()
    global wdb
    wdb = pd.read_csv(directory + '/db.csv')
    Text_update(msg, 'database is loaded!', w1)
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
               command=lambda: Text_update(msg, directory, w1))
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


#
# # this is a is work!
# te = tk.Tk()
# sound_icon_ = Image.open("/Users/hao/Documents/dict/icon/sound.png")
# sound_icon_.thumbnail((20, 20), Image.ANTIALIAS)
# sound_icon = ImageTk.PhotoImage(sound_icon_)
#
# b = tk.Button(te, image=sound_icon,  width='30')
#
# b.grid(row=0, column=0)
#
# te.mainloop()


# functions for ADD WORD:
def add_ck():
    if (ck_var.get() == 1):
        for i in range(1, 1 + n_word):
            if len(Text_get(word_d['w' + str(i)])) > 0:
                word_d['ck' + str(i)].select()
    else:
        for i in range(1, 1 + n_word):
            word_d['ck' + str(i)].deselect()





def add_pron(i):
    word = Text_get(word_d['w' + str(i)])
    spelling = pron(word)
    if spelling == False:
        Text_update(addt, word + ' is not found!', wa)
        os.system('say "word is not found"')
    else:
        Text_update(word_d['p' + str(i)], spelling, wa)


def play_pron(i):
    if Text_get(word_d['p' + str(i)]) != "":
        mp3_file = f"/Users/hao/Documents/dict/sound/{Text_get(word_d['w' + str(i)])}.mp3"
        play(AudioSegment.from_mp3(mp3_file))


def add_prons():
    word_na = ''
    for i in range(1, 1 + n_word):
        if word_d['ckv' + str(i)].get() == 1:
            word = Text_get(word_d['w' + str(i)])
            spelling = pron(word)
            if spelling == False:
                word_na += word + ' \n'
            else:
                Text_update(word_d['p' + str(i)], spelling, wa)
    if len(word_na) == 0:
        Text_update(addt, 'all words are found!', wa)
        os.system('say "all words are found"')
    else:
        Text_update(addt, word_na + 'are not found!', wa)
        os.system('say "words are not found"')


def add_check_db():
    cur_window = []
    for i in range(1, 1 + n_word):
        add_check_db_w = Text_get(word_d['w' + str(i)])
        if len(add_check_db_w) > 0:
            if add_check_db_w in wdb['word'].values:
                word_d['in' + str(i)].configure(text='found', bg='red')
            elif add_check_db_w in cur_window:
                word_d['in' + str(i)].configure(text='dup', bg='red')
            else:
                cur_window.append(add_check_db_w)
                word_d['in' + str(i)].configure(text='NEW', bg='green')
        else:
            word_d['in' + str(i)].configure(text='')


def add_delete(i):
    for j in 'wdcjpt':
        word_d[j + str(i)].delete('1.0', tk.END)
    word_d['in' + str(i)].configure(text='', bg='white')
    word_d['ck' + str(i)].deselect()


def add_append():
    # double check the world is not three
    add_append_status = True
    global wdb
    add_check_db()
    for i in range(1, 1 + n_word):
        if len(Text_get(word_d['in' + str(i)])) > 0:
            if word_d['in' + str(i)]["text"] == 'found':
                Text_update(addt, "Already in database!", wa)
                os.system('say "Already in database"')
                add_append_status = False
                break
            if word_d['ckv' + str(i)].get() == 0:
                Text_update(addt, "Not all words are selected", wa)
                os.system('say "Not all words are selected"')
                add_append_status = False
                break
    if add_append_status == True:
        for i in range(1, 1 + n_word):
            new_record = {'word': Text_get(word_d['w' + str(i)]),
                          'definition': Text_get(word_d['d' + str(i)]),
                          'comment': Text_get(word_d['c' + str(i)]),
                          'picture': Text_get(word_d['j' + str(i)]),
                          'pronunciation': Text_get(word_d['p' + str(i)]),
                          'type': Text_get(word_d['t' + str(i)]),
                          'updated_date': date.today().strftime("%Y/%m/%d"),
                          'status': '0'}
            wdb = wdb.append(new_record, ignore_index=True)
    # backup_db() # to enable this later


# add words
def add_words():

    # wa = tk.Toplevel(w1)
    wa = tk.Tk()
    n_word = 10  # int(ea.get())

    tk.Button(wa, text='in_db', command=add_check_db).grid(row=0, column=0)
    tk.Label(wa, text='word', width=5).grid(row=0, column=2)
    tk.Label(wa, text='definition', width=20).grid(row=0, column=3)
    tk.Label(wa, text='comment', width=10).grid(row=0, column=4)
    tk.Label(wa, text='picture', width=5).grid(row=0, column=5)
    tk.Label(wa, text='pronunciation', width=10).grid(row=0, column=6)
    tk.Label(wa, text='type', width=5).grid(row=0, column=8)
    ck_var = tk.IntVar()
    tk.Checkbutton(wa, variable=ck_var, command=add_ck).grid(row=0, column=9)
    tk.Button(wa, text='ALL', command=add_prons).grid(row=0, column=10)

    word_d = {}
    sound_icon = ImageTk.PhotoImage(sound_icon_)
    for i in range(1, 1 + n_word):
        # in_db
        word_d['in' + str(i)] = tk.Label(wa, width=5)
        word_d['in' + str(i)].grid(row=i, column=0, padx=1, pady=1)
        # delete button
        word_d['e' + str(i)] = tk.Button(wa, text='-', width=2,
                                         command=lambda jj=i: add_delete(str(jj)))
        word_d['e' + str(i)].grid(row=i, column=1, padx=1, pady=1)
        # word
        word_d['w' + str(i)] = Text_new(wa, 10)
        word_d['w' + str(i)].grid(row=i, column=2, padx=1, pady=1)
        # definition
        word_d['d' + str(i)] = Text_new(wa, 50)
        word_d['d' + str(i)].grid(row=i, column=3, padx=1, pady=1)
        # comment
        word_d['c' + str(i)] = Text_new(wa, 20)
        word_d['c' + str(i)].grid(row=i, column=4, padx=1, pady=1)
        # picture (jpeg)
        word_d['j' + str(i)] = Text_new(wa, 10)
        word_d['j' + str(i)].grid(row=i, column=5, padx=1, pady=1)
        # pronunciation
        word_d['p' + str(i)] = Text_new(wa, 20)
        word_d['p' + str(i)].grid(row=i, column=6, padx=1, pady=1)
        # play icon
        word_d['s' + str(i)] = tk.Button(wa, image=sound_icon, width=20,
                                         command=lambda jj=i: play_pron(str(jj)))
        word_d['s' + str(i)].grid(row=i, column=7, padx=1, pady=1)
        # type
        word_d['t' + str(i)] = Text_new(wa, 10)
        word_d['t' + str(i)].grid(row=i, column=8, padx=1, pady=1)
        # check box (ckv: check value)
        word_d['ckv' + str(i)] = tk.IntVar()
        word_d['ck' + str(i)] = tk.Checkbutton(wa, var=word_d['ckv' + str(i)])
        word_d['ck' + str(i)].grid(row=i, column=9, padx=1, pady=1)
        # all / get box
        word_d['b' + str(i)] = tk.Button(wa, text='get',
                                         command=lambda jj=i: add_pron(str(jj)))
        word_d['b' + str(i)].grid(row=i, column=10, padx=1, pady=1)

    # append button
    addt = Text_new(wa, 120, 5)
    addt.grid(row=1 + n_word, column=0, columnspan=7)
    addb = tk.Button(wa, command=add_append, text='APPEND', height=2)
    addb.grid(row=1 + n_word, column=8, columnspan=2)
    wa.mainloop()



wdb
