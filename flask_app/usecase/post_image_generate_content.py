from flask_app.models.gemini import Gemini
from PIL import Image


class PostImageGenerateContent:
    def execute(self, file):
        try:
            img = Image.open(file)
            response = Gemini().generate_content_img(img=img)
            analysis_result = response.text
            return f'<div class="message sent">{file.filename}</div>\
                <div class="message received">Gemini: {analysis_result.replace("。","。<br/>")}</div>'
        except Exception as e:
            return f"<div>エラーが発生しました: {e}</div>"
