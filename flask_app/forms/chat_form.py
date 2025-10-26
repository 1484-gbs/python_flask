import ollama
from wtforms import BooleanField, SelectField, StringField, SubmitField
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
    llm_type = SelectField(
        "LLM種別",
        choices=[(model.model, model.model) for model in ollama.list().models],
    )
