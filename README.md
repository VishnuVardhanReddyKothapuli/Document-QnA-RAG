# Document Q&A RAG Web App

A modern, fast, and minimalist web application that allows users to upload PDF documents and ask questions about them using Retrieval-Augmented Generation (RAG). Built with FastAPI, LangChain, and Groq.

## Features

- **Drag-and-Drop PDF Upload**: Easily upload your course materials or documents.
- **AI-Powered Chat**: Ask questions about your document and get instant, accurate answers.
- **FastAPI Backend**: High-performance asynchronous backend.
- **Minimalist UI**: Clean, Udemy-inspired interface.
- **Dockerized**: Ready for containerized deployment.
- **Render Ready**: Includes `render.yaml` for instant deployment on Render.

## Tech Stack

- **Backend**: FastAPI, Uvicorn, Python 3.11
- **AI & RAG**: LangChain, ChromaDB, HuggingFace Embeddings, Groq (Llama 3)
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Deployment**: Docker, Render

## Setup and Installation

### Prerequisites

- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VishnuVardhanReddyKothapuli/Document-QnA-RAG.git
   cd Document-QnA-RAG
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory and add your Groq API key and optional model:
   ```ini
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=openai/gpt-oss-120b
   ```

3. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open your browser and navigate to `http://localhost:8000` to start using the app.

### Docker Setup

You can easily run this application using Docker.

1. **Build the image:**
   ```bash
   docker build -t genai-pdf-qna .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 --env-file .env genai-pdf-qna
   ```

## Deployment on Render

This project includes a `render.yaml` Blueprint file for simple deployment on [Render.com](https://render.com/).

1. Connect your GitHub repository to Render.
2. Render will automatically detect the `render.yaml` file.
3. Provide your `GROQ_API_KEY` in the Render dashboard when prompted.
4. Deploy!
