import streamlit as st
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import os

#cache setup

st.set_page_config(
    page_title = "PitWall",
    page_icon = "🏎️",
    layout = "wide"
)

# Cache setup
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')

# Title
st.title("🏎️ PitWall")
st.subheader("F1 Driver Performance Analysis Dashboard")
st.markdown("---")

# Load session
@st.cache_data
def load_session():
    session = fastf1.get_session(2024, 'Bahrain', 'R')
    session.load()
    return session

with st.spinner("Loading 2024 Bahrain GP data..."):
    session = load_session()

st.success("Data loaded successfully! ✅")
st.write("Event:", session.event['EventName'])
st.write("Date:", str(session.event['EventDate']))
st.markdown("---")
st.header("📊 Analysis 1 — Lap Time Comparison")

# Driver selection
all_drivers = list(session.laps['Driver'].unique())
selected_drivers = st.multiselect(
    "Select drivers to compare:",
    options=all_drivers,
    default=['VER', 'PER', 'SAI']
)

if selected_drivers:
    fig, ax = plt.subplots(figsize=(12, 5))
    for driver in selected_drivers:
        driver_laps = session.laps.pick_drivers(driver)
        lap_numbers = driver_laps['LapNumber']
        lap_times = driver_laps['LapTime'].dt.total_seconds()
        ax.plot(lap_numbers, lap_times, marker='o', markersize=3, label=driver)
    
    ax.set_title('Lap Time Comparison - 2024 Bahrain GP')
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time (seconds)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("Please select at least one driver!")