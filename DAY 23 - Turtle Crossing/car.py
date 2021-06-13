from turtle import Turtle
import random

CAR_SHAPE = "square"
CAR_SPEED = 6
SPEED_MULTIPLIER = 1.4

class Car(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.seth(180)
        self.color((random.random(), random.random(), random.random()))
        self.shape(CAR_SHAPE)
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.goto(position)
        
        self.speed = CAR_SPEED
        self.has_multiplied = False
    
    def move(self):
        """Makes the car move in a constant speed."""
        self.forward(self.speed)
    
    def add_speed(self, level):
        """Multiply speed accordingly to level passed."""
        self.speed *= SPEED_MULTIPLIER ** level