from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    login_id = StringField("ログインID", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    login_button = SubmitField("ログイン")


class CSRFOnlyForm(FlaskForm):
    csrf_token = HiddenField()
