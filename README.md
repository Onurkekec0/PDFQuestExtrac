# PDFQuestExtrac

# PDF Summary and Quiz Generator

This project is designed to process PDF documents written in English, summarize their content using a summarization function, and then generate multiple-choice questions related to the content by leveraging the GPT (Generative Pre-trained Transformer) network. It is implemented in Python and showcased on a web server using the Django framework.

## Installation

Before you can run the project, you need to install its dependencies. Make sure you have Python installed on your system, and then follow the steps below:

1. Clone the repository to your local machine:
```bash
git clone <repository-url>
```
2. Navigate to the project directory:

```bash
cd PDFQuestExtrac
```
3. Install the required Python packages:
```bash
pip install django spacy pymupdf nltk openai sumy re
```
4. Download the necessary Spacy language model:
```bash
python -m spacy download en_core_web_sm
```
## Configuration
Before running the application, you need to set your OpenAI API key for the project to function correctly. Locate the views.py file in the project, and replace the placeholder <<openai api should come here>> with your actual OpenAI API key:
```bash
openai.api_key = "<<openai api should come here>>"

```

## Running the Application
After installing the dependencies and configuring the API key, you can start the Django web server to use the application:

```bash
python manage.py runserver

```
Navigate to the URL provided by the Django server to access the web interface, where you can upload PDF files and receive summaries and generated multiple-choice questions.

## Contributing
Contributions to the PDF Summary and Quiz Generator are welcome. Here are a few ways you can help:

Report bugs
Suggest new features
Improve documentation
Submit pull requests with fixes and improvements
