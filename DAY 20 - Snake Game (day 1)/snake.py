from turtle import Turtle

# constants
MOVE_DISTANCE = 20
EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270

class Snake:

    def __init__(self):
        """Make a list that comprises of turtles, forming the
        snake segment by segment"""
        self.snake_segments = []
        for i in range(3):
            self.snake_segments.append(Turtle(shape="square"))
            self.snake_segments[i].penup()
            self.snake_segments[i].color("white")
            self.snake_segments[i].setx(-(i * 20))
        
        self.head().color("yellow")

    def head(self):
        """Return snake head, or turtle at snake list index 0."""
        return self.snake_segments[0]
    
    def move(self):
        """Moves the snake according to the heading of the head."""

        # place last segment of the snake to the position of the segment
        # right after it, essentially moving the snake counter-intuitively
        # by moving all the segments behind the "head" before updating.
        for i in range(len(self.snake_segments) - 1, 0, -1):
            self.snake_segments[i].goto(self.snake_segments[i - 1].pos())
        
        self.snake_segments[0].forward(MOVE_DISTANCE)

    # function with no parameters that turns snake left
    def turn_left(self):
        if self.head().heading() != EAST:
            self.head().seth(180)

    # function with no parameters that turns snake right
    def turn_right(self):
        if self.head().heading() != WEST:
            self.head().seth(0)

    # function with no parameters that turns snake up
    def go_up(self):
        if self.head().heading() != SOUTH:
            self.head().seth(90)

    # function with no parameters that turns snake down
    def go_down(self):
        if self.head().heading() != NORTH:
            self.head().seth(270)