"""
prompts.py
All prompt templates used to instruct the LLM for meeting summarization
and action item extraction.
"""

SYSTEM_INSTRUCTION = """You are an expert executive assistant who specializes in
reading raw meeting transcripts and turning them into clean, structured,
professional meeting reports. You are precise, you never invent information
that is not present in the transcript, and you always follow the exact
output format you are asked for."""


EXTRACTION_PROMPT_TEMPLATE = """You will be given a raw meeting transcript.
Read it carefully and extract the following information.

Return your answer as **valid JSON only** (no markdown fences, no extra text
before or after) matching exactly this schema:

{{
  "executive_summary": "string - a concise 3-5 sentence summary of the whole meeting",
  "key_discussion_points": ["string", "string", ...],
  "action_items": [
    {{
      "task": "string - what needs to be done",
      "owner": "string or null - who is responsible, null if not mentioned",
      "deadline": "string or null - due date/deadline, null if not mentioned"
    }}
  ],
  "decisions_made": ["string", "string", ...],
  "deadlines": [
    {{
      "item": "string - what the deadline is for",
      "date": "string - the deadline/date mentioned"
    }}
  ],
  "next_steps": ["string", "string", ...]
}}

Rules:
- If a section has no relevant content in the transcript, return an empty list [] for it.
- Do not fabricate owners or deadlines that are not stated or clearly implied in the transcript.
- Keep the executive_summary tight and readable, no bullet points inside it.
- Keep each list item short and clear (one sentence each, ideally).
- Output must be strictly valid JSON, parsable by a JSON parser.

Meeting Transcript:
\"\"\"
{transcript}
\"\"\"
"""


def build_extraction_prompt(transcript: str) -> str:
    """Fill the transcript into the extraction prompt template."""
    return EXTRACTION_PROMPT_TEMPLATE.format(transcript=transcript)
