from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


class ChatForm(FlaskForm):
    user_message = StringField(
        "",
        validators=[DataRequired()],
        render_kw={"placeholder": "メッセージを入力..."},
    )
    send = SubmitField("送信")
