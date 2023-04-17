import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

API_KEY = os.environ['OPENAI_API_KEY']
url = 'https://api.openai.com/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY}

def extract_action_item(meeting_transcript_string):
    prompt = "Using the given transcript, extract action items for each meeting participant using this format: \"{WHO}: {ACTION ITEM}\""
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You need to extract action items from a meeting transcript in the given format."},
            {"role": "assistant", "content": meeting_transcript_string},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        action_items_string = response.json()['choices'][0]['message']['content']
        return [a for a in action_items_string.split('\n') if len(a) > 0]
    else:
        return None

def return_llm_answer(question, chain, search_index):
    """Returns an answer to a given question using a language model."""
    return chain({'input_documents': search_index.similarity_search(question,
                 k=4), 'question': question},
                 return_only_outputs=True)['output_text']


def generate_summaries(agenda_text, transcript_text):
    """
    Generates meeting summaries using a language model and a similarity search index.

    Args:
    agenda_text (str): A string containing the agenda items discussed in the meeting.
    transcript_text (str): A string containing the full transcript of the meeting.

    Returns:
    tuple: A tuple containing three strings - the overall summary of the meeting, a dictionary of agenda item summaries, and
    a summary of topics not covered by the agenda items.

    This function generates meeting summaries by first splitting the transcript text into smaller chunks using a recursive
    character text splitter. The chunks are then converted into documents, which are used to create a search index for
    performing similarity searches. The function also loads a language model using the ChatOpenAI class and a QA chain using
    the load_qa_chain method.

    The function then uses the language model to generate an overall summary of the meeting by asking a pre-defined
    question. Next, it generates summaries for each agenda item by asking a question related to that item. Finally, it
    generates a summary of topics not covered by the agenda items by asking a general question.

    The function returns a tuple containing the three summaries as strings.
    """
    
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0301',
                     openai_api_key=API_KEY)

    source_chunks = []
    splitter = RecursiveCharacterTextSplitter()
    for chunk in splitter.split_text(transcript_text):
        source_chunks.append(Document(page_content=chunk))
    search_index = FAISS.from_documents(source_chunks,
            OpenAIEmbeddings(openai_api_key=API_KEY))

    chain = load_qa_chain(llm)

    # get overall summary of the meeting

    overall_summary = \
        return_llm_answer('Provide a summary of the meeting.', chain, search_index)

    # get a dictionary of agenda item summaries

    agenda_summaries = {}
    for agenda in agenda_text.split('.'):
        print(agenda)
        agenda_summaries[agenda] = \
            return_llm_answer('From this meeting, provide a summary related to this agenda item: '
                               + agenda, chain, search_index)

    # get summary not coverred by the agenda items

    num_agenda = len(agenda_summaries)
    additional_summaries = \
        return_llm_answer(
            f"Provide additional information if there are any additional items that were not mentioned" + 
            f"in the following {num_agenda} agenda items: {agenda_text}", chain, search_index
        )

    return (overall_summary, agenda_summaries, additional_summaries)

