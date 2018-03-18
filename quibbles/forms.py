from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from .models import User


class QuibbleForm(Form):
    text = StringField('Text:', validators=[DataRequired()])
    category = StringField('Category:', validators=[DataRequired()])
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message="Tags can only contain letters and numbers")])

    def validate(self):
        if not Form.validate(self):
            return False

        if not self.text.data:
            self.text.data = self.text.data

        if not self.category.data:
            self.category.data = self.category.data

        # filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True


class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(Form):
    username = StringField('Username', validators=[
        DataRequired(), Length(3, 80),
        Regexp('^[A-Za-z0-9_]{3,}$', message='Usernames consist of numbers, letters, and underscores.')])

    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password2', message='Passwords must match.')])

    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])

    @staticmethod
    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already an user with this email address.')

    @staticmethod
    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
