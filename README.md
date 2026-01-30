<div id="top">

<div align="center">

# TALK-TO-YOUR-DOCUMENT-AGENT

<em>Empower your documents with AI conversation assistance.</em>

<img src="https://img.shields.io/github/last-commit/DenysFlnk/talk-to-your-document-agent?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/DenysFlnk/talk-to-your-document-agent?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/DenysFlnk/talk-to-your-document-agent?style=default&color=0080ff" alt="repo-language-count">

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)

---

## Overview

**talk-to-your-document-agent**

An AI assistant for analyzing and querying documents. Self-hosted, privacy-conscious, and designed for seamless interaction with your documents in Ukrainian. 
The core features include:

- Full Ukrainian language support with a self-hosted large language model (LLM)
- Supported document formats: docx, xlsx
- Core capabilities: summarization, targeted search, and statistics extraction based on provided documents and user prompts
- UI with reports and chat
- Local-first, privacy-preserving workflow: no cloud dependency unless you opt in

---

## Project Structure

```sh
└── talk-to-your-document-agent/
    ├── README.md
    ├── agent
    │   ├── __init__.py
    │   ├── agent.py
    │   ├── app.py
    │   ├── prompts.py
    │   ├── tools
    │   └── utils
    ├── core
    │   └── config.json
    ├── docker-compose.yaml
    ├── report-ui
    │   ├── .gitignore
    │   ├── README.md
    │   ├── index.html
    │   ├── package-lock.json
    │   ├── package.json
    │   ├── public
    │   ├── src
    │   ├── tsconfig.app.json
    │   ├── tsconfig.json
    │   ├── tsconfig.node.json
    │   └── vite.config.ts
    ├── report_app
    │   ├── files
    │   ├── main.py
    │   └── requirements.txt
    ├── requirements.txt
    └── settings
        └── settings.json
```

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python, JavaScript
- **Package Manager:** Pip, Npm
- **Container Runtime:** Docker

### Installation

Build talk-to-your-document-agent from the source and install dependencies:

1. **Clone the repository:**

```sh
    ❯ git clone https://github.com/DenysFlnk/talk-to-your-document-agent
```

2. **Navigate to the project directory:**

```sh
    ❯ cd talk-to-your-document-agent
```

3. **Install the dependencies:**

```sh
    ❯ pip install -r requirements.txt, report_app/requirements.txt
```

```sh
    report-ui ❯ npm i
```

4. **Run local LLM of your choice (in project I use qwen3)**
5. **Specify LLM in DIAL config and environment variables**

```json
  "models": {
    "qwen/qwen3-8b": {
      "displayName": "QwenLM",
      "endpoint": "http://host.docker.internal:1234/v1/chat/completions",
      "type": "chat"
    }
  }
```

```shell
export DEPLOYMENT_NAME=qwen/qwen3-8b
```

### Usage

Run the project with:

**Agent**

```sh
❯ python -m agent.app
```

**Report app**

```sh
report_app ❯ uvicorn main:app --host 0.0.0.0 --port 8000
```

**UI**

```sh
report-ui ❯ npm run dev
```

**DIAL-AI**

```sh
❯ docker compose up -d
```

---

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square

---
