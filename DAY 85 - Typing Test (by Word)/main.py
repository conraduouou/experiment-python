from tkinter import *
from tkinter import font
import random, time


# constants
WIDTH = 800
HEIGHT = 500

random_words = []

# read words from 1000 most commonly used words
with open('DAY 85 - Typing Test (by Word)/words.txt', 'r') as file:
    words = ''.join(file.readlines()).split('\n')


# start type test
def start():
    random_words.clear()

    for i in range(16):
        while True:
            word_to_append = random.choice(words)
            if len(word_to_append) <= 6:
                break
        
        random_words.append(word_to_append)

    field.config(state=NORMAL)
    field.delete(0, END)
    field.focus()

    word_label.config(text=' '.join(random_words))
    start_button.place_forget()

    start_label.config(text=time.time())
    count_label.config(text='Count: ')
    result_label.place_forget()


# calculate result and show on window
def calculate():
    end_time = time.time()

    window.unbind('<Key>', id)

    user_words = field.get().split(' ')
    field.config(state=DISABLED)

    correct_words = []
    for word in user_words:
        if word in random_words:
            correct_words.append(word)
    
    seconds = end_time - float(start_label['text'])

    wpm = float(len(correct_words)) * (1 + (60 - seconds)/seconds)

    result_label.config(text=f'Your WPM (Word per Minute) is {wpm:.2f}!')
    result_label.place(x=WIDTH/2 - 110, y=HEIGHT - 110)

    start_button.config(text='Try again?')
    start_button.place(x=WIDTH/2 - 40, y=HEIGHT - 80)
    

# update labels
def change(*args):
    if time.time() - float(start_label['text']) >= 60:
        calculate()

    count = len(field.get().split(' ')) - 1

    count_label.config(text='Count: %d' % count)

    if count >= len(random_words):
        new_words = []
        for i in range(16):
            while True:
                word_to_append = random.choice(words)
                if len(word_to_append) <= 6:
                    break
            
            new_words.append(word_to_append)
            random_words.append(word_to_append)
        
        word_label.config(text=' '.join(new_words))


# GUI Program
window = Tk()
window.title('Type Test (By Words!)')
window.minsize(width=WIDTH, height=HEIGHT)
window.resizable(width=False, height=False)

# to update label and count widgets
id = window.bind('<Key>', change)

# placeholders for start timer
start_label = Label()

# window components
field = Entry(width=90, state=DISABLED)
field.place(x=WIDTH/7, y=HEIGHT * 3/5)

word_label = Label()
word_label.place(x=WIDTH/7, y=HEIGHT * 1/5)

count_label = Label(text='Count: ')
count_label.place(x=WIDTH/7, y=HEIGHT * 2/5)

result_label = Label(text='')

start_button = Button(text='Start typing', command=start)
start_button.place(x=WIDTH/2 - 40, y=HEIGHT - 80)


window.mainloop()