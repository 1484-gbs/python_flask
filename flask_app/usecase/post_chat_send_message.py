from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini
import markdown
from pynamodb.exceptions import DoesNotExist


class PostChatSendMessage:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, user_message, chat_id, login_id):
        try:
            history = []
            try:
                # チャット履歴取得
                chat_history = ChatHistory.get(hash_key=chat_id, range_key=login_id)
            except DoesNotExist:
                chat_history = ChatHistory()
                chat_history.uuid = chat_id
                chat_history.login_id = login_id

            if chat_history.history:
                history = self.gemini.json_to_history(chat_history.history)

            response = self.gemini.send_message(user_message, history)
            gemini_response = response.text

            # チャット履歴保存
            chat_history.history = self.gemini.history_to_json(self.gemini.chat.history)
            chat_history.save()

            return f'<div class="message received">\
                Gemini: {markdown.Markdown().convert(gemini_response)}</div>'
        except Exception as e:
            print(e)
            return f"<div class='message error'>エラーが発生しました: {e}</div>"
