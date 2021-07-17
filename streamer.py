import threading
import ctypes
import pyaudio
import wave

CHUNK = 1024

player = pyaudio.PyAudio()

currently_playing = {}

output_device = 0


class Streamer(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        try:
            wf = wave.open(self.path)

            stream = player.open(format=player.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                                 rate=wf.getframerate(), output=True, output_device_index=output_device)

            data = wf.readframes(CHUNK)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(CHUNK)

            stream.stop_stream()
            stream.close()
        except FileNotFoundError or OSError:
            pass

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)


def PlaySound(path):
    thread = Streamer(path)
    if path in currently_playing:
        currently_playing[path].append(thread)
    else:
        currently_playing[path] = [thread]
    thread.start()


def StopSound(path):
    try:
        for thread in currently_playing[path]:
            thread.raise_exception()
        del currently_playing[path]
    except KeyError:
        pass


def StopAllSounds():
    global currently_playing
    for i in currently_playing:
        for thread in currently_playing[i]:
            thread.raise_exception()
    currently_playing = {}


def ChangeOutputID(new_device):
    global output_device
    output_device = new_device

# player.terminate()
