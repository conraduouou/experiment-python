from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, Email, ValidationError

# integrate Bootstrap to app
def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app


# form from wtforms
class MyForm(FlaskForm):

    # password validator
    def password_validator(form, field):
        if len(field.data) < 8:
            raise ValidationError('Password must contain at least 8 characters.')


    email = fields.StringField(label='Email', validators=[DataRequired(), Email()])
    password = fields.PasswordField(label='Password', validators=[DataRequired(), password_validator])
    submit = fields.SubmitField(label='Log In')


# main
app = create_app()
app.secret_key = "nagyungiloveu"


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()

    email_to_match = 'admin@email.com'
    pass_to_match = '12345678'

    if form.validate_on_submit():
        if form.email.data == email_to_match and form.password.data == pass_to_match:
            return render_template('success.html')
        else:
            return render_template('denied.html')
        
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)