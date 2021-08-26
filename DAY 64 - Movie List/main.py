from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, ValidationError, NumberRange
from decouple import config
import requests

# prerequisites
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)

# dynamically get image base url
response = requests.get(url=f"https://api.themoviedb.org/3/configuration?api_key={config('MOVIE_DB_API')}").json()

IMAGE_BASE_URL = response['images']['secure_base_url']
POSTER_SIZE = 'w500'



# form from wtforms made for updating both the rating and review
class RateMovieForm(FlaskForm):

    rating = fields.FloatField(label="Your Rating out of 10 e.g 7.5", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = fields.StringField(label="Your Review", validators=[DataRequired()])
    submit = fields.SubmitField(label="Done")


# form from wtforms made for adding a movie
class AddMovieForm(FlaskForm):

    title = fields.StringField(label="Movie Title", validators=[DataRequired()])
    submit = fields.SubmitField(label="Add Movie")


# Movie table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=False)
    year = db.Column(db.Integer, unique=False)
    description = db.Column(db.String(400), unique=True)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer, unique=True)
    review = db.Column(db.String(150), unique=False)
    img_url = db.Column(db.String(250), unique=True)


# # commence database creation
# db.create_all()


# main program
@app.route("/")
def home():

    # The hard part wasn't implementing the code -- it was understanding the documentation.
    ## https://docs.sqlalchemy.org/en/14/tutorial/data_select.html#tutorial-order-by
    ## https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying
    ranking = 1
    for instance in Movie.query.order_by(Movie.rating.desc()):
        instance.ranking = ranking
        ranking += 1
    
    db.session.commit()

    return render_template("index.html", movies=Movie.query.order_by(Movie.ranking))


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    form = RateMovieForm()
    movie_to_edit = Movie.query.filter_by(id=request.args.get('id')).first()

    if form.validate_on_submit():
        movie_to_edit.rating = form.rating.data
        movie_to_edit.review = form.review.data
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", movie=movie_to_edit, form=form)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    movie_to_delete = Movie.query.filter_by(id=request.args.get('id')).first()
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()

    if form.validate_on_submit():
        details = {
            "api_key": config('MOVIE_DB_API'),
            "query": form.title.data
        }

        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=details)
        response.raise_for_status()

        results = response.json()['results']

        return render_template('select.html', movies=results)

    return render_template('add.html', form=form)


@app.route('/select')
def select():

    movie_data = requests.get(url=f"https://api.themoviedb.org/3/movie/{request.args.get('id')}?api_key={config('MOVIE_DB_API')}").json()
    image_data = requests.get(url=f"https://api.themoviedb.org/3/movie/{request.args.get('id')}/images?api_key={config('MOVIE_DB_API')}").json()

    new_movie = Movie(
        title=movie_data['title'],
        year=movie_data['release_date'],
        img_url=f"{IMAGE_BASE_URL}/{POSTER_SIZE}{image_data['posters'][0]['file_path']}",
        description=movie_data['overview']
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)