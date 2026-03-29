import os
from elevenlabs import ElevenLabs

EXPORT_MUSIC_DIR = "/temp/generated_music"
EXPORT_TTS_DIR = "/temp/tts"

os.makedirs(EXPORT_MUSIC_DIR, exist_ok=True)
os.makedirs(EXPORT_TTS_DIR, exist_ok=True)


class ElevenLab:

    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def generate_music(self, prompt, music_length_ms=30000):
        return self.client.music.compose(
            prompt=prompt,
            music_length_ms=music_length_ms,
        )

    def get_voices(self):
        return self.client.voices.get_all()

    def tts_convert(
        self,
        text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    ):
        return self.client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
