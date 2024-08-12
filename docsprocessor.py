# import the necessary libraries
import fitz  # PyMuPDF
import json
import requests
import time
import datetime
import warnings
import tiktoken
import faiss
import fitz  # PyMuPDF
from docx import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.schema import SystemMessage
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    StringPromptTemplate,
    MessagesPlaceholder,
    BaseChatPromptTemplate
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback
import fitz  # PyMuPDF
from docx import Document
import docx2txt
import io
from PIL import Image
import pytesseract
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import os
import openai

# Get the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def process_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

            # Extract images
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Use PIL to open the image
                image = Image.open(io.BytesIO(image_bytes))

                # Perform OCR on the image
                image_text = pytesseract.image_to_string(image)
                text += f"\nImage {img_index + 1} text:\n{image_text}\n"

        return text

    def process_docx(self, docx_path):
        # Extract text
        text = docx2txt.process(docx_path)

        # Extract images
        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)
        docx2txt.process(docx_path, temp_dir)

        # Perform OCR on extracted images
        for img_file in os.listdir(temp_dir):
            if img_file.endswith(('png', 'jpg', 'jpeg', 'tiff')):
                img_path = os.path.join(temp_dir, img_file)
                image_text = self.extract_text_from_image(img_path)
                text += f"\nImage {img_file} text:\n{image_text}\n"
                os.remove(img_path)  # Clean up the temporary image file

        os.rmdir(temp_dir)  # Remove the temporary directory
        return text

    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def process_file(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            return self.process_pdf(file_path)
        elif file_extension.lower() in ['.docx', '.doc']:
            return self.process_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def add_document(self, file_path):
        text = self.process_file(file_path)
        texts = self.text_splitter.split_text(text)

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_texts(texts, self.embeddings)
        else:
            self.vectorstore.add_texts(texts)

    def search(self, query, k=3):
        if self.vectorstore is None:
            return []
        return self.vectorstore.similarity_search(query, k=k)


# Usage example:
processor = DocumentProcessor()
processor.add_document('Referrral Form 03.pdf')
processor.add_document('Referrral Form 02.pdf')
processor.add_document('Referrral Form 01.pdf')
processor.add_document('Nutritional Risk Assessment 01.pdf')
processor.add_document('Nutritional Risk Assessment 02.pdf')
processor.add_document('Nutritional Risk Assessment 03.pdf')
processor.add_document('Nutritional Risk Assessment 04.pdf')
results = processor.search("personal details")
print(results)