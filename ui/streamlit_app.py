import streamlit as st
import requests
import json
import os

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000") + "/analyze"
st.set_page_config(page_title="Guardrails Gateway", page_icon="🛡️")
st.title("🛡️ SentraGuard Lite")
st.write("Minimal GenAI Guardrails Gateway")

with st.container():
    st.subheader("Test Request")
    prompt_input = st.text_area("Prompt", height=150, placeholder="Enter prompt to test...")
    st.markdown("**Context Documents (Optional)**")
    doc_text = st.text_area("Context Document Text", height=100, placeholder="Simulated RAG content...")
    submit_btn = st.button("Analyze Prompt", type="primary")

if submit_btn:
    if not prompt_input:
        st.warning("Please enter a prompt.")
    else:
        payload = {
            "prompt": prompt_input,
            "context_docs": [{"id": "doc-1", "text": doc_text}] if doc_text else [],
            "metadata": {"source": "streamlit-ui"}
        }
        with st.spinner("Scanning for risks..."):
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    decision = result["decision"]
                    score = result["risk_score"]
                    color = "green" if decision == "allow" else ("red" if decision == "block" else "orange")
                    
                    st.divider()
                    st.subheader("Analysis Result")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Decision", decision.upper(), delta_color="off")
                    col2.metric("Risk Score", f"{score}/100")
                    col3.write(f"**Tags:** {', '.join(result['risk_tags']) if result['risk_tags'] else 'None'}")
                    
                    if decision == "block":
                        st.error(f"Request Blocked! Score: {score}")
                    elif decision == "transform":
                        st.warning(f"Content Modified (PII Redacted)")
                    else:
                        st.success("Content Safe")
                    st.subheader("Output")
                    if result.get("sanitized_prompt"):
                        st.text_area("Sanitized Prompt", value=result["sanitized_prompt"], disabled=True)
                    
                    with st.expander("View Raw JSON Response"):
                        st.json(result)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to API. Make sure it is running on http://localhost:8000")
