# LLM CLI Helper

A command-line Python tool powered by OpenAI's models that suggests and runs `zsh` commands based on user-prompted tasks.

---

## Features

- Suggests `zsh`-compatible shell commands for user-defined tasks [I tested it on mac-os].
- Runs suggested commands in a controlled environment once prompted with a yes.
- After running the command, if there is an error, searches for the error, and gives suggestions to debug
- User can use the suggested command to debug

---

## Requirements

- Python 3.8+
- `zsh` installed on your system
- An OpenAI API key

---

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd llm-cli-helper
```
### 2 Install Requirements
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=<your key>
```

### 3 Run the code
```bash
python helper.py
```

### 4 For exiting, type 'exit'. If the command suggested is executed successfully then the program exits. 
