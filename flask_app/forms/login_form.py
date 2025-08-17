from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    login_id = StringField("ログインID", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    login_button = SubmitField("ログイン")


class MfaForm(FlaskForm):
    login_id = HiddenField()
    mfa_id = HiddenField()
    mfa_code = StringField("認証コード", validators=[DataRequired()])
    next = HiddenField()
    login_button = SubmitField("認証")
