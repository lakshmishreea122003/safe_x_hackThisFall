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
    
from streamlit_lottie import st_lottie
import requests


# Functions
# Function to load Lottie animations from a URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# title
st.markdown(
    """
    <style>
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        background-color: #f2e6ff; /* Soft purple background */
        border-radius: 10px;
    }

    .title-text {
        font-family: Arial, sans-serif;
        font-size: 36px;
        font-weight: bold;
        color: #663399; /* Strong purple color */
        text-align: center;
    }

    .subtitle-text {
        font-size: 18px;
        font-style: italic;
        color: #555555; /* Dark grey for subtitle */
        margin-top: 5px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# HTML structure for the title and subtitle
st.markdown(
    """
    <div class="title-container">
        <div>
            <div class="title-text">EmpowerHer: Women's Help Chat</div>
            <div class="subtitle-text">Supporting you through every step of the way</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# lotti
lottie_animation = load_lottie_url("https://lottie.host/0c341f67-405d-46a8-8225-bb7f5fbed80a/KQX1aTTSGv.json")
st_lottie(lottie_animation, height=300, width=300, key="animation")


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

# rag query
query = st.text_area("Enter query here")
if query:
    res = rag.response(query)
    st.write(res)
