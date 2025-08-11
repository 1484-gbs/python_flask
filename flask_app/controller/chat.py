import uuid
from flask import Blueprint, render_template, request
from flask_app.usecase.get_chat_history import GetChatHistory
from flask_app.usecase.post_chat_send_message import PostChatSendMessage
from flask_app.usecase.post_image_generate_content import PostImageGenerateContent
from flask_app.models.gemini import Gemini1_5, Gemini2_0

func_chat = Blueprint("func_chat", __name__)

gemini = Gemini2_0()


@func_chat.get("/chat")
def get():
    return render_template("chat.html", chat_id=str(uuid.uuid4()))


@func_chat.get("/chat/<chat_id>")
def get_path_param(chat_id):
    # TODO login_id
    history = GetChatHistory(gemini=gemini).execute(chat_id=chat_id, login_id="test")
    return render_template("chat.html", chat_id=chat_id, history=history)


@func_chat.post("/chat")
def post_chat():
    chat_id = request.form.get("chat_id")
    if not chat_id:
        return f'<div class="message error">不正なリクエスト。</div>'
    user_message = request.form.get("message")
    if not user_message:
        return f'<div class="message error">メッセージが入力されていません。</div>'
    # TODO login_id
    return PostChatSendMessage(gemini=gemini).execute(
        user_message=user_message, chat_id=chat_id, login_id="test"
    )


@func_chat.post("/image")
def post_image():
    if "file" not in request.files:
        return f'<div class="message error">ファイルが選択されていません。</div>'
    file = request.files["file"]
    q = request.form.get("q") if request.form.get("q") else None
    return PostImageGenerateContent(gemini=gemini).execute(file=file, q=q)
