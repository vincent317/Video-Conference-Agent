1. Backend Structure:
a. Change all services (asr_service, zoom_service, chatgpt_service, etc) into an OOP style design and initialize them at once (Priority: 3)
b. zoom_service: download all data we need from a meeting at once at stored in an organized file format (Priority: 4)

2. ASR:
a. In asr_service, now I am using the dummy meeting meta information:
    "NAME = "TEST MEETING" # TODO: get from zoom
    DESCRIPTION = "N/A" # TODO: get from zoom
    PARTICIPANT_COUNT = 3 # TODO: get from zoom"
    Change it to data we get from ZOOM API. (Priority: 4)
b. Pack the swagger_client package into future Dockerfile (Priority: 2)

3. FrontEnd
a. Enforce pattern to Meeting Date/Time input
b. Fix 'show/hide long summary' toggle issue in downloaded html

4. Cloud
a. Make a Dockerfile and deploy to the cloud.

5. Efficiency
a. Cache the generated meeting data in Redis.
