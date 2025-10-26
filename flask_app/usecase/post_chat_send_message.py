import ollama
from flask_app.forms.chat_form import ChatForm
from flask_app.models.dynamodb.chat_history import ChatHistory
from flask_app.models.gemini import IGemini
import markdown
from pynamodb.exceptions import DoesNotExist


class PostChatSendMessage:
    def __init__(self, gemini: IGemini = None):
        self.gemini = gemini

    def execute(self, form: ChatForm, chat_id, login_id):
        try:
            history = []
            try:
                # チャット履歴取得
                chat_history = ChatHistory.get(hash_key=login_id, range_key=chat_id)
            except DoesNotExist:
                chat_history = ChatHistory()
                chat_history.chat_id = chat_id
                chat_history.login_id = login_id

            if chat_history.history:
                history = self.gemini.json_to_history(chat_history.history)

            response = self.gemini.send_message(form.user_message.data, history)
            gemini_response = response.text

            # チャット履歴保存
            chat_history.history = self.gemini.history_to_json(self.gemini.chat.history)
            chat_history.save(auto_delete=form.auto_delete.data)

            return f'<div class="message received">\
                Gemini: {markdown.Markdown().convert(gemini_response)}</div>'
        except Exception as e:
            print(e)
            return f"<div class='message error'>エラーが発生しました: {e}</div>"

    def execute_local_llm(self, form: ChatForm, chat_id, login_id):
        try:
            try:
                # チャット履歴取得
                chat_history = ChatHistory.get(hash_key=login_id, range_key=chat_id)
            except DoesNotExist:
                chat_history = ChatHistory()
                chat_history.chat_id = chat_id
                chat_history.login_id = login_id

            messages = []
            if chat_history.history:
                messages.extend(chat_history.history)
            messages.append({"role": "user", "content": form.user_message.data})
            response = ollama.chat(model=form.llm_type.data, messages=messages)
            content = response["message"]["content"]

            messages.append({"role": form.llm_type.data, "content": content})

            chat_history.history = messages
            chat_history.save(auto_delete=form.auto_delete.data)

            return f'<div class="message received">\
                {form.llm_type.data}: {markdown.Markdown().convert(content)}</div>'

        except Exception as e:
            print(e)
            return f"<div class='message error'>エラーが発生しました: {e}</div>"
