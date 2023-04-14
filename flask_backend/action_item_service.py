import os
import requests
import openai

API_KEY = os.environ['OPENAI_API_KEY']
url = 'https://api.openai.com/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY}

def extract_action_item(meeting_transcript_string):
    prompt = "Using the given transcript, extract action items for each meeting participant using this format: \"{WHO}: {ACTION ITEM}\""
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You need to extract action items from a meeting transcript in the given format."},
            {"role": "assistant", "content": meeting_transcript_string},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        action_items_string = response.json()['choices'][0]['message']['content']
        return action_items_string.split('\n')
    else:
        return ["GPT-3.5 API failed.\n"]
    