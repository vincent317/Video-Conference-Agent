# Video-Conference-Agent

Set-Up:

1. Create some empty data storage folders under the flask_backend/services.
The flask_backend/services folder should look like this:

flask_backend/services:
----/audios
----/azure_durations
----/azure_transcripts
----/clean_durations
----/clean_transcripts
----/zoom_transcripts
----/asr_postprocessing_service.py
----/asr_service.py
----/chatgpt_service.py
----/zoom_service.py

2. Put .env in the /flask_backend folder (same folder with controller.py)

3. Install ffmpeg on your local machine (https://ffmpeg.org/download.html)