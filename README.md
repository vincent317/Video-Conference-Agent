# Video-Conference-Agent

Use notebook_playground for exploration purpose.
Use flask_backend for production purpose.

Backend Structure TODO:
1. Change all services (asr_service, zoom_service, chatgpt_service, etc) into an OOP style design and initialize them at once
2. zoom_service: download all data we need from a meeting at once at stored in an organized file format

ASR TODO:
1. Pack the swagger_client package into future Dockerfile
2. Fix the manually set container_sas_url & blob_sas_url