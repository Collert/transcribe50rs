import speech_recognition as sr
from googletrans import Translator

def recognize_speech(recognizer, microphone):
    with microphone as source:
        print("Listening to Ukrainian...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=2)

        try:
            print("Processing...")
            recognized_text = recognizer.recognize_google(audio, language="uk-UA")
            print(f"Recognized text (Ukrainian): {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error occurred during recognition: {e}")
            return ""
        
def translate_to_eng(translator, uk_text):

    if not uk_text:
        return ""
    
    translated_text = translator.translate(uk_text, src="uk", dest="en")
    print(f"Translated text (English): {translated_text.text}")
    return translated_text.text

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

    try:
        while True:
            recognized_text = recognize_speech(recognizer, microphone)
            translated_text = translate_to_eng(translator, recognized_text)
            write_to_file("transcription.txt", translated_text)
    except KeyboardInterrupt:
        print("\nShutting down recognition service...")
        write_to_file("transcription.txt", "Recognition service inactive. This is sample text. lol")
