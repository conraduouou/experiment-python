# objects to break in breakout game
from turtle import Turtle
from random import choice

WIDTH = 3.5
SHAPE = 'square'

COLORS = ['gainsboro', 'dark olive green', 'dark goldenrod', 'purple', 'dark red', 'sea green']

class Object(Turtle):

    def __init__(self, position):
        """Initializes object and puts it in position specified in arguments."""
        super().__init__()
        self.penup()
        self.shape(SHAPE)
        self.color(choice(COLORS))
        self.resizemode('user')
        self.shapesize(stretch_len=WIDTH)
        self.goto(position)

    
    def destroy(self):
        super().hideturtle()