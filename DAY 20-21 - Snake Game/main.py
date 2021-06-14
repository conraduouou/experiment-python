from turtle import Screen, Turtle
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

# constants
WIDTH = 600
HEIGHT = 600

is_finished = False

# screen object
screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# snake game resources
snake = Snake()
food = Food()
tim = Scoreboard()
over = Turtle()

over.hideturtle()
over.color("white")

# tell screen to listen for keyboard input
screen.onkey(fun=snake.turn_left, key="Left")
screen.onkey(fun=snake.turn_right, key="Right")
screen.onkey(fun=snake.go_down, key="Down")
screen.onkey(fun=snake.go_up, key="Up")
screen.listen()

# try to move the segments
while not is_finished:
    snake.move()

    tim.update()

    if snake.check():
        snake.reset()
        tim.reset()

    if snake.head().distance(food) <= 15:
        snake.grow()
        food.refresh()
        tim.increase()

    if snake.head().xcor() > (WIDTH / 2 - 20) or snake.head().xcor() < -(WIDTH / 2 - 20) or snake.head().ycor() > (HEIGHT / 2 - 20) or snake.head().ycor() < -(HEIGHT / 2 - 20):
        snake.reset()
        tim.reset()

    screen.update()
    time.sleep(0.08)


# exit command
screen.exitonclick()