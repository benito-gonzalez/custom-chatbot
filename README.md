# Streamlit Chatbot with GPT-3.5-turbo and RAG Expert Models

## Overview
This web application is a chatbot built using Streamlit, integrating two powerful language models: GPT-3.5-turbo for general conversation and the Retrieval-Augmented Generation (RAG) model for specialized knowledge in Formula 1, football, and basketball. Users can choose among the three experts, each utilizing the RAG model to provide informed responses.

## Dependencies
Ensure you have the following dependencies installed:

```bash
pip install -r requirements.txt
```

## Scraping and Data Collection
Data for Formula 1, football, and basketball is gathered using custom scrapers powered by BeautifulSoup. These scrapers fetch news articles from various websites, extracting relevant information. The collected data is stored in a dedicated directory for further processing.

## Llama-index Integration
Llama-index is employed to generate document vectors for the scraped articles. This library converts the textual data into index vectors, facilitating efficient information retrieval.


## Streamlit Application
The main application is developed using Streamlit. Users can interact with the chatbot, select an expert, and pose questions related to Formula 1, football, or basketball. The chatbot leverages GPT-3.5-turbo for general conversation and dynamically integrates the RAG model to provide specialized answers.

Run the application:

```bash
streamlit run main.py
```

## Usage
1. Access the web application through the provided URL.
2. Choose an expert (Formula 1, football, or basketball).
3. Type your questions and receive responses enriched with current knowledge from the RAG model.

## Notes
- Ensure a stable internet connection as the application relies on OpenAI's GPT-3.5-turbo model for conversation.
- Periodically update the scraped data to keep the knowledge base current.


## Acknowledgments
- OpenAI for providing the GPT-3.5-turbo model.
- Llama-index for efficient document indexing.