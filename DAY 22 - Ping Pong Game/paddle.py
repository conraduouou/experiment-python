from turtle import Turtle

MOVE_DISTANCE = 30
PADDLE_COLOR = "white"
PADDLE_SHAPE = "square"
PADDLE_WIDTH = 4
PADDLE_HEIGHT = 1

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape(PADDLE_SHAPE)
        self.color(PADDLE_COLOR)
        self.resizemode("user")
        self.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_HEIGHT, outline=1)
        self.goto(position)
    
    def go_up(self):
        """Tell the screen listener that the paddle goes up."""
        self.goto(self.xcor(), self.ycor() + MOVE_DISTANCE)

    def go_down(self):
        """Tell the screen listener that the paddle goes down."""
        self.goto(self.xcor(), self.ycor() - MOVE_DISTANCE)
    
    def collide_wall(self, height):
        """Takes in window height as parameter to determine if paddle is colliding."""
        if self.ycor() >= height / 2:
            self.sety(height / 2)
        elif self.ycor() <= -(height / 2 - 50):
            self.sety(-(height / 2 - 50)) 