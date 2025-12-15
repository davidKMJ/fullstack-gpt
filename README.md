# fullstack-gpt
![Static Badge](https://img.shields.io/badge/status-in_progress-orange?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/type-learning_project-blue?style=for-the-badge)

A portfolio of GPT-powered applications demonstrating various use cases of LLM integration, including document Q&A, private local models, quiz generation, and website content analysis.

## How to Start

### Environment
- Python 3.11
- Pipenv (package manager)
- OpenAI API key (for DocumentGPT, QuizGPT, and SiteGPT)
- Ollama (optional, for PrivateGPT)

### Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd fullstack-gpt

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Set up environment variables
export OPENAI_API_KEY=your_api_key_here

# Run the application
streamlit run Home.py

# Open in browser
# http://localhost:8501
```

## Key Features
1. **DocumentGPT** – Upload and chat with documents (PDF, TXT, DOCX) using OpenAI embeddings and vector search
2. **PrivateGPT** – Private document Q&A using local Ollama models with no data leaving your machine
3. **QuizGPT** – Generate interactive quizzes from uploaded files or Wikipedia articles with multiple-choice questions
4. **SiteGPT** – Ask questions about website content by loading and indexing sitemap URLs
5. **MeetingGPT** – Meeting analysis application (in development)

## Technical Stack
- **Streamlit** – Web application framework for building interactive UIs
- **LangChain** – Framework for building LLM-powered applications with document loaders and chains
- **OpenAI API** – GPT models for chat, embeddings, and text generation
- **FAISS** – Vector database for efficient similarity search and retrieval
- **Ollama** – Local LLM runtime for private, offline document processing

## Project Structure
```
fullstack-gpt/
├── Home.py                    # Main entry point and navigation hub
├── pages/                     # Streamlit multi-page application modules
│   ├── 01_DocumentGPT.py      # Document Q&A with OpenAI
│   ├── 02_PrivateGPT.py       # Private document chat with Ollama
│   ├── 03_QuizGPT.py          # Quiz generation from files/Wikipedia
│   ├── 04_SiteGPT.py          # Website content Q&A via sitemap
│   └── 05_MeetingGPT.py       # Meeting analysis (in development)
├── notebooks/                 # Jupyter notebooks for experimentation
│   ├── 01_introduction.ipynb
│   ├── basics.ipynb
│   └── notebook.ipynb
├── files/                     # Sample files and media for testing
│   ├── chapter_one.txt
│   ├── chunks/
│   └── podcast.mp3
├── Pipfile                    # Pipenv dependency configuration
├── Pipfile.lock               # Locked dependency versions
├── prompt.json                # Prompt templates
├── prompt.yaml                # YAML prompt configuration
└── README.md                  # Project documentation
```
