import os
from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required
import logging

from flask_app.models.eleven_lab import EXPORT_TTS_DIR, ElevenLab


func_tts_convert = Blueprint("func_tts_convert", __name__)

logger = logging.getLogger(__name__)


@func_tts_convert.get("/")
@login_required
def index():
    client = ElevenLab()
    response = client.get_voices()
    return render_template("tts_convert.html", voices=response.voices)


@func_tts_convert.post("/")
@login_required
def tts_convert():
    prompt = request.form.get("prompt")
    logger.info(f"リクエストを受信: prompt='{prompt}'")

    if not prompt:
        return "<p class='text-red-500'>プロンプトを入力してください</p>"

    try:
        logger.info("ElevenLabs API を呼び出し中...")
        voice_id = request.form.get("voice_id")

        client = ElevenLab()
        audio_iterator = client.tts_convert(
            text=prompt, voice_id=voice_id, model_id="eleven_v3"
        )

        filename = f"tts_{os.urandom(4).hex()}.mp3"
        filepath = os.path.join(EXPORT_TTS_DIR, filename)

        with open(filepath, "wb") as f:
            for chunk in audio_iterator:
                if chunk:
                    f.write(chunk)

        return render_template(
            "tts_convert_success.html",
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


@func_tts_convert.get("/download/<filename>")
@login_required
def download(filename):
    logging.info(filename)
    return send_from_directory(EXPORT_TTS_DIR, filename)
