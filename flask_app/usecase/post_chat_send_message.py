from flask_app.models.gemini import IGemini


class PostChatSendMessage:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, user_message):
        try:
            response = self.gemini.send_message(user_message)
            gemini_response = response.text
            return f'<div class="message received">Gemini: {gemini_response.replace("。","。<br/>")}</div>'
        except Exception as e:
            return f"<div class='message error'>エラーが発生しました: {e}</div>"
