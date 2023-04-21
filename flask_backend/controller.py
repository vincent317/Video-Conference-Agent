from flask import Flask
from flask_restx import Api, Resource, reqparse, fields
import os
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(dotenv_path=env_path)
from services import zoom_service, asr_service, asr_postprocessing_service
from services import chatgpt_service
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
        current_dir = os.getcwd()
        os.chdir("services")
        zoom_transcript_file = zoom_service.get_meeting_transcript(meeting_id)
        azure_transcript_file, duration_file = asr_service.asr(meeting_id)

        clean_transcript_path, _ = asr_postprocessing_service.asr_postprocessing(azure_transcript_file, 
                                                                                          duration_file, zoom_transcript_file, 3, meeting_id)
        with open(clean_transcript_path) as f:
            clean_transcript_string = f.read()

        parsed_2d_list = generate_overlapping_chunk(clean_transcript_string)
        overlapped = []
        for chunk in parsed_2d_list:
            string = '\n'.join(chunk)
            action_items_arr = None
            while True:
                action_items_arr = chatgpt_service.reduce_action_items(string)
                if action_items_arr is not None:
                    break
            overlapped.append(action_items_arr)
            
        ret = chatgpt_service.combine_action_items(overlapped)
        os.chdir(current_dir)
        return ret
    
parser = reqparse.RequestParser()
parser.add_argument('agenda_items')
@api.route('/summarization/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class Summarization(Resource):
    @api.expect(parser)
    def post(self, meeting_id):
        args = parser.parse_args()
        agenda_items = args['agenda_items']

        current_dir = os.getcwd()
        os.chdir("services")
        zoom_transcript_file = zoom_service.get_meeting_transcript(meeting_id)
        azure_transcript_file, duration_file = asr_service.asr(meeting_id)

        clean_transcript_path, _ = asr_postprocessing_service.asr_postprocessing(azure_transcript_file, 
                                                                                          duration_file, zoom_transcript_file, 3, meeting_id)
        with open(clean_transcript_path) as f:
            clean_transcript_string = f.read()
        
        res = chatgpt_service.generate_summaries(agenda_items, clean_transcript_string)
        os.chdir(current_dir)
        return {"overrall symmary" : res[0], "agenda summaries" : res[1], "additional summaries" : res[2]}


# @api.route('/participants_data/<meeting_id>')
# @api.doc(params={'meeting_id': 'Meeting ID'})
# class Participants(Resource):
#     def get(self, meeting_id):
#         return zoom_service.get_participants_data(meeting_id)

if __name__ == '__main__':
    app.run(debug=True)