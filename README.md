# AI-Powered Disability Form Assistant Chatbot

## Overview
This repository contains an AI-powered chatbot designed to assist individuals with disabilities in filling out government forms. The chatbot leverages Retrieval-Augmented Generation (RAG) to enhance the accuracy and relevance of its responses by retrieving specific information from uploaded PDFs and DOCX files. The chatbot is designed to provide step-by-step guidance, simplifying complex procedures and ensuring that users can accurately complete the required forms.

## Features
- **AI-Powered Assistance**: The chatbot provides intelligent and context-aware guidance to users, helping them fill out forms with ease.
- **Retrieval-Augmented Generation (RAG)**: Utilizes RAG to fetch relevant information from uploaded documents, enhancing the precision of the responses.
- **Multi-Format Document Support**: Capable of processing and extracting information from both PDFs and DOCX files.
- **Conversation Memory**: Maintains conversation history to provide consistent and contextually relevant interactions.
- **Dialogue Logging**: Saves user-chatbot interactions for further analysis and inclusion in research or reports.

## Technology Stack
- **Python**: Core programming language used for developing the chatbot.
- **OpenAI**: Provides the language model for generating AI-driven responses.
- **LangChain**: A framework for building applications powered by language models, used for prompt templates, memory management, and document processing.
- **PyMuPDF (fitz)**: Used for reading and extracting text and images from PDF files.
- **Pytesseract**: An OCR tool for extracting text from images within documents.
- **docx2txt**: A tool for extracting text and images from DOCX files.
- **FAISS**: A library for efficient similarity search and clustering of dense vectors, used for storing and retrieving document embeddings.
- **Pydantic**: Used for data validation and settings management.
- **dotenv**: For managing environment variables securely.

## Methodology

### 1. **Setup and Configuration**
   - **Environment Setup**: Python and necessary dependencies are installed, with environment variables managed securely using `.env` files.
   - **API Key Management**: OpenAI API keys are stored securely using environment variables to prevent accidental exposure.

### 2. **Document Processing**
   - **PDF and DOCX Handling**: The system supports multiple document formats, allowing users to upload PDFs and DOCX files. Text and images are extracted from these documents.
   - **Optical Character Recognition (OCR)**: Text is extracted from images within documents using Pytesseract, enhancing the chatbot's ability to reference and utilize all available information.
   - **Text Splitting and Embedding**: Extracted text is split into manageable chunks and embedded using OpenAI embeddings. These embeddings are then stored in a FAISS vector store for efficient retrieval.

### 3. **Chatbot Interaction**
   - **Large Language Model (LLM) Integration**: The chatbot is powered by an OpenAI language model, which generates responses based on the context retrieved from the vector store and the current conversation.
   - **Prompt Engineering**: The chatbot uses carefully designed prompt templates to ensure that responses are accurate, relevant, and easy to understand.
   - **Conversation Memory**: The chatbot maintains a memory of the conversation to provide contextually relevant responses throughout the interaction.

### 4. **User Interaction**
   - **Interactive Session**: Users interact with the chatbot through a command-line interface, where they can ask questions, upload new documents, and receive guidance on filling out forms.
   - **Dialogue Logging**: All interactions are logged and saved, including user inputs, chatbot responses, and response times. This data can be used for further analysis, user experience evaluation, and research.

### 5. **Evaluation Metrics**
   - **Response Time Logging**: The time taken for the chatbot to generate a response is logged for each interaction, allowing for performance analysis.
   - **Accuracy Assessment**: The chatbot's responses are compared against correct answers to evaluate accuracy. Metrics such as precision, recall, and overall accuracy are computed to assess performance.
   - **User Feedback**: After each session, users are prompted to rate their experience, providing qualitative data that can be used to improve the system.

## Installation

### Prerequisites
- Python 3.8+
- An OpenAI API key

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/segunumoru1/Adult-Disability-Payment-Assistant-Chatbot.git
   cd disability-form-assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the Application**:
   ```bash
   python utils.py
   ```

## Usage

### Adding Documents
- During the chatbot interaction, users can upload additional documents by typing `add document` and providing the file path. The new document will be processed and added to the knowledge base.

### Asking Questions
- Users can ask questions related to the forms by typing their query. The chatbot will retrieve relevant information from the processed documents and generate a response.

### Exiting the Session
- To end the interaction, users can type `exit`. The chatbot will save the dialogue and prompt the user for a rating.

### Example Interaction
```plaintext
Welcome! I'm here to assist you with the Adult Disability Payment form.
Type 'exit' to end the conversation.
You can also type 'add document' to add a new document to the knowledge base.

User > What is the deadline for the form?
Assistant: The deadline is on page 3, section 2.
Response time: 2.5 seconds

User > exit
Please rate your experience (1-5): 4
Thank you for your rating: 4/5
Thank you for using the Disability Form Assistant. Goodbye!
```

## Evaluation and Performance Metrics
- **Response Time**: Logs the time taken for each response, allowing for analysis of latency and performance under different conditions.
- **Accuracy**: Measures the correctness of responses by comparing them with predefined correct answers.
- **User Experience**: Users provide ratings after each session, offering insights into the usability and helpfulness of the chatbot.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions for improvements.

## Contact
For any questions or issues, please contact [segunumoru1@gmail.com].

---

This README provides a comprehensive overview of the AI-powered Disability Form Assistant Chatbot, outlining the technology stack, methodology, installation steps, usage examples, and evaluation metrics. It is designed to give users and developers a clear understanding of the project and how to interact with and contribute to it.
