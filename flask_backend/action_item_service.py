import os
import requests
import openai

API_KEY = os.environ['OPENAI_API_KEY']
url = 'https://api.openai.com/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY}

def extract_action_item(meeting_transcript_string):
    prompt = "Extract action items from this meeting transcript in this format:\n WHO: ACTION ITEMS"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "This is a meeting transcript."},
            {"role": "assistant", "content": meeting_transcript_string},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data).json()
    print(response)
    print(response['choices'][0]['message']['content'])
    