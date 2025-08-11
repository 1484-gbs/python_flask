from flask import abort
import markdown
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini


class GetChatHistory:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, chat_id):
        try:
            # チャット履歴取得
            chat_history = ChatHistory.get(chat_id)
        except DoesNotExist:
            abort(404)

        result = [
            dict(
                role=h["role"],
                style="sent" if h["role"] == "user" else "received",
                iam="" if h["role"] == "user" else "Gemini:",
                message=markdown.Markdown().convert(
                    "".join([part["text"] for part in h["parts"]])
                ),
            )
            for h in chat_history.history
        ]

        return result
