import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
import sys

#if len(sys.argv) != 2:
#    print 'Song path needed'

CHUNK = 2**11
plt.axis([0,CHUNK, -32000, 32000])
plt.ion()
graph = plt.plot(range(0,CHUNK))[0]

def play_music():
    p = pyaudio.PyAudio()
    fs, wave_data = wavfile.read('Dancing_On_Glass.wav')
    wf = wave.open('Dancing_On_Glass.wav', 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
              channels=wf.getnchannels(),
              rate=wf.getframerate(),
              output=True)
    i = 0
    while i < len(wave_data):
        data = wf.readframes(CHUNK)
        stream.write(data)
        graph.set_ydata(wave_data[CHUNK*i:CHUNK*(i+1), 1])
        plt.draw()
        i += 1
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    try:
        play_music()
    except KeyboardInterrupt:
        sys.exit()
