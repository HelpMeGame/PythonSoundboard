import pyaudio
import ffmpeg
import os


def GetSounds():
    sounds = []
    for path, subdirs, files in os.walk("./Sounds"):
        for name in files:
            full_path = path.replace("\\", "/") + f"/{name}"
            if name.endswith(".wav"):
                sounds.append((f"{path}/{name}", name.split(".")[0]))
            else:
                if os.path.isfile(full_path):
                    new_path = f"{path}/{name.split('.')[0]}.wav"
                    try:
                        ffmpeg.run(ffmpeg.input(full_path).output(new_path), quiet=True)
                    except ffmpeg._run.Error:
                        continue
                    os.remove(full_path)
                    sounds.append((new_path, name.split(".")[0]))
    return sounds


def GetOutputDevices():
    device_list = {}
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
            device_list[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i

    p.terminate()
    return device_list


def GetDefaultOutputDevice():
    p = pyaudio.PyAudio()
    data = p.get_default_output_device_info()
    return [data['name'], data['index']]
