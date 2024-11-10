import requests
import streamlit as st
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import StorageContext, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import google.generativeai as genai
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class RAG:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.documents = None
        self.nodes = None
        self.query_engine = None
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

    def load_documents(self):
        loader = PDFReader()
        self.documents = loader.load_data(file=self.pdf_path)
        logging.debug(f"Loaded {len(self.documents)} documents from {self.pdf_path}")
        print("############# load documents")

    def parse_documents(self):
        parser = SimpleNodeParser.from_defaults(chunk_size=200, chunk_overlap=10)
        self.nodes = parser.get_nodes_from_documents(self.documents)
        logging.debug(f"Extracted {len(self.nodes)} nodes from documents")
        print("############### nodes")
    
    def setup_llm_and_index(self):
        llm = Gemini(model="models/gemini-pro")
        embed_model = GeminiEmbedding(model_name="models/embedding-001")
        
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.chunk_size = 512

        vector_index = VectorStoreIndex(self.nodes)
        self.query_engine = vector_index.as_query_engine()

    def query(self, query_text):
        response_vector = self.query_engine.query(query_text)
        return response_vector.response
    
    # Update the response for legal and mental health assistance
    def response(self, query_text):
        res = self.query(query_text)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # New prompt for legal and mental health support
        prompt = (
            f"This data {res} is from the legal and mental health support system for the question {query_text}. "
            f"Use the given data to provide a helpful, empathetic, and supportive response to the question. "
            f"Ensure the response is sensitive to the context of mental health or legal issues. "
            f"Provide any necessary advice and resources where appropriate. "
            f"EXPLANATION: Then explain the situation and provide additional support suggestions if needed."
        )
        res = model.generate_content(prompt).text
        return res
    
    # For food and health related legal or mental health queries, modify the prompt accordingly
    def response_health(self, query_text):
        query_text = f"Based on the mental health or legal status of the patient, suggest resources or advice that would help in {query_text}. " \
                      f"Ensure the response is sensitive, compassionate, and informative."
        res = self.query(query_text)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"This data {res} is from the legal and mental health support system for the question {query_text}. "
            f"Use the provided data to give clear, supportive, and compassionate answers. "
            f"EXPLANATION: Then explain your suggestions or advice, and how it can be helpful to the user."
        )
        res = model.generate_content(prompt).text
        return res



# Initialize RAG
rag = RAG(pdf_path="path_to_your_pdf_or_data")  # Adjust path as necessary
rag.load_documents()
rag.parse_documents()
rag.setup_llm_and_index()

# Streamlit setup
st.title("EmpowerHer: Women's Help Chat")

# Load Lottie animation
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_animation = load_lottie_url("https://lottie.host/0c341f67-405d-46a8-8225-bb7f5fbed80a/KQX1aTTSGv.json")
st_lottie(lottie_animation, height=300, width=300, key="animation")

# Initialize session state for chat history if not already
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to handle message input and display the chat history
def handle_message():
    user_input = st.session_state["user_message"]
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"sender": "User", "message": user_input})

        # Query the RAG system and get the response
        bot_response = rag.response(user_input)
        
        # Append bot response to chat history
        st.session_state.chat_history.append({"sender": "Bot", "message": bot_response})

        # Clear input box
        st.session_state["user_message"] = ""

# Display chat history
for chat in st.session_state.chat_history:
    sender = "👤" if chat["sender"] == "User" else "🤖"
    st.markdown(f"{sender} **{chat['sender']}:** {chat['message']}")

# Input box for user message with enter key submission
st.text_input("Your message:", key="user_message", on_change=handle_message)