import streamlit as st
import time
from datetime import datetime
import pandas as pd
import os

# --- Setup ---
os.makedirs("logs", exist_ok=True)
st.set_page_config(page_title="AHT Counter Dashboard", layout="wide", page_icon="⏱️")

# --- Custom CSS for Better UI ---
st.markdown("""
    <style>
    body {
        background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
        background-size: cover;
        background-color: #1e1e2f;
        color: #ffffff;
    }
    .main {
        background: linear-gradient(to right, #1f4037, #99f2c8);
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    .main h1 {
        color: #ffffff;
        text-shadow: 0 0 10px #00e6e6, 0 0 20px #00e6e6;
        font-size: 2.5em;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        from {
            text-shadow: 0 0 5px #00e6e6, 0 0 10px #00e6e6;
        }
        to {
            text-shadow: 0 0 20px #00e6e6, 0 0 30px #00e6e6;
        }
    }
    .stButton>button {
        background-color: #00b894;
        color: white;
        font-size: 16px;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.4s ease;
        box-shadow: 0 0 10px #00b894;
    }
    .stButton>button:hover {
        background-color: #00cec9;
        transform: scale(1.08);
        box-shadow: 0 0 20px #00cec9;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    h2, h3, h4 {
        color: #ffffff;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main">
    <h1>⏱️ AHT Counter & Time Saver Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "manual_start" not in st.session_state:
    st.session_state.manual_start = None
if "manual_end" not in st.session_state:
    st.session_state.manual_end = None
if "auto_start" not in st.session_state:
    st.session_state.auto_start = None
if "auto_end" not in st.session_state:
    st.session_state.auto_end = None

# --- Timer Logic ---
def calculate_duration(start, end):
    if start and end:
        return round(end - start, 2)
    return None

# --- Tabs Layout ---
tab1, tab2 = st.tabs(["⏱️ Timer Dashboard", "📜 History"])

with tab1:
    col1, col2 = st.columns(2)

    # --- Manual Method ---
    with col1:
        st.subheader("🧍 Manual Task Timer")
        if st.button("▶️ Start/Stop Manual Timer"):
            if st.session_state.manual_start is None:
                st.session_state.manual_start = time.time()
                st.success("Manual Timer Started!")
            else:
                st.session_state.manual_end = time.time()
                st.success("Manual Timer Stopped!")

        manual_time = calculate_duration(st.session_state.manual_start, st.session_state.manual_end)
        if manual_time:
            st.info(f"Manual Task Time: **{manual_time} seconds**")

    # --- Automated Method ---
    with col2:
        st.subheader("🤖 Automated Task Timer")
        if st.button("▶️ Start/Stop Automated Timer"):
            if st.session_state.auto_start is None:
                st.session_state.auto_start = time.time()
                st.success("Automated Timer Started!")
            else:
                st.session_state.auto_end = time.time()
                st.success("Automated Timer Stopped!")

        auto_time = calculate_duration(st.session_state.auto_start, st.session_state.auto_end)
        if auto_time:
            st.info(f"Automated Task Time: **{auto_time} seconds**")

    # --- Insights ---
    if manual_time and auto_time:
        st.markdown("---")
        st.subheader("📈 Insights")

        time_saved = manual_time - auto_time
        efficiency = round((time_saved / manual_time) * 100, 2)
        team_daily_saving = time_saved * 10
        monthly_saving = team_daily_saving * 22

        st.success(f"✅ Time Saved per task: **{round(time_saved, 2)} seconds**")
        st.success(f"📊 Efficiency Gain: **{efficiency}%**")
        st.info(f"👥 Daily Team Saving (10 people): **{round(team_daily_saving / 60, 2)} minutes**")
        st.info(f"📅 Monthly Time Saving: **{round(monthly_saving / 3600, 2)} hours**")

        # Bar chart
        df_chart = pd.DataFrame({"Method": ["Manual", "Automated"], "Time (sec)": [manual_time, auto_time]})
        st.bar_chart(df_chart.set_index("Method"))

        # Save log (append to existing or create new)
        file_path = "logs/aht_log_summary.csv"
        log_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Manual Time (sec)": manual_time,
            "Automated Time (sec)": auto_time,
            "Time Saved": time_saved,
            "Efficiency (%)": efficiency
        }

        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, pd.DataFrame([log_data])], ignore_index=True)
        else:
            updated_df = pd.DataFrame([log_data])

        updated_df.to_csv(file_path, index=False)

        st.download_button("📥 Download Result Log", updated_df.to_csv(index=False), "aht_summary.csv", "text/csv")

with tab2:
    st.subheader("📜 Task History & Trends")
    history_path = "logs/aht_log_summary.csv"
    if os.path.exists(history_path):
        df = pd.read_csv(history_path)
        st.dataframe(df.tail(20))

        st.line_chart(df.set_index("Timestamp")["Time Saved"])
        st.line_chart(df.set_index("Timestamp")["Efficiency (%)"])
    else:
        st.warning("No history found. Complete one full run to start tracking!")
