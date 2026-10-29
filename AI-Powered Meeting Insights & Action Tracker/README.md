# AI-Powered Meeting Insights & Action Tracker
## Features

- Upload a meeting transcript (`.txt` or `.pdf`)
- Generate a concise executive summary
- Extract key discussion points
- Identify action items with owners and deadlines (when mentioned)
- Detect decisions made during the meeting
- Extract explicit deadlines/due dates
- Export the full report as Markdown (`.md`) or JSON (`.json`)
- Simple, clean Streamlit UI

## Project Structure

```
AI-MEETING-SUMMARIZER/
│── app.py              # Streamlit UI (entry point)
│── utils.py             # File reading (txt/pdf) + report export helpers
│── summarizer.py         # LLM call logic (Gemini / Ollama) + JSON parsing
│── prompts.py            # Prompt templates
│── requirements.txt
│── README.md
│── sample_data/
│   └── sample_meeting_transcript.txt
│── output/
│   ├── sample_generated_report.md
│   └── sample_generated_report.json
```
## How It Works

1. `utils.py` reads the uploaded `.txt`/`.pdf` file and cleans the text.
2. `prompts.py` builds a strict instruction prompt asking the LLM to return
   **structured JSON** (executive summary, discussion points, action items,
   decisions, deadlines, next steps).
3. `summarizer.py` sends that prompt to Gemini or Ollama, then safely parses
   the JSON response (stripping markdown fences, handling malformed output).
4. `app.py` renders the structured result in a clean Streamlit UI and lets
   the user export it as Markdown or JSON.

## Tech Stack

- **Python 3.9+**
- **Streamlit** – UI
- **Google Gen AI SDK (`google-genai`)** – Gemini API access (free tier), using `gemini-3.5-flash` by default
- **Ollama Python SDK** – optional local LLM backend
- **pdfplumber** – PDF text extraction
- **Pandas** – (available for any further tabular processing/extension)

## Possible Extensions

- Add DOCX/PDF export of the final report (not just Markdown/JSON)
- Support multiple transcript uploads / batch processing
- Add speaker-level analysis (who talked the most, sentiment per speaker)
- Add LangChain for multi-step chains (e.g. summarize long transcripts in
  chunks before final extraction)
- Persist reports to a database instead of just downloading

## Notes

- Gemini's free tier has rate limits — for very long transcripts, consider
  chunking the transcript before sending it to the model.
- The JSON parser in `summarizer.py` is defensive: it strips markdown code
  fences and isolates the outermost `{ ... }` block so minor formatting
  quirks from the LLM don't crash the app.
