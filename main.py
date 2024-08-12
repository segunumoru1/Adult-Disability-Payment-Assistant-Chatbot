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
from utils import DisabilityFormAssistant

# Defining the main class object
def main():
    pdf_paths = [
        "Referrral Form 03.pdf",
        "Referrral Form 02.pdf",
        "Referrral Form 01.pdf",
        "Nutritional Risk Assessment 01.pdf",
        "Nutritional Risk Assessment 02.pdf",
        "Nutritional Risk Assessment 03.pdf"
    ]  # Add your PDF paths here
    assistant = DisabilityFormAssistant(pdf_paths)
    dialogue = ""

    print("Welcome!This system is designed to assist with filling Government forms.")
    print("We are here to help you fill out your government forms, guiding you every step of the way.")
    print("If anything isn't clear or if you need an explanation, just ask—no question is too small.")
    print("We can go at your own pace, and We're happy to repeat or clarify as needed. Let's get started whenever you're ready!.")
    print("Please note:")
    print()
    print("You may type 'exit' to end the conversation at any point.")
    print("You may also type 'add document' to add a new document to the knowledge base if you are authorized to do so.")
    print("Please type your first query and an assistant is automatically assigned to you.")
    while True:
        user_input = input("User > ")
        dialogue += f"User: {user_input}\n"

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'add document':
            file_path = input("Enter the path to the document: ")
            assistant.add_document(file_path)
            print("Document added successfully!")
            dialogue += f"Document added: {file_path}\n"
            continue

        response, response_time = assistant.get_response(user_input)
        print(f"Assistant: {response}")
        print(f"Response time: {response_time:.2f} seconds")

        dialogue += f"Assistant: {response}\n"
        dialogue += f"Response time: {response_time:.2f} seconds\n\n"

    rating = assistant.get_user_rating()
    dialogue += f"User rating: {rating}/5\n"

    assistant.save_dialogue(dialogue)
    print(f"Thank you for your rating: {rating}/5")
    print("Thank you for using the Disability Form Assistant. Goodbye!")

if __name__ == "__main__":
    main()