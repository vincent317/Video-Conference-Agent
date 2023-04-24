from flask import Flask
from flask_restx import Api, Resource, reqparse, fields
from flask_cors import CORS
import os, json
from dotenv import load_dotenv
from datetime import datetime as dt

# load environment variables
env_path = ".env"
if not os.path.exists(env_path):
    raise ValueError('env_path environment variable not found')
load_dotenv(dotenv_path=env_path)

from services import zoom_service, asr_service, asr_postprocessing_service
from services import chatgpt_service
from utils.ai_transcript_chunking import generate_overlapping_chunk
# from utils.action_item_parsing import action_item_processing

# make sure file structure exists
required_dirs = ['services/audios', 
                 'services/azure_durations', 
                 'services/azure_transcripts', 
                 'services/clean_durations', 
                 'services/clean_transcripts', 
                 'services/zoom_transcripts']

for directory in required_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")

# Flask & Swagger Initialization
app = Flask(__name__)
api = Api(app, version='1.0', title='VCA Backend API',
    description='Sample APIs',)
CORS(app)

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
    
# parser = reqparse.RequestParser()
# parser.add_argument('agenda_items')
# @api.route('/summarization/<meeting_id>')
# @api.doc(params={'meeting_id': 'Meeting ID'})
# class Summarization(Resource):
#     @api.expect(parser)
#     def post(self, meeting_id):
#         args = parser.parse_args()
#         agenda_items = args['agenda_items']

#         current_dir = os.getcwd()
#         os.chdir("services")
#         zoom_transcript_file = zoom_service.get_meeting_transcript(meeting_id)
#         azure_transcript_file, duration_file = asr_service.asr(meeting_id)

#         clean_transcript_path, _ = asr_postprocessing_service.asr_postprocessing(azure_transcript_file, 
#                                                                                           duration_file, zoom_transcript_file, 3, meeting_id)
#         with open(clean_transcript_path) as f:
#             clean_transcript_string = f.read()
        
#         res = chatgpt_service.generate_summaries(agenda_items, clean_transcript_string)
#         os.chdir(current_dir)
#         return res


# @api.route('/participants_data/<meeting_id>')
# @api.doc(params={'meeting_id': 'Meeting ID'})
# class Participants(Resource):
#     def get(self, meeting_id):
#         return zoom_service.get_participants_data(meeting_id)

parser = reqparse.RequestParser()
parser.add_argument('agenda_items')
parser.add_argument('meeting_date')
@api.route('/meeting_info/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class MeetingInfo(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('agenda_items')
    # parser.add_argument('meeting_date')
    @api.expect(parser)
    def post(self, meeting_id):
        args = parser.parse_args()
        print(args)
        agenda_items = args['agenda_items']
        meeting_date = args['meeting_date'] # will be in format for YYYY-MM-DD HH:MM

        meeting_title, part_cnt = zoom_service.get_meeting_data(meeting_id)

        current_dir = os.getcwd()
        os.chdir("services")
        zoom_transcript_file = zoom_service.get_meeting_transcript(meeting_id)
        azure_transcript_file, duration_file = asr_service.asr(meeting_id)

        clean_transcript_path, clean_duration_path = asr_postprocessing_service.asr_postprocessing(azure_transcript_file, 
                                                                                          duration_file, zoom_transcript_file, part_cnt, meeting_id)
        with open(clean_transcript_path) as f:
            clean_transcript_string = f.read()
        
        action_items_overlapped = []
        parsed_2d_list = generate_overlapping_chunk(clean_transcript_string)
        for chunk in parsed_2d_list:
            string = '\n'.join(chunk)
            action_items_arr = None
            while True:
                action_items_arr = chatgpt_service.reduce_action_items(string)
                if action_items_arr is not None:
                    break
            action_items_overlapped.append(action_items_arr)
        action_items = chatgpt_service.combine_action_items(action_items_overlapped)

        summary = chatgpt_service.generate_summaries(agenda_items, clean_transcript_string)

        part_arr = zoom_service.get_participants_data(meeting_id)
        with open(clean_duration_path) as f:
            duration = json.load(f)
        part_info = {}
        if part_arr is not None:
            for p in part_arr:
                join_time = dt.strptime(p['join_time'], '%Y-%m-%dT%H:%M:%SZ')
                actual_meeting_time = dt.strptime(meeting_date, '%Y-%m-%dT%H:%M')
                print(join_time)
                print(actual_meeting_time)

                part_info[p['name']] = {'late': 'late' if join_time > actual_meeting_time else 'on-time'}
                if p['name'] in duration:
                    part_info[p['name']]['duration'] = str(round(duration[p['name']],2))+'s (' + str(round(duration[p['name']]/duration['total']*100, 2))+'%)'
                else:
                    part_info[p['name']]['duration'] = '0s (0%)'
        
        os.chdir(current_dir)
        return {'meeting_title': meeting_title,
                'meeting_date': meeting_date,
                'participants': part_info,
                'summary': summary, 'action_items': action_items}



if __name__ == '__main__':
    app.run(debug=True)