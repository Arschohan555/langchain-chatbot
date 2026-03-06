# LangChain Chatbot

A local AI chatbot powered by LangChain and Ollama, featuring both command-line and web interfaces for conversational AI.

## Overview

This project provides a clean implementation of an LLM-powered chatbot using LangChain's chain composition pattern with Ollama as the local model provider. The application maintains conversation history and supports multiple interface types.

## Requirements

- Python 3.11 or higher
- [Ollama](https://github.com/ollama/ollama) installed and running locally
- Required model pulled (default: `qwen2.5-coder:3b`)

## Installation

1. **Clone and install dependencies:**

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

2. **Set up Ollama:**

```bash
# Ensure Ollama is running
ollama serve

# Pull the model you intend to use
ollama pull qwen2.5-coder:3b
```

3. **Configure environment (optional):**

Create or edit `.env` in the project root:

```env
MODEL_NAME=qwen2.5-coder:3b
TEMPERATURE=0.7
MAX_TURNS=5
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | Ollama model identifier | `qwen2.5-coder:3b` |
| `TEMPERATURE` | LLM creativity (0.0 - 1.0) | `0.7` |
| `MAX_TURNS` | Maximum conversation turns | `5` |

## Usage

### Command-Line Interface

**Basic version (hardcoded settings):**
```bash
python app.py
```

**Configured version (reads from .env):**
```bash
python main.py
```

**CLI Commands:**
- Type your message and press Enter to chat
- Enter `clear` to reset conversation history
- Enter `quit` or `exit` to close the application

### Web Interface

Launch the Streamlit web UI:

```bash
streamlit run streamlit_app.py
```

The web interface provides:
- Custom dark-themed UI with professional styling
- Real-time conversation history
- Session statistics (turns used/remaining)
- Clear chat functionality
- Model configuration display

### API Server

Start the FastAPI development server:

```bash
python -m uvicorn src.main:app --reload
```

## Architecture

### Chain Composition

The chatbot uses LangChain's pipe operator pattern:

```
PromptTemplate → ChatOllama → StrOutputParser
```

- **PromptTemplate**: System message + chat history + user question
- **ChatOllama**: Local LLM inference via Ollama
- **StrOutputParser**: Parses AI response to string

### Chat History

Conversation history is stored in-memory as a list of `HumanMessage` and `AIMessage` objects. The chain is invoked with both the current question and accumulated chat history to maintain context.

### Context Limiting

To prevent context window overflow, the application limits conversation turns (default: 5). When the limit is reached, users are prompted to clear the chat history.

## Project Structure

```
langchain-chatbot/
├── main.py              # CLI chatbot (.env config)
├── app.py               # CLI chatbot (hardcoded config)
├── streamlit_app.py     # Web UI interface
├── src/
│   ├── main.py          # FastAPI application
│   ├── api/             # API route handlers
│   ├── config/          # Configuration management
│   ├── core/            # Core utilities
│   ├── models/          # Data models
│   ├── providers/       # LLM providers
│   │   ├── ollama.py
│   │   └── openai.py
│   └── services/        # Business logic
├── .env                 # Environment configuration
├── pyproject.toml       # Project metadata
└── README.md
```

## License

MIT
