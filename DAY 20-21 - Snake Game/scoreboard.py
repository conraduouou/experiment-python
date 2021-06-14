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

        with open("DAY 20-21 - Snake Game\score.txt") as f:
            self.high_score = int(f.read())

    
    def update(self):
        """Updates score on screen."""
        self.clear()
        self.write(f"Score: {self.score}  High Score: {self.high_score}", move=False, align=ALIGN, font=FONT)
    
    def increase(self):
        """Increases score by one."""
        self.score += 1
        self.update()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score

            with open("DAY 20-21 - Snake Game\score.txt", mode="w") as f:
                f.write(f"{self.high_score}")
        self.score = 0
        


    # def game_over(self):
    #     """Initiates game over sequence."""
    #     self.home()
    #     self.write("GAME OVER", move=False, align=ALIGN, font=FONT)