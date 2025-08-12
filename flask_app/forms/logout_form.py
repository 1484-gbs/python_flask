from wtforms import SubmitField
from flask_wtf import FlaskForm


class LogoutForm(FlaskForm):
    logout_button = SubmitField("ログアウト")
