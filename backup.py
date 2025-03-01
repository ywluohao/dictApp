# v2

# functions for ADD WORD:
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


def play_pron(i):
    if word_d['p' + str(i)].get() != "":
        mp3_file = f"/Users/hao/Documents/dict/sound/{word_d['w' + str(i)].get()}.mp3"
        play(AudioSegment.from_mp3(mp3_file))


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
    update_entry('', word_d['in' + str(i)])
    word_d['ck' + str(i)].deselect()

# add words
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
                              'picture': word_d['j' + str(i)].get(),
                              'pronunciation': word_d['p' + str(i)].get(),
                              'type': word_d['t' + str(i)].get(),
                              'updated_date': date.today(),
                              'status': '0'}
                wdb = wdb.append(new_record, ignore_index=True)
    # backup_db() # to enable this later


def add_words():
    wa = tk.Toplevel(w1)
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
        word_d['in' + str(i)] = tk.Entry(wa, width=5)
        word_d['in' + str(i)].grid(row=i, column=0)
        # delete button
        word_d['e' + str(i)] = tk.Button(wa, text='delete',
                                         command=lambda jj=i: add_delete(str(jj)))
        word_d['e' + str(i)].grid(row=i, column=1)
        # word
        word_d['w' + str(i)] = tk.Entry(wa, width=5)
        word_d['w' + str(i)].grid(row=i, column=2)
        # definition
        word_d['d' + str(i)] = tk.Entry(wa, width=20)
        word_d['d' + str(i)].grid(row=i, column=3)
        # comment
        word_d['c' + str(i)] = tk.Entry(wa, width=10)
        word_d['c' + str(i)].grid(row=i, column=4)
        # picture (jpeg)
        word_d['j' + str(i)] = tk.Entry(wa, width=5)
        word_d['j' + str(i)].grid(row=i, column=5)
        # pronunciation
        word_d['p' + str(i)] = tk.Entry(wa, width=10)
        word_d['p' + str(i)].grid(row=i, column=6)
        # play icon
        word_d['s' + str(i)] = tk.Button(wa, image=sound_icon, width=20,
                                         command=lambda jj=i: play_pron(str(jj)))
        word_d['s' + str(i)].grid(row=i, column=7)
        # type
        word_d['t' + str(i)] = tk.Entry(wa, width=5)
        word_d['t' + str(i)].grid(row=i, column=8)
        # check box
        word_d['ckv' + str(i)] = tk.IntVar()
        word_d['ck' + str(i)] = tk.Checkbutton(wa, var=word_d['ckv' + str(i)])
        word_d['ck' + str(i)].grid(row=i, column=9)
        # all / get box
        word_d['b' + str(i)] = tk.Button(wa, text='get',
                                         command=lambda jj=i: add_pron(str(jj)))
        word_d['b' + str(i)].grid(row=i, column=10)

    # append button
    addt = tk.Text(wa, height=5)
    addt.grid(row=1 + n_word, column=0, columnspan=7)
    addb = tk.Button(wa, command=add_append, text='APPEND', height=2)
    addb.grid(row=1 + n_word, column=8, columnspan=2)
    wa.mainloop()
