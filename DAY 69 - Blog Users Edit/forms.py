from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = fields.StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = fields.StringField("Subtitle", validators=[DataRequired()])
    img_url = fields.StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = fields.SubmitField("Submit Post")


# Register Form
class RegisterForm(FlaskForm):
    email = fields.StringField("Email", validators=[DataRequired(), Email()])
    password = fields.PasswordField("Password", validators=[DataRequired()])
    name = fields.StringField("Name", validators=[DataRequired()])
    submit = fields.SubmitField("Register")

# Login Form
class LoginForm(FlaskForm):
    email = fields.StringField("Email", validators=[DataRequired()])
    password = fields.PasswordField("Password", validators=[DataRequired()])
    submit = fields.SubmitField("Login")

# comment form
class CommentForm(FlaskForm):
    body = CKEditorField("Leave a comment!", validators=[DataRequired()])
    submit = fields.SubmitField("Submit Comment")