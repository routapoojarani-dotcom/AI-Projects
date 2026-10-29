"""
app.py
Streamlit UI for the AI Meeting Notes Summarizer & Action Item Extractor.

Run with:
    streamlit run app.py
"""

import streamlit as st

from utils import load_transcript, result_to_markdown, result_to_json_bytes
from summarizer import summarize_meeting

st.set_page_config(
    page_title="AI Meeting Notes Summarizer",
    page_icon="📝",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar - settings
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Settings")

backend = st.sidebar.selectbox(
    "LLM Backend",
    options=["gemini", "ollama"],
    help="Gemini = free cloud API (needs API key). Ollama = free local Llama 3 (needs Ollama installed).",
)

api_key = None
model_name = None

if backend == "gemini":
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey",
    )
    model_name = st.sidebar.selectbox(
        "Model",
        options=["gemini-3.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-flash"],
        index=0,
        help="gemini-1.5-* models are retired. Use gemini-3.5-flash (fast, free-tier friendly).",
    )
else:
    model_name = st.sidebar.text_input("Ollama model name", value="llama3.2")
    st.sidebar.caption("Make sure `ollama serve` is running locally and the model is pulled.")

meeting_title = st.sidebar.text_input("Report Title", value="Meeting Report")

st.sidebar.markdown("---")
st.sidebar.caption("Built for: AI Meeting Notes Summarizer & Action Item Extractor project")

# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------
st.title("📝 AI Meeting Notes Summarizer & Action Item Extractor")
st.write(
    "Upload a meeting transcript (`.txt` or `.pdf`) and get an executive summary, "
    "key discussion points, action items, decisions, deadlines, and next steps — "
    "automatically extracted using an LLM."
)

uploaded_file = st.file_uploader("Upload meeting transcript", type=["txt", "pdf"])

col1, col2 = st.columns([1, 1])
with col1:
    run_button = st.button("🚀 Generate Report", type="primary", use_container_width=True)
with col2:
    show_raw = st.checkbox("Show raw transcript after processing")

if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.transcript = None

if run_button:
    if uploaded_file is None:
        st.warning("Please upload a .txt or .pdf transcript first.")
    elif backend == "gemini" and not api_key:
        st.warning("Please enter your Gemini API key in the sidebar (it's free).")
    else:
        try:
            with st.spinner("Reading file..."):
                transcript = load_transcript(uploaded_file)
                st.session_state.transcript = transcript

            with st.spinner("Calling LLM and extracting meeting info... this can take a few seconds"):
                result = summarize_meeting(
                    transcript,
                    backend=backend,
                    api_key=api_key,
                    model_name=model_name,
                )
                st.session_state.result = result

            st.success("Report generated successfully!")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result

    st.header("📋 Executive Summary")
    st.write(result.get("executive_summary", "N/A"))

    st.header("🗣️ Key Discussion Points")
    points = result.get("key_discussion_points", [])
    if points:
        for p in points:
            st.markdown(f"- {p}")
    else:
        st.caption("No discussion points identified.")

    st.header("✅ Action Items")
    actions = result.get("action_items", [])
    if actions:
        st.table(
            [
                {
                    "Task": a.get("task", "N/A"),
                    "Owner": a.get("owner") or "Unassigned",
                    "Deadline": a.get("deadline") or "Not specified",
                }
                for a in actions
            ]
        )
    else:
        st.caption("No action items identified.")

    st.header("📌 Decisions Made")
    decisions = result.get("decisions_made", [])
    if decisions:
        for d in decisions:
            st.markdown(f"- {d}")
    else:
        st.caption("No decisions identified.")

    st.header("⏰ Deadlines")
    deadlines = result.get("deadlines", [])
    if deadlines:
        for d in deadlines:
            st.markdown(f"- **{d.get('item', 'N/A')}**: {d.get('date', 'N/A')}")
    else:
        st.caption("No explicit deadlines identified.")

    st.header("➡️ Next Steps")
    next_steps = result.get("next_steps", [])
    if next_steps:
        for n in next_steps:
            st.markdown(f"- {n}")
    else:
        st.caption("No next steps identified.")

    # -----------------------------------------------------------------
    # Export
    # -----------------------------------------------------------------
    st.markdown("---")
    st.subheader("📥 Export Report")

    md_report = result_to_markdown(result, meeting_title=meeting_title)
    json_report = result_to_json_bytes(result)

    exp1, exp2 = st.columns(2)
    with exp1:
        st.download_button(
            "Download as Markdown (.md)",
            data=md_report,
            file_name="meeting_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with exp2:
        st.download_button(
            "Download as JSON (.json)",
            data=json_report,
            file_name="meeting_report.json",
            mime="application/json",
            use_container_width=True,
        )

    if show_raw and st.session_state.transcript:
        st.markdown("---")
        st.subheader("📄 Raw Transcript")
        st.text_area("Transcript", st.session_state.transcript, height=300)
