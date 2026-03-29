import os
from elevenlabs import ElevenLabs

EXPORT_MUSIC_DIR = "/temp/generated_music"


class ElevenLab:

    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def generate_music(self, prompt, music_length_ms=30000):
        return self.client.music.compose(
            prompt=prompt,
            music_length_ms=music_length_ms,
        )
