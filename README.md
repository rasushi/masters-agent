# Master's Planning & Execution Agent

An AI-powered agent designed to help students plan and manage their master's application journey, from university research to application preparation.

**Project status:** Early development

## Overview

The goal of this project is to build an AI agent that can understand a student's goals and constraints, research relevant master's programmes, compare universities, and assist with application planning.

The project is being developed incrementally to explore the fundamentals of Agentic AI, LLMs, tool calling, memory, and workflow orchestration.

## Current Features

- Connects to an LLM through the Groq API.
- Defines Python functions as callable tools.
- Uses LLM tool calling to select a relevant function.
- Executes requested tools in Python.
- Sends tool results back to the LLM.
- Generates a final response using the tool result.

## Tech Stack

- Python
- Groq API
- OpenAI GPT-OSS model
- Python-dotenv
- JSON

## Project Structure

```text
masters-agent/
│
├── main.py
├── tools.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── venv/
```

## Learning Objective

This project is also a hands-on learning exercise to understand how LLM-powered agents work internally, rather than relying entirely on agent frameworks.