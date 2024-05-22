import soundcard as sc
import speech_recognition as sr

# Parameters
SAMPLE_RATE = 48000  # [Hz]. sampling rate.
RECORD_SEC = 5       # [sec]. duration to capture audio before processing.

# Initialize recognizer
recognizer = sr.Recognizer()

# Get the default microphone with loopback
microphone = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

# Start recording audio in chunks and process each chunk
with microphone.recorder(samplerate=SAMPLE_RATE) as mic:
    while True:
        # Record audio
        data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
        
        # Convert to a format suitable for the recognizer
        audio_data = sr.AudioData(data.tobytes(), SAMPLE_RATE, data.shape[1])

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))
