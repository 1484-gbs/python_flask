import os
import google.generativeai as genai


class Gemini:

    def __init__(self):
        # Gemini APIキーの設定
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel("gemini-2.0-flash-lite")

    def send_message(self, user_message):
        chat = self.model.start_chat(history=[])
        return chat.send_message(user_message)

    def generate_content_img(self, img, q="この画像について詳しく説明してください。"):
        return self.model.generate_content([q, img])


if __name__ == "__main__":
    pass
