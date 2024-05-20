import soundcard as sc
import soundfile as sf
import time

OUTPUT_FILE_NAME = "out.wav"    # output file name.
SAMPLE_RATE = 48_000              # [Hz]. sampling rate.
RECORD_SEC = 5                  # [sec]. recording duration.

print(f"output device: {str(sc.default_speaker().name)}")

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
    _start_time: float = time.perf_counter()
    
    # record audio with loopback from default speaker.
    data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)

    # output info
    print("\n-- info --")
    print(f"len of data: {len(data)}")
    print(f"elapsed time: {time.perf_counter() - _start_time}s")
    print("-- -- -- --\n")

    sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)