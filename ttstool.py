from deep_translator import GoogleTranslator
from gtts import gTTS
import os

class GoogleTransDeep:
    def trans_to_tamil(self, text: str) -> str:
        # Translate input text to Tamil
        return GoogleTranslator(source='auto', target='ta').translate(text)

    def text_to_speech(self, text: str, filepath: str):
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Convert Tamil text to speech and save as mp3
        tts = gTTS(text, lang='ta')
        tts.save(filepath)

    def run(self, query: str, output_audio_filename="output/output.mp3"):
        try:
            # Translate text
            tamil_text = self.trans_to_tamil(query)

            # Convert and save as audio
            self.text_to_speech(tamil_text, output_audio_filename)

            return {
                "translated_text": tamil_text,
                "audio_path": output_audio_filename
            }
        except Exception as e:
            return {"error": str(e)}
