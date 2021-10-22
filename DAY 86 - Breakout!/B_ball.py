# Ball class made for ping pong game

from turtle import Turtle

BALL_SHAPE = "circle"
BALL_COLOR = "white"
BALL_SPEED = 16

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape(BALL_SHAPE)
        self.color(BALL_COLOR)
        self.penup()

        self.seth(270)

        self.speed = BALL_SPEED

    def move(self):
        """Moves in respect to ball speed and frame update."""
        self.forward(self.speed)
    
    def collide_object(self, turtle):
        """Checks if it collides with an object, or more exactly, another turtle"""
        if self.distance(turtle) <= 40:
            return True

        return False

    def collide_paddle(self, turtle):
        """Special method that checks if it collides with user paddle."""
        if abs(self.ycor() - turtle.ycor()) <= 15 and self.distance(turtle) <= 70:
            return True
        
        return False
    
    def collide_wall(self, width):
        """Detects if ball bumps left and right walls."""
        if self.xcor() >= width / 2 - 30 or self.xcor() <= -(width / 2 - 30):
            return True
        
        return False

    def collide_top(self, height):
        """Detects if ball bumps the upper wall."""
        if self.ycor() >= height / 2 - 30:
            return True
        return False