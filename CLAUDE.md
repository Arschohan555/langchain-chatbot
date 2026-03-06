# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A chatbot application built with LangChain and Ollama, supporting CLI, web (Streamlit), and API interfaces. Uses local LLM models via Ollama for conversational AI with conversation history management.

## Commands

### Running the Application

```bash
# CLI interface with .env configuration (main.py reads from .env)
python main.py

# CLI interface (hardcoded settings)
python app.py

# Web UI (Streamlit)
streamlit run streamlit_app.py

# API server (FastAPI)
python -m uvicorn src.main:app --reload
```

### Dependencies

```bash
# Install via uv (recommended)
uv pip install -r requirements.txt

# Or via pip
pip install -r requirements.txt
```

### Ollama Setup

Ensure Ollama is running locally before using the chatbot:
```bash
ollama serve
ollama pull qwen2.5-coder:3b
```

## Architecture

### Multiple Entry Points
- **main.py**: CLI chatbot that reads configuration from `.env` file
- **app.py**: CLI chatbot with hardcoded model settings (qwen2.5-coder:3b, temperature 0.7)
- **streamlit_app.py**: Full-featured web UI with custom dark theming and session stats
- **src/main.py**: Minimal FastAPI application (foundation for API development)

### Key Components
- **LLM Provider**: ChatOllama from `langchain-ollama`
- **Prompt Template**: ChatPromptTemplate with system message + MessagesPlaceholder for chat history + human question
- **Chain Pattern**: `prompt | llm | StrOutputParser` (LangChain pipe operator)
- **Chat History**: In-memory list with HumanMessage/AIMessage pairs
- **Context Limiting**: Max 5 conversation turns by default to prevent context overflow

### Configuration
Environment variables in `.env`:
- `MODEL_NAME`: Ollama model (default: qwen2.5-coder:3b)
- `TEMPERATURE`: LLM creativity 0-1 (default: 0.7)
- `MAX_TURNS`: Max conversation turns (default: 5)

### src/ Directory Structure
Modular architecture foundation with:
- `api/`: API route handlers (empty, extend as needed)
- `config/`: Settings management (settings.py)
- `core/`: Core utilities (logging.py)
- `models/`: Data models (empty, extend as needed)
- `providers/`: LLM provider integrations - ollama.py and openai.py stubs
- `services/`: Business logic services (empty, extend as needed)
