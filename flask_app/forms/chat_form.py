from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class ChatForm(FlaskForm):
    user_message = StringField(
        "",
        validators=[DataRequired()],
        render_kw={"placeholder": "メッセージを入力..."},
    )
    send = SubmitField("送信")
    auto_delete = BooleanField("自動削除", default=True)
