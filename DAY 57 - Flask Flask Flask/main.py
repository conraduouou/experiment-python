from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

response = requests.get('https://api.npoint.io/4af156202f984d3464c3').json()
posts = [Post(post) for post in response]

@app.route('/')
def home():
    return render_template("index.html", blogs=posts)


@app.route('/post/<int:blog_id>')
def blog(blog_id):
    return render_template("post.html", post=posts[blog_id - 1])


if __name__ == "__main__":
    app.run(debug=True)
