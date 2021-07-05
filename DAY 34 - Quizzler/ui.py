from tkinter import *
from quiz_brain import QuizBrain

from numpy import pad

THEME_COLOR = "#375362"
PADDING = 20
FONT = ("Arial", 20, "italic")


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()

        # config window and setup interface
        self.window.title("Quizzler")
        self.window.config(padx=PADDING, pady=PADDING, bg=THEME_COLOR)

        self.score_text = Label(text=f"Score: {self.quiz.score}", bg=THEME_COLOR, fg="white")
        self.score_text.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150, 
            125, 
            width=280,
            text="Does it work?", 
            font=FONT, 
            fill=THEME_COLOR)

        self.canvas.grid(row=1, column=0, columnspan=2, pady=PADDING)

        true_img  = PhotoImage(file="DAY 34 - Quizzler/images/true.png")
        false_img = PhotoImage(file="DAY 34 - Quizzler/images/false.png")


        self.true_button  = Button(image=true_img, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)
        self.false_button = Button(image=false_img, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You reached the end.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    # button commands
    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        color = "green" if is_right else "red"

        self.canvas.config(bg=color)

        self.score_text.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)