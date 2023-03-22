import jwt
import requests
import json
from time import time
import urllib.request
import os

# TODO: key config file
API_KEY = os.environ['ZOOM_API_KEY']
API_SEC = os.environ['ZOOM_API_SEC']
download_folder = 'transcripts'

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

# Given the meeting ID, returns the location of downloaded WebVTT file
def get_meeting_transcript(meeting_id):
    store_path = os.path.join(download_folder, str(meeting_id) + '.vtt')
    
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
                    return store_path
        else:
            print("Fetching meeting " + str(meeting_id) + "failed")
            return None
        
    return store_path