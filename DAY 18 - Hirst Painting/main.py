from turtle import Turtle, Screen
import random
import colorgram


def get_colors(path, number_of_colors):
    to_return = colorgram.extract(path, number_of_colors)
    for i in range(len(to_return)):
        to_return[i] = tuple(to_return[i].rgb)
    
    return to_return


def draw_row(gap, dot_size, turtle, colors):
    for _ in range(10):
        turtle.pendown()
        turtle.dot(dot_size, random.choice(colors))
        turtle.penup()
        turtle.forward(gap)
        
    
screen = Screen()
louise = Turtle()

screen.colormode(255)
louise.speed("fastest")

colors = get_colors('DAY 18 - Hirst Painting\image.jpg', 30)
louise.hideturtle()
louise.penup()

gap = 60
x_pos = -((gap * 10) / 2) + 30
y_pos = -((gap * 10) / 2) + 30

louise.setpos(x_pos, y_pos)

for i in range(10):
    draw_row(gap, 30, louise, colors)
    louise.setpos(x_pos, y_pos + ((i + 1) * gap))

louise.home()

screen.exitonclick()