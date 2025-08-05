from flask_app.models.gemini import IGemini
from PIL import Image


class PostImageGenerateContent:
    def __init__(self, gemini: IGemini):
        self.gemini = gemini

    def execute(self, file):
        try:
            img = Image.open(file)
            response = self.gemini.generate_content_img(img=img)
            analysis_result = response.text
            return f'<div class="message received">Gemini: {analysis_result.replace("。","。<br/>")}</div>'
        except Exception as e:
            return f"<div>エラーが発生しました: {e}</div>"
