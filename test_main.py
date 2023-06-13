import speech_recognition as sr
import openai
import pyttsx3
import time
import os

openai.api_key = "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"
engine = pyttsx3.init()
time.sleep(3)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
    )
    return response["choices"][0]["text"]

def wakeup():

    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Say 'Spider' to start recording your question...")
            audio = r.listen(source)

        try:
            # Use Google Speech Recognition to convert speech to text
            text = r.recognize_google(audio)
            print(f"Recognized text: {text}")
            time.sleep(1)
            if text.lower() == "spider":
                    return conversation()
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
         
def conversation():
    print ("Spider is listening...\n")

    start_t = time.time()
    current_t = start_t
    filename = "input.wav"
    while True:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            print("Say something...")

            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
                time.sleep(1)
                
            try:
                text = recognizer.recognize_google(audio)
                if text:
                    print(f"[Admin]: {text}\n")
                    intext = f"""{text}"""
                    response = generate_response(intext)
                    print(f"[Spider-GPT]: {response.strip()}")
                    start_t = time.time()
                    speak_text(response)
                    time.sleep(2)
                    
                elif (current_t - start_t) > 10:
                    return wakeup()
                else:
                    current_t = time.time()
                    print(f"Silence...: {current_t - start_t}")
                    time.sleep(1)
              
            except Exception as e:
                if (current_t - start_t) > 10:
                    return wakeup()
                else: current_t = time.time()
                print(f"Noize...: {e}")
                time.sleep(1)

wakeup()
