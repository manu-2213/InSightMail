import pygame
from gtts import gTTS
# from playsound import playsound
import os

    
def text_to_voice(text):
    """Convert text to voice and play it."""
    # Example: Ensure the MP3 file is created by another function beforehand
    print(f"going to speak: {text}")
    mp3_file = "hello2.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(mp3_file)
    
    
    pygame.mixer.init()  # Initialize pygame mixer
    pygame.mixer.music.load(mp3_file)  # Load the MP3 file
    pygame.mixer.music.play()  # Play the file
    
    while pygame.mixer.music.get_busy():  # Wait for playback to finish
        continue
    
    print(f"done speaking: {text}")

def main():
    text_to_voice("Hello Karl and Manu, I would love to chat with you tomorrow around 6pm. Does this work for you? Regards Max.")

if __name__ == "__main__":
    main()





