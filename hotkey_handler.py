import streamer
import keyboard
import threading
import ctypes
import json
import os


def LoadHotkeys():
    if os.path.exists("./Hotkeys.json"):
        try:
            with open("./Hotkeys.json", "r") as f:
                data = json.load(f)
                if data is None:
                    data = {}
                return data
        except json.decoder.JSONDecodeError:
            return {}
    else:
        return {}


def SaveHotkeys():
    with open("./Hotkeys.json", "w") as f:
        json.dump(hotkey_binds, f)


hotkey_binds = LoadHotkeys()

hotkey_threads = {}


def StartHotkeyThreads():
    for binds in hotkey_binds:
        path = hotkey_binds[binds]
        thread = HotkeyHandler(binds, path)
        hotkey_threads[path] = thread
        thread.start()


def StopHotkeyThreads():
    global hotkey_threads
    for hotkey_thread in hotkey_threads:
        hotkey_threads[hotkey_thread].raise_exception()
    hotkey_threads = {}


def RestartHotkeyThreads():
    SaveHotkeys()
    StopHotkeyThreads()
    StartHotkeyThreads()


class HotkeyHandler(threading.Thread):
    def __init__(self, binds="", path=None, thread_type=0):
        threading.Thread.__init__(self)
        self.binds = binds.split("--:--")
        self.path = path
        self.thread_type = thread_type

    def run(self):
        if self.thread_type == 0:
            while True:
                keyboard.wait(self.binds[0])
                streamer.PlaySound(self.path)
        else:
            while True:
                keyboard.wait("pause")
                streamer.StopAllSounds()

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
