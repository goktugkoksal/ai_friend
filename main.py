import speech_recognition as sr
import asyncio
from ollama import AsyncClient

import os
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:

    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id='aEJD8mYP0nuof1XHShVY',
            settings=VoiceSettings(
                stability=0.69, similarity_boost=0.4, style=0.7, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2",
    )

    play(audio)


def recognize_speech_from_mic():
    # Mikrofon nesnesi oluştur
    r = sr.Recognizer()

    while True:
        # Mikrofonu dinle ve sesi kaydet
        with sr.Microphone() as source:
            print("Dinliyorum...")
            audio = r.listen(source)

        # Ses tanıma işlemi
        try:
            # Türkçe olarak tanıma yapılacak
            text = r.recognize_google(audio, language="tr-TR")
            print(f"{text}")
            asyncio.run(chat(text))

        except sr.UnknownValueError:
            print("Anlamadım.")

        except sr.RequestError:
            print("Bağlantı hatası, lütfen internet bağlantınızı kontrol edin.")


async def chat(content):
    message = {'role': 'user', 'content': content}
    result = ""
    async for part in await AsyncClient(host='http://localhost:11434').chat(model='gemma2:latest', messages=[message], stream=True):
        result += part['message']['content']
        print(part['message']['content'], end='', flush=True)

    print("\n")

    text_to_speech_file(result)


def main():
    recognize_speech_from_mic()


if __name__ == "__main__":
    main()
