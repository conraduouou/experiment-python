from turtle import Turtle

PLAYER_SHAPE = "turtle"
PLAYER_COLOR = "black"
PLAYER_SPEED = 10

class Player(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape(PLAYER_SHAPE)
        self.color(PLAYER_COLOR)
        self.seth(90)
        self.goto((position))

    def move_up(self):
        """Function passed to screen in order for player to move up."""
        self.forward(PLAYER_SPEED)