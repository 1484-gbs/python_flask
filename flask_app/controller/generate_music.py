import os
from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required
import logging

from flask_app.models.eleven_lab import EXPORT_MUSIC_DIR, ElevenLab


func_generate_music = Blueprint("func_generate_music", __name__)

logger = logging.getLogger(__name__)


@func_generate_music.get("/")
@login_required
def index():
    return render_template("generate_music.html")


@func_generate_music.post("/")
@login_required
def generate_music():
    prompt = request.form.get("prompt")
    logger.info(f"リクエストを受信: prompt='{prompt}'")

    if not prompt:
        return "<p class='text-red-500'>プロンプトを入力してください</p>"

    try:
        logger.info("ElevenLabs API を呼び出し中...")

        client = ElevenLab()
        # audio_iterator = client.generate_music(prompt=prompt)

        filename = f"music_{os.urandom(4).hex()}.mp3"
        filepath = os.path.join(EXPORT_MUSIC_DIR, filename)

        # with open(filepath, "wb") as f:
        #     for chunk in audio_iterator:
        #         if chunk:
        #             f.write(chunk)

        logger.info(f"保存完了: {filepath}")

        return render_template(
            "generate_music_success.html",
            prompt=prompt,
            filename=filename,
        )

    except Exception as e:
        # コンソールにエラーの詳細を表示
        logger.error(f"エラー発生: {str(e)}", exc_info=True)
        # ユーザー（ブラウザ）にエラーを表示
        return (
            f"""
        <div class="mt-4 p-4 border rounded bg-red-50 border-red-200 text-red-700">
            <p class="font-bold">エラーが発生しました</p>
            <p class="text-sm">{str(e)}</p>
        </div>
        """,
        )


@func_generate_music.get("/download/<filename>")
@login_required
def download(filename):
    logging.info(filename)
    return send_from_directory(EXPORT_MUSIC_DIR, "filename")
