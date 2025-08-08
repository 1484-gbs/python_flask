from flask_app.models.gemini import IGemini
from flask import session
import markdown
import pickle


class PostChatSendMessage:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, user_message):
        try:
            history = []
            if "chat_history" in session:
                # sessionからチャット履歴を取得
                history = pickle.loads(session["chat_history"])

            response = self.gemini.send_message(user_message, history)
            gemini_response = response.text

            # sessionにチャット履歴を格納
            session["chat_history"] = pickle.dumps(self.gemini.chat.history)

            return f'<div class="message received">\
                Gemini: {markdown.Markdown().convert(gemini_response)}</div>'
        except Exception as e:
            return f"<div class='message error'>エラーが発生しました: {e}</div>"
