import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
import scipy.fftpack
import sys
import threading
from Queue import Queue

if len(sys.argv) != 2:
    print 'Song path needed'

CHUNK = 2**11
SKIP = 2**1
plt.axis([0,CHUNK/SKIP, -100000, 100000])
plt.ion()
graph = plt.plot(range(0,CHUNK/SKIP))[0]
shared_bool = True
song = sys.argv[1]


def play_music():
    p = pyaudio.PyAudio()
    fs, wave_data = wavfile.read(song)
    wf = wave.open(song, 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
              channels=wf.getnchannels(),
              rate=wf.getframerate(),
              output=True)

    q = Queue()
    def visualize():
        i = 0
        while i < len(wave_data):
            q.put(wf.readframes(CHUNK))
            d = wave_data[CHUNK*i:CHUNK*(i+1):SKIP, 1]
            graph.set_ydata(np.multiply(d, np.cos([np.pi*.5*h for h in xrange(0, CHUNK, SKIP)])))
            plt.draw()
            i += 1
            print 'Visual: %i' % i
            q.join()

    def play():
        i = 0
        while shared_bool:
            data = q.get()
            stream.write(data)
            q.task_done()
            i += 1
            print 'Stream: %i' % i

    t = threading.Thread(target=play, args=())
    t.start()
    visualize()
    t.join()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    try:
        play_music()
    except KeyboardInterrupt, SystemExit:
        shared_bool = False
        sys.exit()
    except RuntimeError:
        shared_bool = False
        sys.exit()
