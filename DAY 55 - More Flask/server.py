from flask import Flask
import random

app = Flask(__name__)
number = random.randint(0, 9)

@app.route('/')
def home():
    return '<h1>Guess a number between 0 and 9</h1>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'

@app.route('/<int:answer>')
def guess(answer):
    if answer < number:
        return '<h1 style="color: red">Too low! Try again!</h1>' \
               '<img src="https://media.giphy.com/media/9dgnO4jts7kmsFcSPq/giphy.gif">'
    elif answer > number:
        return '<h1 style="color: violet">Too high! Try again!</h1>' \
               '<img src="https://media.giphy.com/media/sEms56zTGDx96/giphy.gif">'
    else:
        return '<h1 style="color: pink">You guessed right!</h1>' \
               '<img src="https://media.giphy.com/media/xwTzbG6rfO81y/giphy.gif">'


if __name__ == '__main__':
    app.run(debug=True)