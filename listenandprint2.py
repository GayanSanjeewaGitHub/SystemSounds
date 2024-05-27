import pyaudio
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Function to capture audio from the speaker output
def callback(in_data, frame_count, time_info, status):
    audio_data = sr.AudioData(in_data, 16000, 2)
    try:
        # Recognize the speech using Google Web Speech API
        text = recognizer.recognize_google(audio_data)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))
    return (in_data, pyaudio.paContinue)

# Set up the PyAudio parameters
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024,
                stream_callback=callback)

# Start the stream
stream.start_stream()

print("Listening...")

# Keep the program running
try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    print("Stopping...")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()