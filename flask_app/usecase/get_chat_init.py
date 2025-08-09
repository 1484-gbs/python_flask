import json
import uuid
from flask import abort
import markdown
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini


class GetChatInit:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, chat_id=""):
        if not chat_id:
            return str(uuid.uuid4()), None

        try:
            # チャット履歴取得
            chat_history = ChatHistory.get(chat_id)
        except DoesNotExist:
            abort(404)

        histoty = self.gemini.json_to_history(json.loads(chat_history.history))

        result = [
            dict(
                style="sent" if h.role == "user" else "received",
                iam="" if h.role == "user" else "Gemini:",
                message=markdown.Markdown().convert(
                    "".join([part.text for part in h.parts])
                ),
            )
            for h in histoty
        ]

        return chat_id, result
