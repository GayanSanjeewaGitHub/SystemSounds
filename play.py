
from pydub import AudioSegment
from pydub.playback import play
 
# for playing wav file
song = AudioSegment.from_wav("out.wav")
print('playing sound using  pydub')
play(song)