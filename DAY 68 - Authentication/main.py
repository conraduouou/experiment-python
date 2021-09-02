from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from decouple import config

# login manager integrated from flask-login
login_manager = LoginManager()

# main app
app = Flask(__name__)
login_manager.init_app(app)     # link login_manager to app

app.config['SECRET_KEY'] = config('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


# In case you want to restart
# for entry in db.session.query(User).all():
#     db.session.delete(entry)
#     db.session.commit()


# a little function to make things easier and shorter
def make_user():
    # generate password hash using werkzeug security
    password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
    
    if db.session.query(User).filter_by(email=request.form.get('email')).first() == None:
        new_user = User(
            email=request.form.get('email'),
            password=password,
            name=request.form.get('name')
        )

        return new_user

    return None


# a user_loader callback specified by Flask-Login.. ?
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        new_user = make_user()

        if new_user == None:
            error = 'There is an already existing account with that email'
        else:
            db.session.add(new_user)
            db.session.commit()

            return render_template("secrets.html", name=new_user.name)

    return render_template("register.html", error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        user = db.session.query(User).filter_by(email=request.form.get('email')).first()

        if user == None:
            error = 'The email does not exist, please try again'
        elif not check_password_hash(user.password, request.form.get('password')):
            error = 'Invalid credentials'
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", error=error)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        'static/files', 'cheat_sheet.pdf'
    )


if __name__ == "__main__":
    app.run(debug=True)
