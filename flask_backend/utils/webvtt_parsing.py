import webvtt

def webvtt_parsing(location):
    everything = ""
    for caption in webvtt.read(location):
        everything += caption.text + "\n"
    return everything