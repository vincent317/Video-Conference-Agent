import jwt
import requests
import json
from time import time
import urllib.request
import webvtt
import os

# TODO: key config file

API_KEY = os.environ['ZOOM_API_KEY']
API_SEC = os.environ['ZOOM_API_SEC']

# Zoom authorization
def auth():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm='HS256'
    )

    headers = {"authorization": "Bearer %s" % token, "content-type": "application/json"}
    params = {"include_fields": "download_access_token"}
    return headers, params

# Given the meeting ID, returns the participants data in the meeting
def get_participants_data(meeting_id):
    headers, _ = auth()
    part = requests.get(f'https://api.zoom.us/v2/past_meetings/'+str(meeting_id)+'/participants', headers=headers)
    if part.status_code == 200:
        response = json.loads(part.text)
        part_arr = response['participants']
        return part_arr
    else:
        print("Zoom: Fetching participants data in meeting " + str(meeting_id) + "failed")
        return None

def webvtt_parsing(vtt_path, meeting_id):
    everything = ""
    for caption in webvtt.read(vtt_path):
        everything += caption.text + "\n"
    txt_path = str(meeting_id) + ".txt"
    txt_path = os.path.join("zoom_transcripts", txt_path)
    if not os.path.exists(txt_path): 
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(everything)
    return txt_path

# Given the meeting ID, returns the location of downloaded WebVTT file
def get_meeting_transcript(meeting_id):
    store_path = os.path.join('zoom_transcripts', str(meeting_id) + '.vtt')
    
    if not os.path.exists(store_path): 
        headers, params = auth()
        ret = requests.get(
            'https://api.zoom.us/v2/meetings/' + str(meeting_id) + "/recordings",
            headers=headers,
            params=params,
        )

        print("Fetching meeting " + str(meeting_id) + "...\n")

        if ret.status_code == 200:
            response = json.loads(ret.text)
            recording_arr = response["recording_files"]

            for meeting_file in recording_arr:
                if  meeting_file['file_type'] == 'TRANSCRIPT':
                    transcript_url =  meeting_file['download_url'] + "?access_token=" + response["download_access_token"]
                    urllib.request.urlretrieve(transcript_url, store_path)
                    break
        else:
            print("Zoom: Fetching meeting transcript" + str(meeting_id) + "failed")
            return None
        
    return webvtt_parsing(store_path, meeting_id)

# Given the meeting ID, returns the location of downloaded WebVTT file
def get_meeting_audio(meeting_id):
    store_path = os.path.join("audios", str(meeting_id) + '.m4a')
    
    if not os.path.exists(store_path): 
        headers, params = auth()
        ret = requests.get(
            'https://api.zoom.us/v2/meetings/' + str(meeting_id) + "/recordings",
            headers=headers,
            params=params,
        )

        print("Zoom: Fetching meeting audio " + str(meeting_id) + "...\n")

        if ret.status_code == 200:
            response = json.loads(ret.text)
            recording_arr = response["recording_files"]

            for meeting_file in recording_arr:
                if  meeting_file['file_type'] == 'M4A':
                    audio_url =  meeting_file['download_url'] + "?access_token=" + response["download_access_token"]
                    urllib.request.urlretrieve(audio_url, store_path)
                    return store_path
        else:
            print("Zoom: Fetching meeting audio" + str(meeting_id) + "failed")
            return None
    print("Zoom: Meeting audio " + str(meeting_id) + " already exists")
    return store_path