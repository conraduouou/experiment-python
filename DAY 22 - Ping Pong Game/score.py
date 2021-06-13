from turtle import Turtle

SCORE_COLOR = "white"
SCORE_FONT = ("Courier", 60, "normal")

class Score(Turtle):
    def __init__(self, height):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color(SCORE_COLOR)
        self.sety(height / 2 - 100)

        self.l_score = 0
        self.r_score = 0

        self.update_score()

    def update_score(self):
        """Updates score based on game."""
        self.clear()
        self.write(f"{self.l_score}   {self.r_score}", align="center", font=SCORE_FONT)
    
    def increment_l(self):
        """Adds 1 to left paddle."""
        self.l_score += 1
        self.update_score()

    def increment_r(self):
        """Adds 1 to right paddle."""
        self.r_score += 1
        self.update_score()