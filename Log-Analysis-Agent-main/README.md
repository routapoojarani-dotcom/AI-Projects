# Logs Agent with Strands Agents

## Aim

To create an AI Agent that can do log analysis

## Setup

```bash
git clone <repo-url>
cd log-analysis-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure Ollama is running locally (`http://localhost:11434`) with the `llama3.2` model pulled.

## Run

```bash
python logs_agent.py
```


# Log Analysis AI Agent using Python, Ollama & Strands Framework

## Situation (Problem / Idea)

In real-world DevOps and production environments, log files continuously grow and contain large amounts of system information, warnings, and errors.

Manually reading logs to identify issues, detect error patterns, and perform root cause analysis becomes time-consuming and inefficient for DevOps engineers.

I wanted to understand how AI Agents can assist DevOps teams by automating intelligent log analysis instead of manually checking application and system logs.

The idea was to build an AI-powered Log Analysis Agent capable of reading log files, understanding log patterns, and providing concise operational insights using Large Language Models.

---

## Task (Responsibility / Goal)

My task was to design and develop an AI Agent that could:

* Read and analyze log files automatically
* Detect occurrences of INFO, WARNING, and ERROR logs
* Summarize log analysis results in a concise format
* Follow a DevOps mindset for troubleshooting and root cause analysis
* Avoid hallucinated responses and unnecessary production actions
* Work locally using an open-source LLM model

The goal was to reduce repetitive manual log analysis effort and improve visibility into application/system issues.

---

## Action (Actual Implementation / Tools / Technologies)

I implemented the project using Python with the Strands Agentic Framework and integrated Ollama-based local LLM models.

### Core Implementation:

* Created a custom AI Log Analysis Agent using the `Agent()` class from the Strands framework.
* Defined a detailed `SYSTEM_PROMPT` to control agent behavior and enforce DevOps-focused log analysis.
* Integrated the `file_read` tool to allow the agent to access and analyze `.log` files.
* Configured a local Ollama-hosted `llama3.2` model for secure and offline AI inference.
* Implemented prompt-based log analysis for detecting INFO, WARNING, and ERROR occurrences from log files.

### Technologies & Tools Used:

* Python
* Strands Agentic Framework
* Ollama
* Llama 3.2 LLM
* AI Agents / Agentic AI
* Prompt Engineering
* Log Analysis
* DevOps Concepts

### Challenges Solved:

During development, I worked on:

* understanding agentic workflows,
* integrating local LLM inference,
* controlling hallucinations using system prompts,
* handling file-based analysis,
* and improving concise AI-generated operational insights.

---

## Result (Outcome / Quantifiable Impact)

* Successfully developed an AI-powered Log Analysis Agent capable of analyzing application log files locally.

* Automated log inspection workflows for detecting INFO, WARNING, and ERROR patterns.

* Reduced repetitive manual log-checking effort through AI-driven analysis.

* Built a reusable foundation for future DevOps AI automation workflows.

* Improved practical understanding of:

  * Agentic AI
  * LLM integration
  * Prompt engineering
  * AI-assisted DevOps operations
  * Log analysis workflows
  * Root cause analysis concepts

* Successfully integrated and automated 3+ log analysis operations including:

  * file reading,
  * log severity detection,
  * and AI-generated summarization using local LLMs.

## ATS-Friendly Resume + LinkedIn Description

🔹 Developed an AI-powered Log Analysis Agent using Python, Strands Agentic Framework, and Ollama-based Llama 3.2 model to automate log analysis workflows.

🔹 Automated 3+ log analysis operations including log file reading, INFO/WARNING/ERROR detection, and AI-generated log summarization using local LLM inference.

🔹 Integrated AI Agents, prompt engineering, and file-based analysis to support DevOps-focused troubleshooting and root cause analysis workflows.

🔹 Designed system prompts to minimize hallucinations and generate concise operational insights without performing unsafe production actions.

🔹 Gained hands-on experience in Agentic AI, Large Language Models (LLMs), local AI model deployment, Python automation, DevOps workflows, and AI-assisted operational analysis.

## BEST INTERVIEW EXPLANATION (Simple Speaking Style)

If interviewer asks:

“Explain your Log Analysis Agent project.”

You can say:

“This project is an AI-powered Log Analysis Agent developed using Python, Strands Agentic Framework, and Ollama-hosted Llama 3.2 model.

The main goal was to automate repetitive log analysis tasks usually performed manually by DevOps engineers.

The agent reads log files, analyzes log patterns, detects INFO, WARNING, and ERROR occurrences, and provides concise operational insights.

I used system prompts to control the AI agent behavior and ensure DevOps-focused analysis without hallucinations or unsafe actions.

Through this project, I gained practical understanding of Agentic AI, local LLM integration, prompt engineering, and AI-assisted DevOps automation workflows.”


