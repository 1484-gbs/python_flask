from abc import ABCMeta, abstractmethod
import os
from typing import Any, List
import google.generativeai as genai
from google.generativeai.protos import Content, Part


class IGemini(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, user_message):
        pass

    @abstractmethod
    def generate_content_img(self, img, q):
        pass

    @abstractmethod
    def history_to_json(self, history):
        pass

    @abstractmethod
    def json_to_history(self, json):
        pass

    def set_model(self, version):
        # Gemini APIキーの設定
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=GEMINI_API_KEY)

        return genai.GenerativeModel(version)


class Gemini2_0(IGemini):
    def __init__(self):
        self.model = super(Gemini2_0, self).set_model("gemini-2.0-flash-lite")

    def send_message(self, user_message, history=[]):
        self.chat = self.model.start_chat(history=history)
        return self.chat.send_message(user_message)

    def generate_content_img(self, img, q="この画像について詳しく説明してください。"):
        return self.model.generate_content([q, img])

    def history_to_json(self, history):
        return [
            {
                "role": h.role,
                "parts": [
                    {"text": part.text} if hasattr(part, "text") else part
                    for part in h.parts
                ],
            }
            for h in history
        ]

    def json_to_history(self, json):
        return [
            Content(
                role=item["role"],
                parts=[Part(text=part["text"]) for part in item["parts"]],
            )
            for item in json
        ]


class Gemini1_5(IGemini):
    def __init__(self):
        self.model = super(Gemini1_5, self).set_model("gemini-1.5-flash-002")

    def send_message(self, user_message):
        # chat = self.model.start_chat(history=[])
        # return chat.send_message(user_message)
        raise Exception("not defined send_message.")

    def generate_content_img(self, img, q="この画像について詳しく説明してください。"):
        # return self.model.generate_content([q, img])
        raise Exception("not defined generate_content_img.")


if __name__ == "__main__":
    pass
