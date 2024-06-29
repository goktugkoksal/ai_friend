import speech_recognition as sr
import asyncio
from ollama import AsyncClient

import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from playsound import playsound

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="aEJD8mYP0nuof1XHShVY",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        model_id="eleven_multilingual_v2",

    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"output.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    # Return the path of the saved audio file
    return save_file_path


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

    playsound(text_to_speech_file(result))


def main():
    recognize_speech_from_mic()


if __name__ == "__main__":
    main()
