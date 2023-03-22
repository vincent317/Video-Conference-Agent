import os

API_KEY = os.environ['OPENAI_API_KEY']

from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings

llm = OpenAI(model_name="gpt-3.5-turbo-0301", openai_api_key = API_KEY)
prompt = "Given the meeting transcript, extract the action items in the format of WHO will DO SOMETHING."

def extract_action_item(meeting_transcript_string):
    source_chunks = []
    splitter = RecursiveCharacterTextSplitter()
    for chunk in splitter.split_text(meeting_transcript_string):
        source_chunks.append(Document(page_content=chunk))
    search_index = FAISS.from_documents(source_chunks, OpenAIEmbeddings(openai_api_key = API_KEY))
    chain = load_qa_chain(llm)

    print("Querying GPT-3.5...")
    str_res = chain({"input_documents": search_index.similarity_search(prompt, k=4),"question": prompt}, 
                    return_only_outputs=True)["output_text"]
    return str_res.split('\n')
    