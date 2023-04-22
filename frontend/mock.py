from flask import Flask
from flask_restx import Api, Resource, reqparse, fields
from flask_cors import CORS
import os
from dotenv import load_dotenv


# Flask & Swagger Initialization
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="VCA Backend API",
    description="Sample APIs",
)
CORS(app)


@api.route("/meeting_info/<meeting_id>")
@api.doc(params={"meeting_id": "Meeting ID"})
class MeetingInfo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("agenda_items")

    @api.expect(parser)
    def post(self, meeting_id):
        return {
            "meeting_title": "23min_demo_meeting",
            "meeting_date": "2023-03-03 19:59:40",
            "participants": {
                "Yooni Choi": {"late": "on-time", "duration": "424.4s (32.94%)"},
                "Jiahe Feng": {"late": "late", "duration": "458.44s (35.58%)"},
                "DAZHI PENG": {"late": "late", "duration": "405.68s (31.48%)"},
            },
            "summary": {
                "Overall summary": "The meeting involved Dazhi Peng, Jeffrey Feng, and Yooni Choi discussing the progress of a data scripting project. Jeffrey and Yooni had encountered difficulties with scraping dynamic websites, and Dazhi suggested using the Selenium library to automate web browsers. Jeffrey agreed to help Yooni with Python installation issues, and Dazhi assigned action items for creating a GitHub branch and reporting progress by the next day. Dazhi also suggested adding new team members to help with the project.",
                "Short agenda summaries": {
                    "data scraping": "The team discussed issues with data scraping and agreed to use Selenium library to automate web browsers, update Python environment, and create a GitHub branch to track progress.",
                    "add new member": "Dazhi Peng suggests adding new members to the team to help with the data scripting project.",
                },
                "Detailed agenda summaries": {
                    "data scraping": "During the meeting, Jeffrey and Uni reported that they were having difficulty scraping data from some dynamic websites on their list, and mentioned issues they were facing with Python libraries like Beautiful Soup. Dazhi recommended using the Selenium library to automate web browsers, and suggested that updating their Python environment might help with the installation issues. Jeffrey agreed to help Uni with the installation issues, and also agreed to create a GitHub branch to track the team's progress on the project. Dazhi asked the team to report progress to him by the next day, and suggested adding new members to the team to help with the project if progress continued to be slow, which Jeffrey and Uni agreed to.",
                    "add new member": "Dazhi Peng suggests adding new members to the team to help with the data scripting project, which has been progressing slowly. Jeffrey Feng and Yooni Choi report that they are stuck with scraping some of the websites on their list, as some of them are dynamic and they couldn't get the data they need. Dazhi Peng suggests using the Selenium library, a software testing framework used to automate web browsers, to interact with the website and perform automated testing to check for errors. Jeffrey also suggests updating Yooni's Python environment as installing Beautiful Soup was causing her issues. Dazhi Peng assigns an action item to Jeffrey to create a GitHub branch to track the progress of the project, and to report progress to him by the next day. Dazhi also suggests adding new members to the team to help out with the project, and will send updates in a week.",
                },
                "Additional summaries": "No additional information was provided in the context about the data scraping and add new member agenda items.",
            },
            "action_items": [
                "Jeffrey Feng: Read Selenium documentation, help Uni with Python issues, create GitHub branch, send Dazhi link to GitHub branch, schedule a meeting with DAZHI PENG. ",
                "Yooni Choi: Update Python environment before installation. ",
                "DAZHI PENG: Help Jeffrey and Uni with the data scripting project by suggesting the use of Selenium library, read Beautiful Soup documentation, schedule meeting with Jeffrey, ask Jeffrey and Yooni to report progress by tomorrow, consider doing recordings for previous project as an extra item, send updates on the new team members in a week, look for new team members to help with the project.",
            ],
        }


if __name__ == "__main__":
    app.run(debug=True)
