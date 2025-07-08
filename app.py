# main.py
# To run this app, save it as main.py and run `streamlit run main.py` in your terminal.
# You will need to have streamlit installed: `pip install streamlit`

import streamlit as st
import json
import asyncio
import httpx

# --- Page Configuration ---
st.set_page_config(
    page_title="Prompt Fixer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* General Styling */
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f0f2f5;
    }
    .main-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease;
    }
    .main-container:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .stTextArea textarea {
        border: 2px solid #d1d5db;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        outline: none;
    }
    .stButton button {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: transform 0.2s ease, background 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        transform: translateY(-2px);
    }
    .score-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin: 0 auto 10px;
        transition: transform 0.3s ease;
    }
    .score-circle:hover {
        transform: scale(1.1);
    }
    .score-1, .score-2, .score-3 { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .score-4, .score-5 { background: linear-gradient(135deg, #f59e0b, #d97706); }
    .score-6, .score-7 { background: linear-gradient(135deg, #eab308, #ca8a04); }
    .score-8, .score-9, .score-10 { background: linear-gradient(135deg, #22c55e, #16a34a); }
    .stExpander {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background-color: #ffffff;
        padding: 10px;
    }
    .stContainer {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 15px;
        background-color: #ffffff;
    }
    .stSidebar {
        background-color: #f9fafb;
    }
    .stSidebar .stButton button {
        width: 100%;
        text-align: left;
        background: #ffffff;
        color: #1f2937;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        margin-bottom: 8px;
        padding: 10px;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .stSidebar .stButton button:hover {
        background: #e5e7eb;
        border-color: #3b82f6;
        color: #3b82f6;
    }
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 600;
    }
    .stMarkdown p {
        color: #4b5563;
        line-height: 1.6;
        font-size: 15px;
    }
    .stSpinner {
        color: #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Gemini API Call ---
# NOTE: In a real-world scenario, the API key should be handled securely,
# for example, using Streamlit secrets. For this example, we assume it's available.
# The user of this app would need to provide their own key.
API_KEY = "AIzaSyBwKoYf38-txwsmYZPVHjd21_LbQhzC5aQ" # IMPORTANT: Leave this empty. Canvas will handle the key.
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

async def get_prompt_analysis(user_prompt: str):
    """
    Calls the Gemini API to analyze the user's prompt.
    The meta-prompt instructs the model to act as a prompt engineering assistant
    and return a structured JSON response.
    """
    meta_prompt = f"""
    You are a world-class Prompt Engineering Assistant. Your task is to analyze and improve prompts written for large language models.

    When given a prompt by the user, follow these steps meticulously and return the output as a single, well-formed JSON object. Do not include any text or markdown formatting before or after the JSON object.

    The user's prompt to analyze is:
    ---
    {user_prompt}
    ---

    Here are your analysis steps:
    1.  **Identify Flaws**: Critically examine the prompt for issues like vagueness, ambiguity, multiple intents, unclear instructions, lack of context, or missing constraints. If the prompt is strong, acknowledge that.
    2.  **Explain Problems**: Clearly and concisely explain the identified problems. If the prompt is good, explain what makes it effective.
    3.  **Suggest an Improved Version**: Rewrite the prompt to be more effective, clear, and specific. This version should directly address the flaws you identified.
    4.  **Generate Variants**: Create two distinct alternative versions of the improved prompt. Each variant should have a different tone or style (e.g., "Formal & Technical", "Friendly & Casual", "Direct & Imperative", "Creative & Evocative").
    5.  **Assign Quality Score**: Rate the original prompt on a scale of 1 to 10, where 1 is extremely poor and 10 is perfect.
    6.  **Justify Score**: Provide a brief but clear justification for the score you assigned.
    7.  **Provide a Tip**: Offer one actionable, context-specific tip that the user can learn from this example to improve their future prompting skills.

    **JSON Output Structure:**
    Please structure your response as a JSON object with the following keys:
    {{
      "identifiedFlaws": [
        Genix AI
        "Flaw 1 description",
        "Flaw 2 description"
      ],
      "problemExplanation": "A clear explanation of the issues or strengths.",
      "improvedPrompt": "The rewritten, superior prompt.",
      "promptVariants": [
        {{
          "title": "Variant 1 Title (e.g., Formal Tone)",
          "prompt": "The first prompt variant."
        }},
        {{
          "title": "Variant 2 Title (e.g., Casual Tone)",
          "prompt": "The second prompt variant."
        }}
      ],
      "qualityScore": <integer_between_1_and_10>,
      "scoreJustification": "The justification for the quality score.",
      "promptingTip": "A single, helpful prompting tip."
    }}

    If the original prompt is already excellent, state this in the 'problemExplanation', reflect it in the high score, and make the 'improvedPrompt' the same as the original.
    """

    payload = {
        "contents": [{"parts": [{"text": meta_prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(API_URL, json=payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            # The response from the API is expected to be a JSON string.
            # We extract the text part which contains this string.
            api_response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            return json.loads(api_response_text)
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        st.error(f"Failed to parse the API response. Error: {e}")
        st.info("Raw response received:", api_response_text)
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None


# --- Streamlit UI ---
st.title("🤖 Prompt Fixer - Your Prompt Engineering Assistant")
st.markdown("Analyze and improve your LLM prompts. Enter your prompt below to get a detailed analysis, an improved version, and actionable tips.")

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []

with st.container(border=True):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Use a form to group the text area and button
    with st.form(key='prompt_form'):
        user_prompt = st.text_area(
            "**Enter your prompt here:**",
            height=150,
            placeholder="e.g., 'Write about cars.'",
            key="prompt_input"
        )
        submit_button = st.form_submit_button(label="Analyze Prompt")

    if submit_button and user_prompt:
        with st.spinner("🔍 Analyzing your prompt... This may take a moment."):
            analysis_result = asyncio.run(get_prompt_analysis(user_prompt))
            if analysis_result:
                st.session_state.analysis_result = analysis_result
                # Add to history if it's a new prompt
                if user_prompt not in st.session_state.prompt_history:
                    st.session_state.prompt_history.insert(0, user_prompt)
            else:
                st.session_state.analysis_result = None # Clear previous results on error

    st.markdown('</div>', unsafe_allow_html=True)


# --- Display Results ---
if st.session_state.analysis_result:
    res = st.session_state.analysis_result
    st.markdown("---")
    st.header("Analysis Results")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Quality Score")
        score = res.get('qualityScore', 0)
        st.markdown(f'<div class="score-circle score-{score}">{score}/10</div>', unsafe_allow_html=True)
        with st.expander("**Score Justification**", expanded=True):
            st.write(res.get('scoreJustification', "No justification provided."))

    with col2:
        st.subheader("Identified Flaws")
        flaws = res.get('identifiedFlaws', [])
        if flaws:
            for flaw in flaws:
                st.warning(f"**{flaw}**")
        else:
            st.success("✅ No significant flaws were identified. This is a strong prompt!")

        st.markdown("**Explanation:**")
        st.write(res.get('problemExplanation', "No explanation provided."))

    st.subheader("✨ Improved Prompt")
    st.success(res.get('improvedPrompt', "No improved prompt provided."))

    st.subheader("🎭 Prompt Variants")
    variants = res.get('promptVariants', [])
    if len(variants) == 2:
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            with st.container(border=True):
                st.markdown(f"**{variants[0].get('title', 'Variant 1')}**")
                st.write(variants[0].get('prompt', ''))
        with v_col2:
            with st.container(border=True):
                st.markdown(f"**{variants[1].get('title', 'Variant 2')}**")
                st.write(variants[1].get('prompt', ''))
    else:
        st.write("Could not generate prompt variants.")

    st.subheader("💡 Pro Tip")
    st.info(res.get('promptingTip', "No tip provided."))

# --- History Sidebar ---
with st.sidebar:
    st.title("📜 Prompt History")
    st.write("Click to re-analyze a previous prompt.")
    if st.session_state.prompt_history:
        for i, old_prompt in enumerate(st.session_state.prompt_history):
            if st.button(old_prompt, key=f"history_{i}"):
                st.session_state.prompt_input = old_prompt
                st.rerun()
    else:
        st.write("No prompts analyzed yet.")
