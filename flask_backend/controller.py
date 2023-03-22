from flask import Flask, jsonify
from flask_restx import Api, Resource

import zoom_service, action_item_service
from utils.webvtt_parsing import webvtt_parsing

# Flask & Swagger Initialization
app = Flask(__name__)
api = Api(app, version='1.0', title='VCA Backend API',
    description='Sample APIs',)

@api.route('/action_item_extraction/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class Meeting(Resource):
    def get(self, meeting_id):
        vtt_file_location = zoom_service.get_meeting_transcript(meeting_id)
        meeting_transcript_string = webvtt_parsing(vtt_file_location)
        return jsonify(action_item_service.extract_action_item(meeting_transcript_string))

if __name__ == '__main__':
    app.run(debug=True)