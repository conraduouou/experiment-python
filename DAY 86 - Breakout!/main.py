from turtle import Turtle, Screen
from B_paddle import Paddle
from B_object import Object
from B_ball import Ball, BALL_SPEED
import random
import time


# screen size constants
WIDTH = 800
HEIGHT = 600
is_finished = False

# screen config
screen = Screen()
screen.title('Breakout!')
screen.bgcolor('#00162B')
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)        # kind of like the controller for the frame animation

# ball config
ball = Ball()
SPEED_MULTIPLIER = 1.01

# paddle config
user = Paddle((0, -(HEIGHT/4)))
screen.onkeypress(fun=user.go_left, key="a")
screen.onkeypress(fun=user.go_right, key="d")
screen.listen()

# objects config
X_GAP = 80
Y_GAP = 40

objects = []
for k in range(4):
    x_offset = 37 if k % 2 == 0 else 0

    i = 0
    while i < 11 - (x_offset / 37):
        objects.append(Object((-(WIDTH/2) + x_offset + (X_GAP * i), HEIGHT/2 - 20 - (Y_GAP * k))))
        i += 1

while not is_finished:
    if len(objects) == 0:
        is_finished = True
        break

    # check objects list if ball collides with one of its components
    for object in objects:
        if ball.collide_object(object):
            ball.seth(-ball.heading() + random.randint(-30, 30))

            # the turtle object still exists, but is invisible, and goes undetected when checked
            object.destroy()        # just a little nuance, but merely hides the object
            objects.remove(object)

            ball.speed *= SPEED_MULTIPLIER
            break

    # sets the angle of the ball to negative, which effectively flips its direction
    if ball.collide_paddle(user):
        ball.sety(user.ycor() + 16)     # to avoid clipping
        ball.seth(-ball.heading())

    # this one was a little tricky when trying to solve the problem head on.
    # you have to set the angle of the ball to negative, and then add 180 to it in
    # order to emulate change of direction to the right or left
    if ball.collide_wall(WIDTH):

        # to avoid clipping
        if ball.xcor() > 0:
            ball.setx(WIDTH/2 - 31)
        else:
            ball.setx(-(WIDTH/2 - 31))

        ball.seth(-ball.heading() + 180 + random.randint(-20, 20))
        ball.speed *= SPEED_MULTIPLIER

    if ball.collide_top(HEIGHT):
        ball.sety(HEIGHT/2 - 31)        # to avoid clipping
        ball.seth(-ball.heading() + random.randint(-20, 20))
        ball.speed *= SPEED_MULTIPLIER

    if ball.ycor() <= -(HEIGHT/2):
        ball.goto(0, HEIGHT/7)
        ball.speed = BALL_SPEED
        ball.seth(270)

    user.collide_wall(WIDTH)

    ball.move()
    user.setx(ball.xcor())      # comment line to remove AI player

    time.sleep(0.02)
    screen.update()


screen.exitonclick()