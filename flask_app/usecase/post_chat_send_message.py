from flask_app.models.gemini import Gemini


class PostChatSendMessage:
    def execute(self, user_message):
        try:
            response = Gemini().send_message(user_message)
            gemini_response = response.text
            return f'<div class="message received">Gemini: {gemini_response.replace("。","。<br/>")}</div>'
        except Exception as e:
            return f"<div>エラーが発生しました: {e}</div>"
