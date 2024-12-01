import speech_recognition as sr
import threading
import time
from queue import Queue
# from gemma_utils import Prediction

listen_recognizer = sr.Recognizer()
process_recognizer = sr.Recognizer()

audios_to_process = Queue()

# Shared user_input variable to store recognized text
user_input = None

def callback(recognizer, audio_data):
    if audio_data:
        audios_to_process.put(audio_data)

def listen():
    source = sr.Microphone()
    stop_listening = listen_recognizer.listen_in_background(source, callback, 3)
    return stop_listening

def process_thread_func():
    global user_input  # Declare user_input as global to modify it inside the function
    while user_input is None:
        if audios_to_process.empty():
            time.sleep(2)
            continue
        audio = audios_to_process.get()
        if audio:
            try:
                text = process_recognizer.recognize_google(audio)
            except Exception as e:
                print(f"Error recognizing audio: {e}")
            else:
                user_input = text  # Update the global user_input variable
                print(f"Recognized Text: {user_input}")

def get_user_input():
    global user_input
    
    # Start listening and processing
    stop_listening = listen()
    process_thread = threading.Thread(target=process_thread_func)
    process_thread.daemon = True  # Ensure thread exits when the main program ends
    process_thread.start()
    try:
        # model_cls = Prediction()
        while user_input is None:
            if user_input:
                stop_listening()
            # print(f"Using user_input: {user_input}")
            # Reset user_input after processing if needed
            # user_input = None
            # model_cls.obtain_actions()
            # model_cls.main()
        time.sleep(1)  # Prevent busy-waiting
        print(f"Got some input: {user_input}")
    except KeyboardInterrupt:
        print("Stopping...")
        stop_listening()
    return user_input

def main():
    global user_input
    print("actual main method")
    try:
        # model_cls = Prediction()
        print(f"Using user_input: {user_input}")
        while user_input is None:
            if user_input:
                stop_listening()
            # print(f"Using user_input: {user_input}")
            # Reset user_input after processing if needed
            # user_input = None
            # model_cls.obtain_actions()
            # model_cls.main()
        time.sleep(1)  # Prevent busy-waiting
        print(f"Got some input: {user_input}")
    except KeyboardInterrupt:
        print("Stopping...")
        stop_listening()
    print("actual end method")

if __name__ == "__main__":
    main()

