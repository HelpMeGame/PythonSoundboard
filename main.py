import hotkey_handler
import threading
import gui

def Main():
    hotkey_handler.StartHotkeyThreads()
    stop_all_handler = hotkey_handler.HotkeyHandler(thread_type=1)
    stop_all_handler.start()
    gui.CreateGUI()

    hotkey_handler.StopHotkeyThreads()

Main()
