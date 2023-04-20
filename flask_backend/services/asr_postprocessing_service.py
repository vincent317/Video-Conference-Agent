import re
import os
from . import chatgpt_service
import json

def parse_transcript(transcript_file, num_participant, num_line_threshold = 3):
    """Parse a transcript file and extract conversation text from each participant.

    Args:
        transcript_file (str): Path to the transcript file.
        num_participant (int): Number of participants in the conversation.
        num_line_threshold (int, optional): Number of conversation lines from each participant
            used for further matching. Defaults to 3.

    Returns:
        str: A concatenated string of the extracted conversation text from each participant.

    Raises:
        FileNotFoundError: If the transcript file path is invalid.

    """

    def end_transcript_loop(ppt_length):
        return len(ppt_length) == num_participant and all([v > 100 for v in ppt_length.values()])
    
    with open(transcript_file) as file:
        lines = file.readlines()

    ppt_text = {}
    ppt_length = {}

    for line in lines:
        if ": " not in line:
            continue
        line_split = line.split(": ")
        speaker, text = line_split[0], line_split[1]
        if speaker in ppt_length and ppt_length[speaker] > num_line_threshold:
            continue
        if speaker not in ppt_text:
            ppt_text[speaker] = text
        else:
            ppt_text[speaker] += text
        if speaker not in ppt_length:
            ppt_length[speaker] = 1
        else:
            ppt_length[speaker] += 1
        if end_transcript_loop(ppt_length):
            break
    result_text = ""
    for k, v in ppt_text.items():
        result_text += k + ": \n"
        result_text += v + "\n"
    return result_text

'''
Post processed the Azure and Zoom transcripts.

1; Cleans the zoom and azure transcripts.
2. Call ChatGPT to match the speakers and actual participant names.
3. Returns the cleaned duration dict.
'''
def asr_postprocessing(azure_transcript, azure_duration, zoom_transcirpt, num_participant, meeting_id):
    zoom_result_text = parse_transcript(zoom_transcirpt, num_participant)
    azure_result_text = parse_transcript(azure_transcript, num_participant)

    # write new transcription.txt files with speaker names
    ppt_match = chatgpt_service.ppt_matching_api_call(zoom_result_text, azure_result_text)
    old_transcript = open(azure_transcript).read()
    for k,i in ppt_match.items():
        old_transcript = re.sub(i,k, old_transcript)

    with open(azure_duration, 'r') as fp:
        duration = json.load(fp)
    # match name to duration dictionary
    duration = {y:x for x,y in {duration.get(k, k): v for v, k in ppt_match.items()}.items()}
    duration['total'] = sum(duration.values())

    final_path = os.path.join("clean_transcripts", str(meeting_id) + ".txt")
    with open(final_path, 'w') as f:
        f.write(old_transcript)
        print("ASR Postprocessing: Cleaned transcript saved at " + final_path)
    return duration, final_path