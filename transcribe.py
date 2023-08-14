import speech_recognition as sr
import overrides as mysr
from googletrans import Translator
import threading

# Config
OUTPUT_FILE_NAME = "transcription.txt"
# These next two have to be in ISO 639-1 format (see: https://www.w3schools.com/tags/ref_language_codes.asp)
IN_LANGUAGE = "uk-UA"
OUT_LANGUAGE = "en-US"
SHORT_IN = IN_LANGUAGE.split("-")[0]
SHORT_OUT = OUT_LANGUAGE.split("-")[0]
        
def listen(recognizer, microphone):
    print("Listening...")
    with microphone as source:
        audio = recognizer.listen(source)
        print("Stopped listening")
        return audio
        
def transcribe(audio, recognizer, translator):
    # print("Transcribing...")
    try:
        uk_text = recognizer.recognize_google(audio, language=IN_LANGUAGE)
        translated_text = translator.translate(uk_text, src=SHORT_IN, dest=SHORT_OUT)
        write_to_file(OUTPUT_FILE_NAME, translated_text.text)
    except sr.UnknownValueError:
        print("Could not understand audio.")
        write_to_file(OUTPUT_FILE_NAME, "")
    except sr.RequestError as e:
        print(f"Error occurred during recognition: {e}")

def write_to_file(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def get_mic():
    for index, source in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {source}")
    while True:
        index = input("Select an index from the list above: ")
        try:
            return int(index)
        except ValueError:
            print("Invalid index")

def test_recording():
    # This function never gets used in runtime, it is simply here to test the microphone
    # Run it with the following command: `python -c 'from transcribe import *; test_recording()'`
    recognizer = mysr.NewRecognizer()
    recognizer.energy_threshold = 1000
    recognizer.pause_threshold=0.3
    recognizer.non_speaking_duration=0.3
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise, please don't say anything...")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print("Listening")
        audio = recognizer.listen(source)
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

if __name__ == "__main__":

    mic_index = get_mic()
    translator = Translator()
    recognizer = mysr.NewRecognizer()
    recognizer.energy_threshold = 1000
    recognizer.pause_threshold=0.3
    recognizer.non_speaking_duration=0.3
    microphone = sr.Microphone(device_index=mic_index)

    print("Adjusting for ambient noise, please don't say anything...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    try:
        while True:
            audio = listen(recognizer, microphone)
            transcription_thread = threading.Thread(
                                    target=transcribe,
                                    kwargs={"audio":audio,
                                    "recognizer":recognizer,
                                    "translator":translator}
                                    )
            transcription_thread.setDaemon(True)
            transcription_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down recognition service...")
        write_to_file(OUTPUT_FILE_NAME, "Recognition service inactive. This is sample text.")