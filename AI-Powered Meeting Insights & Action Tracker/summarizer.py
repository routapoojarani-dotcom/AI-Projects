"""
summarizer.py
Handles the actual LLM call (Google Gemini free tier by default) and parses
the model's JSON response into a clean Python dict.

Also includes an optional Ollama (local Llama 3) backend so the intern can
run this fully offline if they don't want to use an API key.
"""

import json
import re

from prompts import SYSTEM_INSTRUCTION, build_extraction_prompt

DEFAULT_SCHEMA = {
    "executive_summary": "",
    "key_discussion_points": [],
    "action_items": [],
    "decisions_made": [],
    "deadlines": [],
    "next_steps": [],
}


def _extract_json(raw_text: str) -> dict:
    """
    LLMs sometimes wrap JSON in ```json fences or add stray text.
    This strips that out and parses the JSON safely.
    """
    text = raw_text.strip()

    # Remove markdown code fences if present
    text = re.sub(r"^```(json)?", "", text.strip(), flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text.strip()).strip()

    # If there's still leading/trailing junk, isolate the outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model did not return valid JSON. Raw output:\n{raw_text}"
        ) from e

    # Fill in any missing keys with safe defaults so the UI never crashes
    merged = DEFAULT_SCHEMA.copy()
    merged.update(parsed)
    return merged


def summarize_with_gemini(transcript: str, api_key: str, model_name: str = "gemini-3.5-flash") -> dict:
    """
    Calls Google's Gemini API (free tier) to extract structured meeting info.
    Requires: pip install google-genai
    Get a free API key at: https://aistudio.google.com/app/apikey

    Uses the current Google Gen AI SDK (google.genai). The older
    google-generativeai package and gemini-1.5-* models are retired as of 2026.
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    prompt = build_extraction_prompt(transcript)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    return _extract_json(response.text)


def summarize_with_ollama(transcript: str, model_name: str = "llama3.2") -> dict:
    """
    Calls a locally running Ollama instance instead of a cloud API.
    Requires: `pip install ollama` and `ollama pull llama3` with Ollama running locally.
    """
    import ollama

    prompt = build_extraction_prompt(transcript)
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0.2},
    )

    raw_text = response["message"]["content"]
    return _extract_json(raw_text)


def summarize_meeting(transcript: str, backend: str = "gemini", api_key: str = None,
                       model_name: str = None) -> dict:
    """
    Single entry point used by app.py. Routes to the chosen backend.

    backend: "gemini" or "ollama"
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty. Please upload a valid file.")

    if backend == "gemini":
        if not api_key:
            raise ValueError("Gemini API key is required. Get one free at https://aistudio.google.com/app/apikey")
        return summarize_with_gemini(transcript, api_key, model_name or "gemini-3.5-flash")

    elif backend == "ollama":
        return summarize_with_ollama(transcript, model_name or "llama3")

    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'gemini' or 'ollama'.")
