from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from score import Score
import random
import time

# constants
WIDTH = 800
HEIGHT = 600

# screen
screen = Screen()
screen.title("Pong!")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# "net"
net = Turtle()
net.color("white")
net.hideturtle()
net.width(6)
net.penup()
net.goto(0, -(HEIGHT / 2))
while net.ycor() < HEIGHT / 2:
    net.pendown()
    net.goto(0, net.ycor() + 12)
    net.penup()
    net.goto(0, net.ycor() + 14)

# paddles
paddle1 = Paddle((-(WIDTH / 2 - 40), 0))
paddle2 = Paddle((WIDTH / 2 - 40, -(HEIGHT / 2 - 100)))

# ball
ball = Ball()

# score
score = Score(HEIGHT)

# listen to commands
screen.onkeypress(fun=paddle1.go_up, key="w")
screen.onkeypress(fun=paddle1.go_down, key="s")
screen.listen()

print(paddle1.heading())

is_finished = False
while not is_finished:
    ball.move()

    paddle1.collide_wall(HEIGHT)
    paddle2.collide_wall(HEIGHT)

    if ball.collide_paddle(paddle1) or ball.collide_paddle(paddle2):
        if ball.xcor() >= paddle2.xcor() - 20 or ball.xcor() <= paddle1.xcor() + 20:
            if ball.heading() < 90 or ball.heading() > 270:
                ball.seth(random.uniform(110, 250))
                ball.speed *= ball.speed
            else:
                ball.seth(random.uniform(70, -70))
                ball.speed *= ball.speed

    if ball.collide_wall(HEIGHT):
        ball.seth(-(ball.heading()))
        ball.speed *= ball.speed

    if ball.xcor() >= WIDTH / 2:
        score.increment_l()
        ball.home()
        ball.seth(0)
    elif ball.xcor() <= -(WIDTH / 2):
        score.increment_r()
        ball.home()
        ball.seth(180)

    time.sleep(0.05)
    screen.update()



screen.exitonclick()