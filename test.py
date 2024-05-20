import soundcard as sc

# get a list of all speakers:
speakers = sc.all_speakers()
print(speakers)
# get the current default speaker on your system:
default_speaker = sc.default_speaker()
print(default_speaker)
# get a list of all microphones:
mics = sc.all_microphones()
print(mics)
# get the current default microphone on your system:
default_mic = sc.default_microphone()
print(default_mic)