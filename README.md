# Streamlit Chatbot with GPT-3.5-turbo and RAG Expert Models

## Overview
This project aims to develop a sports chatbot capable of providing real-time information about various sports events and news. The chatbot utilizes a combination of Natural Language Processing (NLP) models, web scraping techniques, and an intuitive web interface to allow users to interact and receive timely updates on their favorite sports.

## Technologies Used
### Python
Python was chosen as the primary programming language for its versatility and extensive libraries for NLP and web scraping.

### Streamlit
Streamlit was used as the web framework for building the user interface. It offers a simple and intuitive way to create interactive web applications for data science and machine learning projects.

### Beautiful Soup 4
Beautiful Soup 4, a Python library, was utilized for web scraping. It provided powerful tools for extracting information from HTML and XML files, making it ideal for gathering sports news from online sources.

### Llama-Index
LlamaIndex is a simple, flexible data framework for connecting custom data sources to large language models (LLMs).

### Docker Compose
Docker Compose is used to orchestrate the deployment of the various components of the system. The docker-compose.yml file defines the configuration for each service, including the build context, Dockerfile, ports mapping, and volume mounting. This ensures consistency and reproducibility across different environments and simplifies the deployment process.
### AWS (Amazon Web Services)
AWS was chosen as the cloud platform for hosting the application. It provided scalability, reliability, and a wide range of services to support the deployment and operation of the chatbot.

## Project Structure
1. **Web Scraper**: This component is responsible for gathering sports news data from various online sources. It utilizes the Beautiful Soup 4 library, a powerful tool for web scraping in Python. The scraper is designed to extract headlines and article content from popular sports news websites such as Marca, As, Sport, and Mundo Deportivo. By targeting specific HTML elements and patterns on these websites, the scraper retrieves the latest news articles related to sports events and updates.

2. **Index Generator**: Once the sports news data is collected by the web scraper, it is passed to the index generator component. Here, the news articles are processed and transformed into tokens using embedding models. These tokens represent the semantic meaning of the articles and are used to index the content for efficient retrieval. The index generator employs advanced techniques to generate embeddings that capture the context and relevance of each article, enhancing the chatbot's ability to provide accurate and informative responses.

3. **User Interface**: The user interface is developed using Streamlit, a web framework for creating interactive data visualization and machine learning applications. It serves as the primary interface through which users interact with the chatbot system. The interface allows users to select their preferred language, chat interface style, and sports expert. Users can then engage in conversations with the chatbot, asking questions and receiving real-time updates on sports news and events.

4. **API**: The system includes an API component that exposes endpoints for /scrapers and /vectors. These endpoints are called by the cron container to trigger the web scraping process and vector generation. The API is implemented using FastAPI or Flask, providing a lightweight and efficient way to communicate between components within the system.

Overall, the project structure is designed to facilitate the seamless integration of the various components, allowing for efficient data retrieval, processing, and presentation to users through the intuitive web interface. The modular architecture and use of industry-standard tools and technologies contribute to the scalability, maintainability, and extensibility of the sports chatbot system.
## RAG Approach
The chatbot implements the RAG (Retriever, Answerer, Generator) approach to provide real-time information to the model. The Retriever component retrieves relevant information from online sources using web scraping techniques. The Answerer component utilizes NLP models to generate responses based on the retrieved information and user queries. Finally, the Generator component produces the final response to the user, incorporating context and ensuring relevance.

## How to Run the Application
1. Clone this repository to your local machine.
2. Install Docker Compose if not already installed.
3. Navigate to the project directory in your terminal.
4. Run the following command to start the application:
```bash
docker-compose up
```
If you want to check the deployed version, go to the provided URL http://ec2-3-64-8-248.eu-central-1.compute.amazonaws.com/