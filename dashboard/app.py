import pandas as pd
import streamlit as st
import os
from datetime import datetime

st.set_page_config(layout="wide", page_title="Real-time Weather Analysis Dashboard ☀️", page_icon="⛅")

# 🌸 Custom CSS for cuteness & animation
st.markdown("""
    <style>
    @keyframes fadeIn {
        0% {opacity: 0; transform: translateY(20px);}
        100% {opacity: 1; transform: translateY(0);}
    }

    .title {
        font-size: 3em;
        color: #2c3e50;
        text-align: center;
        font-weight: bold;
        animation: fadeIn 3s ease-in-out;
    }

    .subtitle {
        text-align: center;
        font-size: 1.3em;
        color: #7f8c8d;
        margin-bottom: 30px;
        animation: fadeIn 5s ease-in-out; 
    }

    .metric-container {
        background: #2c4063;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        animation: fadeIn 5s ease-in-out; 
    }

    .other-city {
        font-size: 16px;
        padding: 8px;
        margin-bottom: 6px;
        background-color: #543232;
        border-radius: 8px;
        animation: fadeIn 5s ease-in-out; 
    }

    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.9em;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 🗓️ Show date
today = datetime.now()
date_str = today.strftime("%A, %d %B %Y")

st.markdown(f"<div class='title'>🌍 Real-Time Weather Dashboard</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{date_str}</div>", unsafe_allow_html=True)

# 📁 Weather file location
file_path = "/data/weather_data.csv"

if not os.path.exists(file_path):
    st.info("Waiting for data... Please make sure producer and consumer are running.")
else:
    df = pd.read_csv(file_path)
    if df.empty:
        st.warning("Data file is empty.")
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        cities = df['city'].unique().tolist()
        selected_city = st.selectbox("🏙️ Select a City", cities)

        main, side = st.columns([3, 1])

        with main:
            filtered = df[df['city'] == selected_city].sort_values('timestamp', ascending=False)
            latest = filtered.iloc[0]

            st.markdown(f"### ☁️ Current Weather in **{selected_city}**", unsafe_allow_html=True)

            with st.container():
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown("<div class='metric-container'>🌡️ Temp", unsafe_allow_html=True)
                    st.metric(label="", value=f"{latest['temp']} °C")

                with col2:
                    st.markdown("<div class='metric-container'>💧 Humidity", unsafe_allow_html=True)
                    st.metric(label="", value=f"{latest['humidity']} %")

                with col3:
                    st.markdown("<div class='metric-container'>💨 Wind", unsafe_allow_html=True)
                    st.metric(label="", value=f"{latest['wind']} m/s")

                with col4:
                    st.markdown("<div class='metric-container'>📉 Pressure", unsafe_allow_html=True)
                    st.metric(label="", value=f"{latest['pressure']} hPa")

            st.markdown("### 📈 Temperature Trend Over Time")
            chart_data = filtered[['timestamp', 'temp']].set_index('timestamp')
            st.line_chart(chart_data)

        with side:
            st.markdown("### 🌎 Other Cities Temps")
            for city in cities:
                if city != selected_city:
                    latest_other = df[df['city'] == city].sort_values('timestamp', ascending=False).iloc[0]
                    st.markdown(f"<div class='other-city'>🏙️ {city}: {latest_other['temp']} °C</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div class='footer'>Made by Museerah, Saad, Anas, and Hamdaan ❤️</div>", unsafe_allow_html=True)
