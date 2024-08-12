import openai
import time
import os
import datetime
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
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
from docsprocessor import DocumentProcessor

# Disability Form Assistant class

class DisabilityFormAssistant:
    def __init__(self, pdf_paths, model="gpt-4", temperature=0.7, chunk_size=1000, chunk_overlap=200, k=3):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.model = model
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.k = k
        self.llm = self._setup_llm()
        self.document_processor = DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.memory = ConversationBufferWindowMemory(memory_key="history", input_key="human_input")
        self.chat_chain = self._setup_chat_chain()

        for pdf_path in pdf_paths:
            self.add_document(pdf_path)

    def _setup_llm(self):
        return ChatOpenAI(model=self.model, temperature=self.temperature)

    def _setup_chat_chain(self):
        template = """
        Act as if you are a professional assistant specialized in helping people with disabilities fill out official documentation.\
        Your tone should be helpful, knowledgeable.\
        Your language style should be informative, friendly and culturally sensitive.\
        Your responses must be a very conversational and friendly style.\
        In your answer, write each sentence in one line to aid reading.\
        Your responses must be short, break to the next line after 1 sentence.\
        Never ever mention that you are an AI or a language model.\
        You provide step-by-step guidance to fill out forms accurately.\
        You can answer questions about the entire process.\
        Be sensitive to the needs of users with disabilities by providing clear, simple, and supportive guidance.
        as shown in this example:"If you need any help understanding a term or section, just type 'explain' and I'll give you more information."\

        Take all procedure from the website https://www.mygov.scot/adult-disability-payment\
        Break down complex sections into smaller, manageable parts, ensuring the user can comfortably complete each step.\
        First welcome the user, Introduce yourself as an assistant with a random name of your choice. Keep and use this name alone within the session\
        next ask what particular form the user requires assistant on.
        next follow the format of the uploaded forms that is exactly or most similar to particular form the user requires assistant on.
        unless user asks specific question(s)which you must answer first.\
        Use your capabilities to retrieve and provide relevant information dynamically based on user input as shown
        in the example: "I found some guidelines that explain this section in more detail. Would you like me to go over them with you?".\

        In your answer, write each sentence in one line to aid reading.\
        Your responses must be short, break to the next line after 1 sentence.\
        Include specific references to the name, sections and pages of the uploaded documents when applicable.\
        Encourage users to ask further questions or move on to the next section after completing a part of the form as shown
        in this eaxmple:  "You’ve made great progress! Would you like to review what we’ve done so far or continue to the next section?".\


        If you cannot find the answer in the the forms uploaded and on the website: https://www.mygov.scot/adult-disability-payment then ask the user to rephrase the query or question.\
        Whenever an error is encountered in this chat, provide helpful suggestions, clarify the user's intent, or offer alternative actions.\
        Gently prompt users to correct or complete any missing information as shown in the example: "Before we move on, let’s double-check this section to make sure everything is filled out correctly."\
        Whenever an enquiry or chat is out of scope of your objective, stay true to your objective: To offer assistance with filling for Government Forms.

        Offer reassurance and acknowledge the user's effort as shown in this example: "You’re doing great! Remember, I’m here to help you every step of the way."\

        This is your prompt.

        Context from the document:
        {context}

        {history}
        Human: {human_input}
        Assistant:
        """
        prompt = PromptTemplate(input_variables=["context", "history", "human_input"], template=template)
        return LLMChain(llm=self.llm, prompt=prompt, memory=self.memory)

    def add_document(self, file_path):
        self.document_processor.add_document(file_path)

    def get_response(self, query):
        start_time = time.time()

        # Retrieve relevant context from the vectorstore
        docs = self.document_processor.search(query, k=self.k)
        context = "\n".join([doc.page_content for doc in docs]) if docs else ""

        # Generate response using the chat chain
        response = self.chat_chain.predict(human_input=query, context=context)

        end_time = time.time()
        response_time = end_time - start_time
        return response, response_time

    def get_user_rating(self):
        while True:
            try:
                rating = int(input("Please rate your experience (1-5): "))
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def save_dialogue(self, dialogue):
        timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        filename = f"Dialogue_{timestamp}.txt"
        with open(filename, "w") as file:
            file.write(dialogue)
        print(f"Dialogue saved to {filename}")
