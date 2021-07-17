# PythonSoundboard
A Python-based Soundboard, using `PyAudio`, `FFMPEG`, `YouTube-DL` and `Tkinter`.

## Installation
The installation for `PythonSoundboard` is pretty simple. You need to have [FFMPEG installed](https://ffmpeg.org/download.html) and added to your PATH, and the following libraries installed in python 3.6:

`pyaudio`, `ffmpeg-python`, and `pip install youtube-dl`

Then, run the `start.bat` file to open the GUI.

## Usage
### Adding Sounds
To add a sound, simply drop a file into the `Sounds` folder. When the application starts, anything that is not a `.wav` folder will be converted with `ffmpeg` and the old version will be deleted.

### Setting a Hotkey
Setting a hotkey is simple. Just double click the name of the sound you want to create a hotkey for, and click the `Set` button. Your next button press will become the hotkey for that sound.

### Downloading Sounds
PythonSoundboard has `youtube-dl` built in, allowing for the downloading of youtube videos or other media links through the application. This can be achieved by hitting the `Download` button on the main view, and entering a search term or link. This may take a while, depending on your internet speed.

## Known Bugs
- The player uses **lots** of RAM. This may be in part to the large number of threads being used.
- Some hotkeys have multiple triggers, including the arrow keys triggering number hotkeys.
