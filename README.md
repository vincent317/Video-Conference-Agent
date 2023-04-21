# Video-Conference-Agent

Set-Up:

1. Create some empty data storage folders under the flask_backend/services.
The flask_backend/services folder should look like this:

flask_backend/services: <br>
----/audios <br>
----/azure_durations <br>
----/azure_transcripts <br>
----/clean_durations <br>
----/clean_transcripts <br>
----/zoom_transcripts <br>
----/asr_postprocessing_service.py <br>
----/asr_service.py <br>
----/chatgpt_service.py <br>
----/zoom_service.py <br>

2. Put .env in the /flask_backend folder (same folder with controller.py)

3. Install ffmpeg on your local machine (https://ffmpeg.org/download.html)

4. Start the flask server, and use existing meeting IDs such as 85996564215 from (https://docs.google.com/spreadsheets/d/1xdy_1uytJoWVuvVO9DVq1IFbABYl2MG2NJXxODqLG4k/edit#gid=0)
