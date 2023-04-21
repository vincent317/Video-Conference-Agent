# Video-Conference-Agent

Use notebook_playground for exploration purpose.
Use flask_backend for production purpose.

Pipeline Demo TODO:
1. Generate the information needed for the meeting report aside from action_items & summaries.

Backend Structure TODO:
1. Change all services (asr_service, zoom_service, chatgpt_service, etc) into an OOP style design and initialize them at once
2. zoom_service: download all data we need from a meeting at once at stored in an organized file format

ASR TODO:
1. Pack the swagger_client package into future Dockerfile