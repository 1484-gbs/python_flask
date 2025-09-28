from flask import abort
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory


class GetChatHistoryList:
    def execute(self, login_id):
        try:
            # チャット履歴取得
            chat_historys = ChatHistory.query(hash_key=login_id)
        except DoesNotExist:
            abort(404)

        sorted_historys = sorted(
            chat_historys, key=lambda c: c.last_modify_datetime, reverse=True
        )

        return [
            dict(chat_id=c.chat_id, title=c.history[0]["parts"][0]["text"])
            for c in sorted_historys
        ]
