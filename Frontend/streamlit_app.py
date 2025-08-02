import streamlit as st
import requests

# Page config
st.set_page_config(page_title="⚡️ Energy Consumption Predictor", layout="wide")
backend_url = "https://energy-consuption-prediction-using.onrender.com/predict"

# Sidebar / Menu
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3381/3381681.png", width=100)
    st.markdown("### ⚙️ Settings")

    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #00d4ff;'>⚡️ Smart Energy Consumption Prediction</h1>",
    unsafe_allow_html=True
)
st.markdown("### Enter the input parameters below 👇")

# Inputs layout
col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=-10.0, max_value=50.0, value=23.5)

with col2:
    humidity = st.number_input("💧 Humidity (%)", min_value=0, max_value=100, value=55)

with col3:
    wind_speed = st.number_input("💨 Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=3.2)

col4, col5 = st.columns(2)

with col4:
    hour_of_day = st.slider("🕒 Hour of Day", min_value=0, max_value=23, value=14)

with col5:
    day_of_week = st.selectbox("📅 Day of Week", options=[
        ("0", "Monday"), ("1", "Tuesday"), ("2", "Wednesday"),
        ("3", "Thursday"), ("4", "Friday"), ("5", "Saturday"), ("6", "Sunday")
    ], index=2, format_func=lambda x: x[1])

# Predict button
if st.button("🔍 Predict Energy Consumption"):
    payload = {
        "data": [
            temperature,
            humidity,
            wind_speed,
            hour_of_day,
            int(day_of_week[0])  # Convert to int
        ]
    }

    try:
        response = requests.post(backend_url, json=payload)
        if response.status_code == 200:
            result = response.json()

            # Response could be string or dict
            if isinstance(result, str):
                st.success(result)
            elif isinstance(result, dict) and "prediction" in result:
                pred = result['prediction']
                st.markdown(
                    f"""
                    <div style="background-color: #e0f7fa; padding: 20px; border-radius: 10px; text-align: center;">
                        <h2 style="color: #00796b;">🔋 Predicted Energy Consumption</h2>
                        <h1 style="color: #00695c;">{pred:.2f} kWh</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("⚠️ Unexpected response format")
        else:
            st.error(f"❌ Backend error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")

# Footer
st.markdown("---")
st.markdown("<center>© 2025 | Made by Ramesh 🌟 | #EnergyAI #Streamlit #DeepLearning</center>", unsafe_allow_html=True)
