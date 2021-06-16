import turtle
import pandas

# image constant
IMAGE = "DAY 25 - States Game/blank_states_img.gif"

states = pandas.read_csv("DAY 25 - States Game/50_states.csv")

# writer turtle
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

# screen from turtle
screen = turtle.Screen()
screen.title("US States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

is_finished = False
guessed_states = []

while not is_finished:
    answer_state = screen.textinput(title=f"Guess the State {len(guessed_states)}/50", prompt="Name a state: ")
    if answer_state == None or len(guessed_states) == 50:
        is_finished = True
    elif answer_state.title() in states["state"].tolist():
        guessed_states.append(answer_state.title())
        states_row = states[states["state"] == answer_state.title()]
        x_pos = int(states_row["x"])
        y_pos = int(states_row["y"])

        writer.goto(x_pos, y_pos)
        writer.write(answer_state.title())

states_to_learn = []
for state in states["state"].tolist():
    if state not in guessed_states:
        states_to_learn.append(state)

new_data = pandas.DataFrame(states_to_learn)
new_data.to_csv("DAY 25 - States Game\states_to_learn.csv")

turtle.mainloop()