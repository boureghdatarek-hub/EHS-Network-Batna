import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(page_title="Hosp-Net Pro | Batna", layout="wide")

# Custom CSS for a professional "Dark Tech" look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #007bff; font-size: 32px; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 8px; height: 3em; }
    .status-card { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def speak_update(text):
    """Text-to-Speech: Makes the app talk to you and Djamel"""
    components.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 3. DASHBOARD HEADER ---
st.title("🏥 Hospital Network Infrastructure")
st.write(f"**Lead Engineers:** Tarek & Djamel")

# --- 4. TOP METRICS (REAL-TIME) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ground Floor", "17/17", "100% DONE")
col2.metric("1st Floor", "3/19", "Cabling Next")
col3.metric("I-POOK Tests", "17/36", "47%")
col4.metric("Active Team", "2", "Online")

st.divider()

# A simple, reliable replacement for Sunday
st.subheader("📢 Digital Command (Talkie-Text)")
msg = st.text_input("Send voice message to Djamel:")

if st.button("Send & Shout"):
    st.success(f"Sent: {msg}")
    # This uses a simple Javascript trick to make the phone talk
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{msg}');
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)
    
    st.subheader("📝 Log New Progress")
    with st.form("progress_form", clear_on_submit=True):
        floor = st.radio("Floor", ["Ground Floor", "1st Floor"], index=1)
        office = st.text_input("Office / Point ID")
        task = st.selectbox("Task Completed", ["Raceway Fixed", "Cable Pulled", "Jack Terminated", "I-POOK Verified"])
        cisco_port = st.number_input("Cisco Switch Port", 1, 48)
        
        if st.form_submit_button("Sync & Shout"):
            update_text = f"Update from Tarek: {office} {task} on port {cisco_port}"
            st.success("Cloud Synchronized!")
            # This triggers the "Talking" part
            speak_update(update_text)

with right_col:
    st.subheader("📊 Deployment Roadmap")
    # This would eventually pull from your Google Sheet or SQL database
    # For now, here is a professional-looking preview
    data = {
        "ID": ["G-16", "G-17", "F1-01", "F1-02", "F1-03"],
        "Office": ["Archive", "New Office", "Accounting", "HR", "Pharmacy"],
        "Status": ["Verified ✅", "Verified ✅", "Raceway 🏗️", "Raceway 🏗️", "Raceway 🏗️"],
        "Cisco Port": [47, 48, 1, 2, 3],
        "VLAN": [10, 10, 20, 20, 20]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- 6. FOOTER REPORTING ---
st.divider()
if st.button("📑 Generate Professional Project Report"):
    st.balloons()
    st.write("Report generated for Hospital Administration.")
