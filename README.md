# Jarvis

A personal productivity agent built from scratch to learn GenAI.

## Stack
- Python 3.10
- Ollama (qwen2.5:7b)
- SQLite for memory

## Setup
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull qwen2.5:7b
```

## Run
```bash
python agent.py
```

## Commands
- `/help` — show all commands
- `/clear` — wipe memory
- `/history` — show recent messages
- `/tools` — list tools

## Structure
- `agent.py` — main loop
- `llm.py` — Ollama wrapper + error handling
- `tools.py` — tool functions, schemas, dispatcher
- `memory.py` — SQLite persistence
- `commands.py` — slash command handlers
- `config.py` — constants, system prompt

## Progress
- [x] Day 1: Hello Ollama + streaming
- [x] Day 2: Multi-turn conversation loop
- [x] Day 3: First tool (get_current_time)
- [x] Day 4: Mock emails + calendar tools, refactor
- [x] Day 5: SQLite persistent memory
- [x] Day 6: Polish, error handling, /commands, system prompt
- [x] Day 7: Anthropic prompt engineering tutorial + Week 1 reflection
