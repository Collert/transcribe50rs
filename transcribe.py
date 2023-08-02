import speech_recognition as sr
from googletrans import Translator
import threading

# Config
OUTPUT_FILE_NAME = "transcription.txt"
        
def listen(recognizer, microphone):
    with microphone as source:
        audio = recognizer.listen(source, timeout=2)
        return audio
        
def transcribe(audio, recognizer, translator):
    try:
        uk_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio.")
        write_to_file(OUTPUT_FILE_NAME, "")
    except sr.RequestError as e:
        print(f"Error occurred during recognition: {e}")
    translated_text = translator.translate(uk_text, src="uk", dest="en")
    write_to_file(OUTPUT_FILE_NAME, translated_text)

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

if __name__ == "__main__":

    mic_index = get_mic()
    translator = Translator()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    print("Adjusting for ambient noise, please don't say anything...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    print("Listening...")

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
        write_to_file("transcription.txt", "Recognition service inactive. This is sample text.")