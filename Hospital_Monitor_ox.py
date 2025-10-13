import streamlit as st
import random
import time

st.title("HOSPITAL SENSOR LIVE MONITORING")

st.write("Simulation live sensor data: Heart_Rate, Temperature, Oxygen_level")

#generator: simulate live sensor data
def sensor_data_stream():
    yield {
        "heart_rate": random.randint(60, 100),
        "temperature": round(random.uniform(97.0, 100.0), 1),
        "oxygen_level": random.randint(90, 100)
        }
    time.sleep(1) #simulate real time delay

# streamlit ui placeholder
heart_rate_bar = st.progress(0)
temperature_bar = st.progress(0)
oxygen_level_bar = st.progress(0)

heart_rate_text = st.empty()
temperature_text = st.empty()
oxygen_level_text = st.empty()

for reading in sensor_data_stream():
    hr = reading["heart_rate"]
    temp= reading["temperature"]
    ox = reading["oxygen_level"]

    # update progress bars(scale %)
    heart_rate_bar.progress(min(hr,100))
    temperature_bar.progress(int((temp-97)/3*100)) # temperature 97-100 scale
    oxygen_level_bar.progress(ox) # oxygen level %

    # Update text display
    heart_rate_text.text(f"Heart Rate:  {hr} bpm")
    print(f" Heart Rate :  {hr} bpm")
    temperature_text.text(f" Temperature : {temp } F")
    print(f"Temperature : {temp} F")
    oxygen_level_text.text(f"Oxygen_Level : {ox} %")
    print(f"Oxygen Level : {ox} %")