
# Fake News Detection Chrome Extension

## Project Overview

This project is a Chrome extension designed to detect the legitimacy of news and posts across social media platforms and websites. By using advanced language models and AI techniques, it analyzes selected content—either text or images—and provides users with a legitimacy score and detailed explanations regarding the authenticity of the content.

The system architecture integrates the LangChain framework and Gemini API for advanced natural language processing and fake news detection. The front end, developed as a Chrome extension, captures the content, and the backend processes the data using machine learning models and distributed systems, ensuring both scalability and quick response times.

## Key Features

1. **Chrome Extension Integration**: Users can seamlessly select text or images in their browser, which are then passed to the backend for analysis.
2. **LangChain Integration**: This framework is used to construct complex language model pipelines, making the system capable of reasoning over different kinds of content and providing contextual insights.
3. **Gemini API**: The Gemini API is employed in the backend to process and evaluate the legitimacy of the news by running checks based on large-scale datasets and language models.
4. **FastAPI for Backend**: Provides a robust and scalable API for handling requests from the Chrome extension.
5. **Streamlit Visualization**: A real-time dashboard to display the legitimacy score, detailed explanations, and insights provided by the LangChain-Gemini system.
6. **Distributed System Architecture**: Ensures the system can handle large volumes of data while maintaining low latency and high throughput.

## Project Architecture

The project's architecture is divided into the following components:

1. **Chrome Extension**:
   - Captures selected content (text and images) from the browser.
   - Sends the content as a request to the backend API for analysis.

2. **FastAPI Backend**:
   - Manages API endpoints for receiving requests from the Chrome extension.
   - Passes the data to the LangChain-powered pipeline.
   - Interfaces with the Gemini API to process and verify the legitimacy of the news content.

3. **LangChain + Gemini API**:
   - LangChain organizes the logic and reasoning required to process different forms of content.
   - The Gemini API evaluates the content, providing legitimacy scores and explanations based on NLP models.

4. **Streamlit Dashboard**:
   - Displays real-time results of the analysis, including the legitimacy score, breakdown of the reasoning process, and more.

## Workflow

1. **User Interaction**: The user highlights text or selects an image on a webpage.
2. **Data Capture**: The Chrome extension captures this content and sends it to the FastAPI server.
3. **Processing**:
   - The FastAPI backend invokes the LangChain framework, which organizes the flow for processing the input.
   - The content is sent to the Gemini API for legitimacy checks.
   - The API responds with a legitimacy score and detailed explanation based on the analysis.
4. **Visualization**: The results are displayed on a Streamlit dashboard, allowing the user to see the authenticity score and explanations for how the determination was made.

## Dependencies

To run this project, the following dependencies are required:

- **Python** (3.x)
- **FastAPI**: For managing API endpoints
- **LangChain**: For constructing NLP pipelines and complex reasoning logic
- **Gemini API**: For fake news detection
- **Streamlit**: For visualizing results in real-time
- **Chrome Extension**: For capturing and sending content from the user's browser
- **Additional Libraries**:
  - `uvicorn` (for FastAPI server)
  - `requests` (for API interaction)
  - `pydantic` (for data validation)

Make sure all dependencies are installed by running:

```bash
pip install -r requirements.txt
```

## Usage

1. **Chrome Extension**:
   - Once the extension is installed, select any text or image on a webpage.
   - Right-click and choose the option to analyze the content.
   - The extension will send the content to the backend for processing.

2. **API Server**:
   - The FastAPI server receives the content and processes it through LangChain and Gemini API.
   - The API returns the results, including the legitimacy score and an explanation of why the content is considered legitimate or fake.

3. **Streamlit Dashboard**:
   - The results are visualized in the Streamlit app, showing detailed insights into the analysis process, including the score, the reasoning behind it, and any specific flags or issues identified.

## Example Flow

1. A user highlights a piece of news text saying, "X politician involved in scandal."
2. The extension captures the text and sends it to the FastAPI server.
3. The server passes the data through LangChain, which invokes the Gemini API to check the content's legitimacy.
4. The API returns a legitimacy score of, say, **30%** along with an explanation that the text is related to an unverified rumor on social media.
5. The results are then displayed on the Streamlit dashboard for the user to review.

## Future Enhancements

- **User Authentication**: Implement a user login system for storing analysis history.
- **Machine Learning Model Improvement**: Continuously update the ML model for detecting fake news based on evolving patterns.
- **Support for More Languages**: Expand the system to analyze news in multiple languages.
- **Scalability**: Further optimize the distributed system for handling higher volumes of traffic.
