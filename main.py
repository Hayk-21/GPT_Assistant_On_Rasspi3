import speech_recognition as sr
import openai
import time
import os
from gtts import gTTS
import pygame
import pyttsx3

def speak(text, lang='en', filename='output.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    
def speak_fast(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 130)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

    engine.say(text)

    engine.runAndWait()

def generate_response(prompt):
    res = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user', 'content':prompt}]
    )
    return res['choices'][0]['message']['content']

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
                    response = generate_response(text)
                    print(f"[Spider-GPT]: {response.strip()}")
                    start_t = time.time()
                    speak_fast(response) if len(response) > 400 else speak(response)
                    time.sleep(2)
                    
                elif (current_t - start_t) > 10:
                    return wakeup()
                else:
                    current_t = time.time()
                    print(f"Silence...: {current_t - start_t}")
                    
            except Exception as e:
                if (current_t - start_t) > 10:
                    return wakeup()
                else: current_t = time.time()
                print(f"Noize...: {e}")
                

if __name__ == "__main__":
    wakeup()
