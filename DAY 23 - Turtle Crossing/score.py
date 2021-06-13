from turtle import Turtle

SCORE_COLOR = "black"
SCORE_FONT = ("Courier", 20, "normal")

class Score(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(position)
        
        self.level = 1
    
    def update(self):
        """Updates current level."""
        self.clear()
        self.write(f"Level: {self.level}", font=SCORE_FONT)

    def game_over(self):
        self.home()
        self.write("GAME OVER", align="center", font=SCORE_FONT)