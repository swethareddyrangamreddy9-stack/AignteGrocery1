import streamlit as st
import time
from google import genai
from google.genai import types

# ==========================================
# 1. SETUP (MUST BE FIRST)
# ==========================================
st.set_page_config(page_title="Project 49: Grocery Bot", layout="wide")

# ==========================================
# 2. HARDCODED Q&A DATA (For the Presentation)
# ==========================================
FAQ_DATA = {
    "Explain grocery order fulfillment": 
        "Fulfillment begins when you click 'Order'. A 'Picker' in a Dark Store receives a digital list. "
        "They use a route-optimized app to select items. Perishables are picked last to maintain freshness.",
    
    "What happens after order placement?": 
        "1. Picking: Items selected. 2. Quality Check: Freshness verified. "
        "3. Packing: Food and chemicals separated. 4. Dispatch: Rider assigned via AI.",
    
    "Explain last-mile delivery process": 
        "This is the final journey from the store to your door. Our AI calculates the fastest route "
        "considering traffic and weather to ensure your groceries arrive in under 20 minutes.",
    
    "Why do delivery delays occur?": 
        "Common reasons include: 1. High demand periods. 2. Traffic congestion. "
        "3. Weather conditions. 4. Item stock-outs requiring a substitute search."
}

# ==========================================
# 3. SIDEBAR & SETTINGS
# ==========================================
with st.sidebar:
    st.title("⚙️ Project 49 Admin")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.success("Project: Grocery Logistics")
    st.info("Model: Gemini 2.5 Flash")

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.title("🚛 Grocery Delivery Process Explainer")
st.markdown("### 💡 Click to see how it works (Instant Answers)")

# Display 4 Hardcoded Buttons
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

selected_q = None
with col1:
    if st.button("📦 Order Fulfillment"): selected_q = "Explain grocery order fulfillment"
with col2:
    if st.button("🕒 After Placement"): selected_q = "What happens after order placement?"
with col3:
    if st.button("🛵 Last-Mile Process"): selected_q = "Explain last-mile delivery process"
with col4:
    if st.button("⚠️ Why the Delays?"): selected_q = "Why do delivery delays occur?"

st.markdown("---")

# ==========================================
# 5. CHAT LOGIC (API + HARDCODED)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Trigger Chat (From Input or Buttons)
user_input = st.chat_input("Ask a custom question...")
prompt = user_input or selected_q

if prompt:
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        # 2. CHECK IF IT IS A HARDCODED QUESTION
        if prompt in FAQ_DATA:
            answer = FAQ_DATA[prompt]
            # Simulate typing
            full_txt = ""
            for word in answer.split():
                full_txt += word + " "
                time.sleep(0.05)
                placeholder.markdown(full_txt + "▌")
            placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # 3. IF NOT HARDCODED, USE THE AI
        else:
            if not api_key:
                st.error("Please enter an API key for custom questions!")
            else:
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Explain this grocery logistics topic: {prompt}. Be concise."
                    )
                    placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"API Error: {e}")