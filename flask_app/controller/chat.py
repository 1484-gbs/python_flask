import http
import uuid
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from flask_app.forms.chat_form import ChatForm
from flask_app.usecase.create_csv_chat_history import CreateCsvChatHistory
from flask_app.usecase.get_chat_history import GetChatHistory
from flask_app.usecase.get_chat_history_list import GetChatHistoryList
from flask_app.usecase.post_chat_send_message import PostChatSendMessage
from flask_app.usecase.post_image_generate_content import PostImageGenerateContent
from flask_app.models.gemini import Gemini1_5, Gemini2_0
from flask_login import current_user
from werkzeug.exceptions import NotFound


func_chat = Blueprint("func_chat", __name__)

gemini = Gemini2_0()


@func_chat.get("/chat")
@login_required
def get():
    return redirect(url_for("func_chat.get_path_param", chat_id=str(uuid.uuid4())))


@func_chat.get("/chat/<chat_id>")
@login_required
def get_path_param(chat_id):
    try:
        chat = GetChatHistory().execute(chat_id=chat_id, login_id=current_user.login_id)
    except NotFound:
        chat = {}
    return render_template(
        "chat.html",
        chat_id=chat_id,
        chat=chat,
        form=ChatForm(
            auto_delete=(
                chat["auto_delete"] if not chat.get("auto_delete") is None else True
            )
        ),
    )


@func_chat.get("/chat_list")
@login_required
def get_list():
    if not "HX-Request" in request.headers:
        return redirect(url_for("func_index.index"))
    try:
        historys = GetChatHistoryList().execute(login_id=current_user.login_id)
    except NotFound:
        historys = []
    return render_template("chat_list.html", historys=historys)


@func_chat.post("/chat/<chat_id>/s3upload")
@login_required
def s3upload(chat_id):
    CreateCsvChatHistory().execute(chat_id=chat_id, login_id=current_user.login_id)
    return "", http.HTTPStatus.OK


@func_chat.post("/chat/<chat_id>")
@login_required
def post_chat(chat_id):
    form = ChatForm()
    print(form.auto_delete.data)
    return PostChatSendMessage(gemini=gemini).execute(
        form=form,
        chat_id=chat_id,
        login_id=current_user.login_id,
    )


@func_chat.post("/chat_image")
@login_required
def post_image():
    if "file" not in request.files:
        return f'<div class="message error">ファイルが選択されていません。</div>'
    file = request.files["file"]
    q = (
        request.form.get("q")
        if request.form.get("q")
        else "この画像について詳しく説明してください。"
    )
    return PostImageGenerateContent(gemini=gemini).execute(file=file, q=q)


@func_chat.before_request
def before_request():
    # Flask-Loginのリダイレクト前にhtmxリクエストかをチェック
    if "HX-Request" in request.headers and not current_user.is_authenticated:
        # htmxリクエストで未認証の場合、HX-Refreshでリロードを指示
        return "", 200, {"HX-Refresh": "true"}
