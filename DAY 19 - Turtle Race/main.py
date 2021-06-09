from turtle import Turtle, Screen
import random

# CONSTANTS
WIDTH = 500
HEIGHT = 400
START_X = -230

# screen object
screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
user_bet = screen.textinput(title="WHO WILL WIN?!?!?", prompt="What color do you think will win?: ")

# colors that the turtles will take on
colors = ["red", "orange", "yellow", "green", "blue", "indigo"]

# turtles that will race each other
turtle = []
for i in range(len(colors)):
    turtle.append(Turtle(shape="turtle"))
    turtle[i].penup()
    turtle[i].speed("slow")
    turtle[i].color(colors[i])
    turtle[i].goto(x=START_X, y=(125 + -(i * 45)))

if user_bet:
    is_race_on = True

while is_race_on:
    for t in turtle:
        t.forward(random.randint(0, 10))

        if t.xcor() > (WIDTH / 2) - 20:
            is_race_on = False
            winning_color = t.pencolor()
            
            # make new turtle to write result
            tim = Turtle()
            tim.penup()
            tim.goto(x=-(WIDTH / 2 - 100), y=-(HEIGHT / 2 - 50))
            tim.pendown()
            tim.speed("slow")

            # write results
            if winning_color == user_bet:
                tim.write(f"You WON! {user_bet.title()} won!", True, align="left",
                            font=("Impact", 30, "normal"))
            else:
                tim.write(f"You LOST! {winning_color.title()} won!", True, align="left",
                            font=("Impact", 30, "normal"))
                

screen.exitonclick()