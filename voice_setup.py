from gtts import gTTS
import pygame
from io import BytesIO

def speak(text, lang='en'):
    # Create a gTTS object with the text and language
    tts = gTTS(text=text, lang=lang)

    # Save the speech as an audio file in memory
    audio_data = BytesIO()
    tts.save(audio_data)
    audio_data.seek(0)

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the audio data from the BytesIO object
    pygame.mixer.music.load(audio_data)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the speech to complete
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.mixer.quit()

# Example usage
text = "Hello, how are you today?"
speak(text)
