from flask import Blueprint, render_template, request
from flask_app.usecase.post_chat_send_message import PostChatSendMessage
from flask_app.usecase.post_image_generate_content import PostImageGenerateContent

func_chat = Blueprint("func_chat", __name__)


@func_chat.get("/chat")
def get():
    return render_template("chat.html")


@func_chat.post("/chat")
def post_chat():
    user_message = request.form.get("message")
    if not user_message:
        return f'<div class="message error">メッセージが入力されていません。</div>', 400
    return PostChatSendMessage().execute(user_message=user_message)


@func_chat.post("/image")
def post_image():
    if "file" not in request.files:
        return f'<div class="message error">ファイルが選択されていません。</div>', 400

    file = request.files["file"]
    return PostImageGenerateContent().execute(file)
