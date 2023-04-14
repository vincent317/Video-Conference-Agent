from flask import Flask, jsonify
from flask_restx import Api, Resource

import zoom_service, action_item_service
from utils.webvtt_parsing import webvtt_parsing
from utils.transcript_parsing import process_transcript


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
        parsed_2d_list = process_transcript(meeting_transcript_string)
        overlapped = []
        for chunk in parsed_2d_list:
            string = '\n'.join(chunk)
            action_items_arr = action_item_service.extract_action_item(string)
            overlapped.append(action_items_arr)
        # TODO: deal with overlapping
        return overlapped

if __name__ == '__main__':
    app.run(debug=True)