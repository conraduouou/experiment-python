from tkinter import *
from tkinter import messagebox
from numpy import row_stack
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
CARD_WIDTH = 800
CARD_HEIGHT = 526
FONT = "Arial"
chosen_word = {}

# button commands
def correct():
    global chosen_word, words_to_learn

    try:
        words_to_learn = words_to_learn.drop(chosen_word["English"], axis=0)
        kanji.remove(chosen_word)
        generate_new_word()
    except:
        canvas.itemconfig(card_image, image=card_frontimg)
        canvas.itemconfig(lng_text, text="Well Done!", fill="black")
        canvas.itemconfig(wrd_text, text="You answered all the cards!", fill="black", font=(FONT, 40, "bold"))
        canvas.itemconfig(rji_text, text="")


def wrong():
    generate_new_word()


def generate_new_word():
    global chosen_word, flip_timer
    window.after_cancel(flip_timer)

    chosen_word = random.choice(kanji)

    canvas.itemconfig(card_image, image=card_frontimg)
    canvas.itemconfig(lng_text, text="Japanese", fill="black")
    canvas.itemconfig(wrd_text, text=chosen_word["Japanese"], fill="black")
    canvas.itemconfig(rji_text, text=chosen_word["Pronunciation"], fill="black")

    flip_timer = window.after(3000, func=change)


def change():
    canvas.itemconfig(card_image, image=card_backimg)
    canvas.itemconfig(lng_text, text="English", fill="white")
    canvas.itemconfig(wrd_text, text=chosen_word["English"], fill="white")
    canvas.itemconfig(rji_text, text="")


# window
window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Japanese CSV
try:
    data = pandas.read_csv("DAY 31 - Flashcards/data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("DAY 31 - Flashcards/data/japanese_words.csv")
else:
    is_reset = messagebox.askyesno(title="Reset", message="Save found. \nDo you want to start from scratch?")

    if is_reset:
        data = pandas.read_csv("DAY 31 - Flashcards/data/japanese_words.csv")

finally:
    kanji = data.to_dict(orient="records")
    words_to_learn = pandas.DataFrame(kanji)
    words_to_learn = words_to_learn.set_index("English")


flip_timer = window.after(3000, func=change)

# PhotoImages
card_frontimg = PhotoImage(file="DAY 31 - Flashcards/images/card_front.png")
card_backimg  = PhotoImage(file="DAY 31 - Flashcards/images/card_back.png")
wrong_buttonimg = PhotoImage(file="DAY 31 - Flashcards/images/wrong.png")
right_buttonimg = PhotoImage(file="DAY 31 - Flashcards/images/right.png")

# card
canvas = Canvas()
canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_image = canvas.create_image(CARD_WIDTH/2, CARD_HEIGHT/2,  image=card_frontimg)
lng_text = canvas.create_text(400, 150, text="", font=(FONT, 40, "italic"))
wrd_text = canvas.create_text(400, 263, text="", font=(FONT, 60, "bold"))
rji_text = canvas.create_text(400, 340, text="", font=(FONT, 24))

canvas.grid(row=0, column=0, columnspan=2)

# buttons
wrong_button = Button(image=wrong_buttonimg, bg=BACKGROUND_COLOR, command=wrong)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_buttonimg, bg=BACKGROUND_COLOR, command=correct)
right_button.grid(row=1, column=1)

generate_new_word()

window.mainloop()

if len(kanji) != 0:
    words_to_learn = words_to_learn.reset_index()
    words_to_learn = words_to_learn.set_index("Japanese")
    words_to_learn.to_csv("DAY 31 - Flashcards/data/words_to_learn.csv")