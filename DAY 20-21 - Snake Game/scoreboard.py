from turtle import Turtle

ALIGN = "center"
FONT = ("Courier", 12, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 250)
        self.pendown()

        self.score = 0
    
    def update(self):
        """Updates score on screen."""
        self.clear()
        self.write(f"Score: {self.score}", move=False, align=ALIGN, font=FONT)
    
    def increase(self):
        """Increases score by one."""
        self.score += 1
        self.update()

    def game_over(self):
        """Initiates game over sequence."""
        self.penup()
        self.home()
        self.pendown()
        self.write("GAME OVER", move=False, align=ALIGN, font=FONT)