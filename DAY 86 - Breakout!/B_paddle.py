# Modified paddle class made for ping pong game

from turtle import Turtle

MOVE_DISTANCE = 30
PADDLE_COLOR = "white"
PADDLE_SHAPE = "square"
PADDLE_WIDTH = 1
PADDLE_HEIGHT = 6

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape(PADDLE_SHAPE)
        self.color(PADDLE_COLOR)
        self.resizemode("user")
        self.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_HEIGHT, outline=1)
        self.goto(position)
    
    def go_right(self):
        """Tell the screen listener that the paddle goes up."""
        self.goto(self.xcor() + MOVE_DISTANCE, self.ycor())

    def go_left(self):
        """Tell the screen listener that the paddle goes down."""
        self.goto(self.xcor() - MOVE_DISTANCE, self.ycor())
    
    def collide_wall(self, width):
        """Takes in window width as parameter to determine if paddle is colliding."""
        if self.xcor() >= width / 2 - 50:
            self.setx(width / 2 - 50)
        elif self.xcor() <= -(width / 2 - 50):
            self.setx(-(width / 2 - 50)) 