# Jarvis

A personal productivity agent built from scratch to learn GenAI.

## Goal
Natural language interface to email, calendar, and notes. Runs fully locally using Ollama.

## Tech Stack
- Python 3.10
- Ollama (local LLM runtime)
- Llama 3.2

## Setup

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is installed and `llama3.2:latest` is pulled:
```bash
ollama pull llama3.2:latest
```

## Run

```bash
python hello.py
```

## Progress
- [x] Day 1: Hello Ollama + streaming
- [x] Day 2: Conversation loop
- [x] Day 3: First tool
- [x] Day 4: Multiple tools
- [ ] Day 5: SQLite memory
- [ ] Day 6: Polish + refactor
- [ ] Day 7: Prompt engineering tutorial
