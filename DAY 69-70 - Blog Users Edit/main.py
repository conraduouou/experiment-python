from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from sqlalchemy.sql.schema import Table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, AnonymousUserMixin
from wtforms.validators import DataRequired
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# instantiate login manager for app
login_manager = LoginManager()
login_manager.init_app(app)

# instantiate gravatar for comment avatars
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(70), nullable=False)

    # using back_populates as an argument for relationship requires you to use the variable it
    # is being passed on to the table it relates to as a one-to-many relationship, hence the
    # 'author' variable in the BlogPost table. Using backref doesn't connect the receiving end,
    # I believe.
    posts = db.relationship('BlogPost', back_populates='author', lazy=True)
    comments = db.relationship('Comment', back_populates='author', lazy=True)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # the receiving end of the one-to-many relationship, which also connects the table back
    # to the sender, hence, 'posts' variable on User table
    author = db.relationship("User", back_populates='posts', lazy=True)

    # to access a column of a linked table, you use the ForeignKey explicitly in the arguments
    # and use the __tablename__ of the table plus the dot operator and the name of the column.
    # 'user.id' uses this in the code below.
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship("Comment", back_populates='parent_post', lazy=True)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)

    # application of above principles
    author = db.relationship("User", back_populates="comments", lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_post = db.relationship("BlogPost", back_populates='comments', lazy=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)

# db.create_all()


# used to load a user for a given session
# this is a user object
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()


# decorator for admin purposes in my blog
def admin_only(function):
    @wraps(function)

    # when you wrap functions with arguments, you declare *args and **kwargs in the
    # wrapper function to use them.
    def wrapper(*args, **kwargs):
        if not current_user.id == 1:
            return abort(403)
        
        return function(*args, **kwargs)
    
    return wrapper


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user != None:
            flash("You've already signed up with that email. Log in instead!")
            return redirect(url_for('login'))
        
        password_to_pass = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

        new_user = User(
            email=form.email.data,
            password=password_to_pass,
            name=form.name.data
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user == None:
            flash("User with entered credentials does not exist, please try again.")
        elif not check_password_hash(user.password, form.password.data):
            flash("Invalid email or password.")
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must be logged in to do that!")
            return redirect(url_for('login'))
        
        new_comment = Comment(
            text=form.body.data,
            author=current_user,
            parent_post=requested_post
        )

        db.session.add(new_comment)
        db.session.commit()
        
        form.body.data = ""
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['GET', 'POST'])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@login_required
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)