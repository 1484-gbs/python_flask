from flask import abort
import markdown
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini


class DeleteChatHistory:
    def execute(self, chat_id, login_id):
        try:
            # チャット履歴削除
            ChatHistory.get(hash_key=chat_id, range_key=login_id).delete()
        except DoesNotExist:
            abort(404)
