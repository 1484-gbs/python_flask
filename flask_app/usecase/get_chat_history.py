from flask import abort
import markdown
from pynamodb.exceptions import DoesNotExist
from flask_app.models.dynamodb.chat_history import ChatHistory


class GetChatHistory:
    def execute(self, chat_id, login_id):
        try:
            # チャット履歴取得
            chat_history = ChatHistory.get(hash_key=login_id, range_key=chat_id)
        except DoesNotExist:
            abort(404)

        result = dict(
            history=[
                dict(
                    role=h["role"],
                    style="sent" if h["role"] == "user" else "received",
                    iam="" if h["role"] == "user" else h["role"] + ":",
                    message=markdown.Markdown().convert(
                        "".join([part["text"] for part in h["parts"]])
                        if h.get("parts")
                        else "".join(h["content"])
                    ),
                )
                for h in chat_history.history
            ],
            auto_delete=chat_history.auto_delete,
        )

        return result
