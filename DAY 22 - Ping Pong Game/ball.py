from turtle import Turtle
import random

BALL_SHAPE = "circle"
BALL_COLOR = "white"
BALL_SPEED = 20
SPEED_MULTIPLIER = 1.1

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape(BALL_SHAPE)
        self.color(BALL_COLOR)
        self.penup()

        # self.seth(0) if random.randint(0,1) == 1 else self.seth(180)
        self.seth(180)

        self.speed = SPEED_MULTIPLIER

    def move(self):
        """Moves in respect to ball speed and frame update."""
        self.forward(BALL_SPEED * self.speed)
    
    def collide_paddle(self, turtle):
        """Checks if it collides with a paddle, or more exactly, another turtle"""
        if self.distance(turtle) <= 50:
            return True

        return False
    
    def collide_wall(self, height):
        """Detects if ball goes over or below wall."""
        if self.distance(self.xcor(), height / 2) <= 20 or self.distance(self.xcor(), -(height / 2)) <= 20:
            return True
        
        return False
