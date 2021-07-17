import tkinter as tk
from tkinter import ttk
import youtube_dl
import threading
import keyboard

import hotkey_handler
import streamer
import utils

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': './Sounds/%(title)s.%(ext)s',
    'default_search': 'auto',
    'quiet': True,
    'warnings': 'no-warnings'
}


class ToolBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        output_device = utils.GetDefaultOutputDevice()
        streamer.output_device = output_device[1]

        self.selected_sound = None
        self.sound_tree = None

        self.pack(side="top", fill="x")

        self.SoundRefresh = tk.Button(self, text="Refresh", command=self.RefreshSounds)
        self.SoundRefresh.pack(side="left")

        self.Download = tk.Button(self, text="Download", command=self.DownloadSound)
        self.Download.pack(side="left")

        self.StopAll = tk.Button(self, text="Stop All", command=self.StopAllSounds)
        self.StopAll.pack(side="right")

        self.SoundStop = tk.Button(self, text="Stop", command=self.StopSound)
        self.SoundStop.pack(side="right")

        self.SoundPlay = tk.Button(self, text="Play", command=self.PlaySound)
        self.SoundPlay.pack(side="right")

        self.output_device = tk.StringVar(self)
        self.output_device.set(output_device[0])
        self.output_device.trace("w", self.ChangeOutputDevice)

        self.output_device_options = tk.OptionMenu(self, self.output_device, *utils.GetOutputDevices())
        self.output_device_options.pack(side="right")

    def RefreshSounds(self):
        self.sound_tree.SetSounds()

    def PlaySound(self):
        streamer.PlaySound(self.selected_sound)

    def StopSound(self):
        streamer.StopSound(self.selected_sound)

    def StopAllSounds(self):
        streamer.StopAllSounds()

    def DownloadSound(self):
        download_root = tk.Tk()
        download_root.geometry('200x30')
        download_root.resizable(False, False)
        download_root.title("Download")

        download_window = Download(download_root, self)
        download_root.mainloop()

    def ChangeOutputDevice(self, *args):
        current_devices = utils.GetOutputDevices()
        streamer.output_device = current_devices[self.output_device.get()]


class SoundTree(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(side="bottom", fill="both", expand="true")

        self.tree = ttk.Treeview(self.master, columns=('#1', '#2', '#3'), show='headings')
        self.SetupTree()
        self.tool_bar = None

    def SetupTree(self):
        self.tree.heading('#1', text='Sound')
        self.tree.heading('#2', text='Hotkey')
        self.tree.heading('#3', text='Path')

        self.SetSounds()
        self.tree.pack(side="top", fill="both", expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.SetCurrentSound)
        self.tree.bind('<<TreeviewOpen>>', self.EditHotkey)

    def SetSounds(self):
        self.tree.delete(*self.tree.get_children())
        for sound in utils.GetSounds():
            keybind = "none"

            if sound[0] in hotkey_handler.hotkey_binds.values():
                print(sound[0])
                index = list(hotkey_handler.hotkey_binds.values()).index(sound[0])
                print(index)
                keybind = list(hotkey_handler.hotkey_binds.keys())[index]

            self.tree.insert('', 'end', values=(sound[1], keybind, sound[0]))

    def SetCurrentSound(self, event):
        for item_selected in self.tree.selection():
            self.tool_bar.selected_sound = self.tree.item(item_selected)['values'][2]

    def EditHotkey(self, event):
        for item_selected in self.tree.selection():
            hotkey_root = tk.Tk()
            hotkey_root.geometry('200x30')
            hotkey_root.resizable(False, False)
            hotkey_root.title("Set Hotkey")

            hotkey_window = SetHotkey(hotkey_root, self.tree.item(item_selected)['values'][2], self)
            hotkey_root.mainloop()


class Download(ttk.Frame):
    def __init__(self, master, tool_bar: ToolBar):
        super().__init__(master)
        self.master = master
        self.pack(side="top")
        self.tool_bar = tool_bar

        self.search_input = tk.Entry(self)
        self.search_input.pack(side="left")

        self.search_button = tk.Button(self, text="Download", command=self.SearchForSound)
        self.search_button.pack(side="right")

    def SearchForSound(self):
        search = self.search_input.get()
        self.search_button['text'] = "Downloading..."
        self.search_button["state"] = "disabled"
        with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
            ytdl.download([search])
        self.tool_bar.RefreshSounds()
        self.master.destroy()


class SetHotkey(ttk.Frame):
    def __init__(self, master, path, treeView):
        super().__init__(master)
        self.master = master
        self.pack(side="top")
        self.path = path
        self.treeView = treeView

        self.key = tk.StringVar(self)
        self.key.set("none")

        self.label = tk.Label(self, textvariable=self.key)
        self.label.pack(side="left")

        self.set_button = tk.Button(self, text="Set", command=self.SetKey)
        self.set_button.pack(side="left")

    def SetKey(self):
        self.key.set("Press any button")
        self.set_button['state'] = "disabled"
        self.key.set(keyboard.read_key())
        self.set_button['state'] = "active"

        hotkey_handler.hotkey_binds[self.key.get()] = self.path
        print(hotkey_handler.hotkey_binds)
        hotkey_handler.RestartHotkeyThreads()

        self.treeView.SetSounds()

        self.master.destroy()


def CreateGUI():
    root = tk.Tk()
    root.geometry('410x250')
    root.resizable(False, False)
    root.title("Soundboard")

    sound_tree = SoundTree(root)
    tool_bar = ToolBar(root)

    sound_tree.tool_bar = tool_bar
    tool_bar.sound_tree = sound_tree

    root.mainloop()
