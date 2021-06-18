from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    reps = 0
    
    window.after_cancel(timer)
    timer_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    check.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps == 8:
        count_down(long_break_sec)
        timer_label.config(text="Break", font=(FONT_NAME, 40), fg=RED, bg=YELLOW)
    elif reps % 2 == 1:
        count_down(work_sec)
        timer_label.config(text="Work", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
    else:
        count_down(short_break_sec)
        timer_label.config(text="Break", font=(FONT_NAME, 40), fg=PINK, bg=YELLOW)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    minute = math.floor(count / 60)
    second = count % 60

    canvas.itemconfig(timer_text, text=f"{minute:02d}:{second:02d}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if reps % 2 == 0:
            to_print = ""
            work_sessions = int(reps / 2)
            for _ in range(work_sessions):
                to_print += "✔"
            
            check.config(text=to_print, font=(FONT_NAME, 10), bg=YELLOW, fg=GREEN)
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("ポモドロ")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato = PhotoImage(file="DAY 28 - Pomodoro/tomato.png")
canvas.create_image(100, 112, image=tomato)
timer_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="Start", command=start_timer, highlightthickness=0)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", command=reset_timer, highlightthickness=0)
reset_button.grid(row=2, column=2)

check = Label(font=(FONT_NAME, 10), bg=YELLOW, fg=GREEN)
check.grid(row=3, column=1)



window.mainloop()