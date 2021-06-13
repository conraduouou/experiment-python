from turtle import Turtle, Screen
from player import Player
from car import Car
from score import Score
import time, random

# constants
WIDTH = 600
HEIGHT = 600

# screen
screen = Screen()
screen.title("Turtle Crossing")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# player
player = Player((0, -(HEIGHT / 2 - 50)))

# cars list and offset
cars = []
offset = 0 #this offset is for not rendering already went past cars to improve performance

# score or level, more precisely
score = Score((-(WIDTH / 2 - 30), HEIGHT / 2 - 50))

# listen to user command
screen.onkeypress(fun=player.move_up, key="Up")
screen.onkeypress(fun=player.move_up, key="w")
screen.listen()

score.update()

is_finished = False
while not is_finished:
    
    if random.randint(1, 6) == 1:
        cars.append(Car((WIDTH / 2, random.uniform(-(HEIGHT / 2 - 50), HEIGHT / 2 - 50))))
    
    for i in range(offset):
        cars[i].hideturtle()

    j = offset
    while j < len(cars):
        cars[j].move()

        if cars[j].xcor() <= -(WIDTH / 2):
            offset += 1
        elif cars[j].xcor() <= 50 and cars[j].distance(player) <= 30:
            score.game_over()
            is_finished = True
        
        if score.level != 1 and not cars[j].has_multiplied:
            cars[j].add_speed(score.level)
            cars[j].has_multiplied = True
        
        j += 1
    
    if player.ycor() >= HEIGHT / 2 - 20:
        score.level += 1
        score.update()

        player.goto((0, -(HEIGHT / 2 - 50)))
        
    time.sleep(0.07)
    screen.update()

screen.exitonclick()