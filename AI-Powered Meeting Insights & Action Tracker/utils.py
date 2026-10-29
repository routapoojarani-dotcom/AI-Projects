"""
utils.py
Helper functions for:
- Reading uploaded .txt / .pdf transcript files
- Cleaning transcript text
- Exporting the structured result as a Markdown / TXT / JSON report
"""

import io
import json
from datetime import datetime

import pdfplumber


def read_txt_file(uploaded_file) -> str:
    """Read a Streamlit-uploaded .txt file and return its text content."""
    raw_bytes = uploaded_file.read()
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1")


def read_pdf_file(uploaded_file) -> str:
    """Read a Streamlit-uploaded .pdf file and return extracted text."""
    text_chunks = []
    with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


def load_transcript(uploaded_file) -> str:
    """Detect file type by extension and route to the correct reader."""
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        text = read_pdf_file(uploaded_file)
    elif filename.endswith(".txt"):
        text = read_txt_file(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a .txt or .pdf file.")

    return clean_text(text)


def clean_text(text: str) -> str:
    """Basic cleanup: strip extra blank lines and trailing whitespace."""
    lines = [line.rstrip() for line in text.splitlines()]
    lines = [line for line in lines if line.strip() != "" or line == ""]
    cleaned = "\n".join(lines)
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned.strip()


def result_to_markdown(result: dict, meeting_title: str = "Meeting Report") -> str:
    """Convert the structured JSON result dict into a nicely formatted Markdown report."""
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [f"# {meeting_title}", f"*Generated on: {generated_on}*", ""]

    md.append("## Executive Summary")
    md.append(result.get("executive_summary", "N/A") or "N/A")
    md.append("")

    md.append("## Key Discussion Points")
    points = result.get("key_discussion_points", [])
    if points:
        for p in points:
            md.append(f"- {p}")
    else:
        md.append("_No discussion points identified._")
    md.append("")

    md.append("## Action Items")
    actions = result.get("action_items", [])
    if actions:
        md.append("| # | Task | Owner | Deadline |")
        md.append("|---|------|-------|----------|")
        for i, a in enumerate(actions, start=1):
            task = a.get("task", "N/A")
            owner = a.get("owner") or "Unassigned"
            deadline = a.get("deadline") or "Not specified"
            md.append(f"| {i} | {task} | {owner} | {deadline} |")
    else:
        md.append("_No action items identified._")
    md.append("")

    md.append("## Decisions Made")
    decisions = result.get("decisions_made", [])
    if decisions:
        for d in decisions:
            md.append(f"- {d}")
    else:
        md.append("_No decisions identified._")
    md.append("")

    md.append("## Deadlines")
    deadlines = result.get("deadlines", [])
    if deadlines:
        for d in deadlines:
            md.append(f"- **{d.get('item', 'N/A')}**: {d.get('date', 'N/A')}")
    else:
        md.append("_No explicit deadlines identified._")
    md.append("")

    md.append("## Next Steps")
    next_steps = result.get("next_steps", [])
    if next_steps:
        for n in next_steps:
            md.append(f"- {n}")
    else:
        md.append("_No next steps identified._")
    md.append("")

    return "\n".join(md)


def result_to_json_bytes(result: dict) -> bytes:
    """Convert the result dict into pretty-printed JSON bytes for download."""
    return json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8")
