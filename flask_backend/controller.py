from flask import Flask, jsonify
from flask_restx import Api, Resource

import zoom_service, action_item_service, time
from utils.webvtt_parsing import webvtt_parsing
from utils.ai_transcript_chunking import generate_overlapping_chunk
from utils.action_item_parsing import action_item_processing

# Flask & Swagger Initialization
app = Flask(__name__)
api = Api(app, version='1.0', title='VCA Backend API',
    description='Sample APIs',)

@api.route('/action_item_extraction/<meeting_id>')
@api.doc(params={'meeting_id': 'Meeting ID'})
class Meeting(Resource):
    def get(self, meeting_id):
        start = time.time()
        vtt_file_location = zoom_service.get_meeting_transcript(meeting_id)
        fetch_zoom = time.time()
        print("Zoom API call taks: %s seconds" % (fetch_zoom - start))
        meeting_transcript_string = webvtt_parsing(vtt_file_location)
        parse_transcript = time.time()
        print("WebVTT parsing takes: %s seconds" % (parse_transcript - fetch_zoom))
        parsed_2d_list = generate_overlapping_chunk(meeting_transcript_string)
        break_transcript = time.time()
        print("Breaking transcript into chunks taks %s seconds" % (break_transcript - parse_transcript))
        overlapped = []
        for chunk in parsed_2d_list:
            string = '\n'.join(chunk)
            action_items_arr = None
            while True:
                action_items_arr = action_item_service.extract_action_item(string)
                if action_items_arr is not None:
                    break
            overlapped.append(action_items_arr)
        chatgpt_call = time.time()
        print("ChatGPT call takes: %s seconds" % (chatgpt_call - break_transcript))
        ret = action_item_processing(overlapped)
        remove_overlapping = time.time()
        print("Remove duplicates takes: %s seconds" % (remove_overlapping - chatgpt_call))
        return ret

if __name__ == '__main__':
    app.run(debug=True)