from flask import Flask
from flask_restx import Api, Resource, reqparse

import zoom_service, chatgpt_service
from utils.webvtt_parsing import webvtt_parsing
from utils.ai_transcript_chunking import generate_overlapping_chunk
from utils.action_item_parsing import action_item_processing

# Flask & Swagger Initialization
app = Flask(__name__)
api = Api(app, version='1.0', title='VCA Backend API',
    description='Sample APIs',)

@api.route('/action_item_extraction/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class ActionItem(Resource):
    def get(self, meeting_id):
        vtt_file_location = zoom_service.get_meeting_transcript(meeting_id)
        meeting_transcript_string = webvtt_parsing(vtt_file_location)
        parsed_2d_list = generate_overlapping_chunk(meeting_transcript_string)
        overlapped = []
        for chunk in parsed_2d_list:
            string = '\n'.join(chunk)
            action_items_arr = None
            while True:
                action_items_arr = action_item_service.extract_action_item(string)
                if action_items_arr is not None:
                    break
            overlapped.append(action_items_arr)
        ret = action_item_processing(overlapped)
        return ret

@api.route('/summarization/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class Summarization(Resource):
    def get(self, meeting_id):
        parser = reqparse.RequestParser()
        parser.add_argument('agenda_items')
        args = parser.parse_args()
        agenda_items = args['agenda_items']

        vtt_file_location = zoom_service.get_meeting_transcript(meeting_id)
        meeting_transcript_string = webvtt_parsing(vtt_file_location)
        
        res = generate_summaries(agenda_items, meeting_transcript_string):




if __name__ == '__main__':
    app.run(debug=True)