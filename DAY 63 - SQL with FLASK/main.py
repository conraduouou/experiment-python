from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# knowing that my db object contains all the data from my new-books-collection.db file via the SQLAlchemy instantiation
# with the app object as an argument, the Book class having all the data makes sense since it inherits all of it through
# the Model subclass.
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# main program
@app.route('/')
def home():
    return render_template('index.html', books=Book.query.all())


# add book page
@app.route("/add", methods=["POST", "GET"])
def add():

    # get data from POST request and add book data to database
    if request.method == 'POST':
        new_book = Book(title=request.form['name'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
    
        return redirect(url_for('home'))

    # display page with GET request
    return render_template('add.html')


# edit rating page
@app.route("/edit", methods=['POST', 'GET'])
def change_rating():

    # if the change has been done, it is then treated as a POST request, to which we will now be able to access
    # the data passed, therefore changing the information in the database.
    if request.method == 'POST':
        book_id = int(request.form['id'])
        to_update = Book.query.filter_by(id=book_id).first()
        to_update.rating = float(request.form['rating'])
        db.session.commit()
        
        return redirect(url_for('home'))

    # if edit rating is clicked on the home page, the url_for function in the anchor tag passes the book id
    # it corresponds to as an argument. Seeing that this function does not receive any arguments formally, flask
    # then treats it as a GET request, with the argument appended in the link after a question mark.

    # this then raises the question, how should I get that data from the link? fortunately, flask handles that as
    # well through the request module, sub-module -- i don't know.
    book_id = request.args.get('id')
    return render_template('rating.html', book=Book.query.filter_by(id=book_id).first())


# delete route. didn't know this was possible lol i thought functions with flask were just automatically going to be pages.
# the home page has a Delete anchor tag before every book information. that anchor tag points to here which just redirects
# it back to the home page, effectively just literally being a function for that page. The home page, again, passes the book id
# as an argument to the url_for function, while our delete route does not formally receive any argument. This is another case
# where we can use the request blah-blah again to get that argument appended in the built link.
@app.route("/delete")
def delete():

    # after getting it, we can now use it to delete the book pointed to by the id.
    book_id = request.args.get('book_id')
    to_delete = Book.query.filter_by(id=book_id).first()
    db.session.delete(to_delete)
    db.session.commit()

    return redirect(url_for('home'))


# Yeaaah, we're awesome.
if __name__ == "__main__":
    app.run(debug=True)