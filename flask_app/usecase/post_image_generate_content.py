from flask_app.models.gemini import IGemini
from PIL import Image
import markdown


class PostImageGenerateContent:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, file, q=None):
        try:
            img = Image.open(file)
            response = self.gemini.generate_content_img(img=img, q=q)
            analysis_result = response.text
            return f'<div class="message received">\
                Gemini: {markdown.Markdown().convert(analysis_result)}</div>'
        except Exception as e:
            return f"<div class='message error'>エラーが発生しました: {e}</div>"
