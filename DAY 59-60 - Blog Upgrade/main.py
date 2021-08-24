from flask import Flask, render_template, request
from decouple import config
import requests
import smtplib

# Constants
N_EMAIL = config('N_EMAIL')
PASSWORD = config('N_PASSWORD')
MY_EMAIL = config('MY_EMAIL')


app = Flask(__name__)

posts = requests.get('https://api.npoint.io/88c2c1f644ef334058be').json()


@app.route('/')
def home():
    return render_template('index.html', blogs=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])   
def contact():

    def form_message(form_dict):
        message = ""
        for key, value in form_dict.items():
            message += f"{key}: {value}\n"
        
        return message

    if request.method == 'POST':
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
                connection.starttls()
                connection.login(N_EMAIL, PASSWORD)
                connection.sendmail(
                    from_addr=N_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"Subject: Message alert, flover!\n\n" + form_message(request.form)
                )

    return render_template('contact.html', method=request.method)

@app.route('/post/<int:blog_id>')
def post(blog_id):
    return render_template('post.html', post=posts[blog_id - 1], bg=f'id-{blog_id}.jpg')
        


if __name__ == '__main__':
    app.run(debug=True)