import http
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_app.usecase.get_chat_history import GetChatHistory
from flask_app.usecase.post_chat_send_message import PostChatSendMessage
from flask_app.usecase.delete_chat_history import DeleteChatHistory
from flask_app.models.gemini import Gemini1_5, Gemini2_0
from werkzeug.exceptions import BadRequest

func_api_chat = Blueprint("func_api_chat", __name__)

gemini = Gemini2_0()


@func_api_chat.get("/chat/<chat_id>")
@jwt_required()
def get(chat_id):
    login_id = get_jwt_identity()
    return jsonify(GetChatHistory().execute(chat_id=chat_id, login_id=login_id))


@func_api_chat.post("/chat/<chat_id>")
@jwt_required()
def post(chat_id):
    try:
        uuid.UUID(chat_id)
    except Exception:
        raise BadRequest("invalid path parameter.")

    post_data = request.get_json(force=True)
    user_message = post_data.get("message")
    if not user_message:
        raise BadRequest("message is required.")

    login_id = get_jwt_identity()

    PostChatSendMessage(gemini=gemini).execute(
        user_message=user_message, chat_id=chat_id, login_id=login_id
    )

    return jsonify(GetChatHistory().execute(chat_id=chat_id, login_id=login_id))


@func_api_chat.delete("/chat/<chat_id>")
@jwt_required()
def delete(chat_id):
    login_id = get_jwt_identity()
    DeleteChatHistory().execute(chat_id=chat_id, login_id=login_id)
    return "", http.HTTPStatus.NO_CONTENT


@func_api_chat.errorhandler(400)
@func_api_chat.errorhandler(404)
def error_handler(error):
    return jsonify(dict(message=error.description)), error.code


# @func_api_chat.errorhandler(Exception)
# def exception_handler(error):
#     print(error)
#     return jsonify(dict(message="internal server error.")), 500
