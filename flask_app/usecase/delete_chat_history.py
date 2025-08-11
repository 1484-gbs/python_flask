from flask import abort
import markdown
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini


class DeleteChatHistory:
    def execute(self, chat_id):
        try:
            # チャット履歴削除
            ChatHistory.get(chat_id).delete()
        except DoesNotExist:
            abort(404)
