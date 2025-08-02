import streamlit as st
import requests

st.set_page_config(page_title="Energy Consumption Prediction", layout="centered")

st.title("⚡ Energy Consumption Prediction")

st.markdown("Enter the environmental conditions to predict energy usage:")

# Input fields
temperature = st.number_input("🌡️ Temperature (°C)", min_value=-50.0, max_value=60.0, value=23.5, step=0.1)
humidity = st.number_input("💧 Humidity (%)", min_value=0, max_value=100, value=55)
wind_speed = st.number_input("💨 Wind Speed (m/s)", min_value=0.0, max_value=50.0, value=3.2, step=0.1)
hour_of_day = st.slider("🕒 Hour of Day (0-23)", min_value=0, max_value=23, value=14)
day_of_week = st.selectbox("📅 Day of Week (0=Mon, ..., 6=Sun)", options=list(range(7)), index=2)

# API endpoint
backend_url = "http://127.0.0.1:8000/predict"  # 🔁 Replace with your actual backend URL

# Submit button
if st.button("🔍 Predict Energy Consumption"):
    payload = {
        "data": [temperature, humidity, wind_speed, hour_of_day, day_of_week]
    }
    try:
        response = requests.post(backend_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, str):
                st.success(result)  # plain string response
            elif isinstance(result, dict) and "prediction" in result:
                st.success(f"🔋 Predicted Energy Consumption: {result['prediction']} kWh")
            else:
                st.error(f"⚠️ Unexpected response format: {result}")
        else:
            st.error(f"❌ Backend error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")


