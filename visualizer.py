import pyaudio
import wave
from matplotlib import pyplot as plt
from scipy.io import wavfile
import sys

#####################################################################
#                                                                   #
# This script is a crude and simple audio visualizer. It has quite  #
# a few dependencies:                                               #
#   matplotlib                                                      #
#   scipy/numpy                                                     #
#   pyaudio                                                         #
#                                                                   #
# It takes an audio file (.wav) as the only arguement.              #
#                                                                   #
# Depending on your system, you might need to adjust the CHUNK size #
# if it lags or skips.                                              #
#                                                                   #
#####################################################################

if len(sys.argv) != 2:
    print 'Song path needed'

CHUNK = 2**11
print CHUNK
plt.axis([0,CHUNK, -32000, 32000])
plt.ion()
graph = plt.plot(range(0,CHUNK))[0]

def play_music():
    p = pyaudio.PyAudio()
    fs, wave_data = wavfile.read(sys.argv[1])
    wf = wave.open(sys.argv[1], 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
              channels=wf.getnchannels(),
              rate=wf.getframerate(),
              output=True)
    i = 0
    while i < len(wave_data):
        data = wf.readframes(CHUNK)
        if (len(data) < 0): break
        stream.write(data)
        graph.set_ydata(wave_data[CHUNK*i:CHUNK*(i+1), 0])
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
