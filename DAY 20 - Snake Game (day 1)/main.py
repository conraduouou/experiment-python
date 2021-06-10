from turtle import Screen, Turtle
from snake import Snake
import time

# constants
WIDTH = 600
HEIGHT = 600

# screen object
screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# snake segments declaration
snake = Snake()


# tell screen to listen for keyboard input
screen.onkey(fun=snake.turn_left, key="Left")
screen.onkey(fun=snake.turn_right, key="Right")
screen.onkey(fun=snake.go_down, key="Down")
screen.onkey(fun=snake.go_up, key="Up")
screen.listen()

# try to move the segments
while True:
    snake.move()

    screen.update()
    time.sleep(0.1)


# exit command
screen.exitonclick()