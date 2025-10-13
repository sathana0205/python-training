import streamlit as st 
import random 
import time 
 
st.set_page_config(page_title="ICU Live Monitoring Dashboard", 
layout="wide") 
st.title("ICU Live Monitoring Dashboard") 
st.write("Monitoring multiple patients in real-time with alerts for abnormal vitals") 
 
# --- Patients list --- 
patients = ["Arun", "Meena", "John", "Priya", "Ravi"] 
 
# --- Normal ranges for vitals --- 
NORMAL_RANGES = { 
    "heart_rate": (60, 100),     # bpm 
    "temperature": (97.0, 99.5), # °F 
    "oxygen_level": (95, 100)    # % 
} 
 
# --- Generator to simulate live sensor data --- 
def patient_sensor_stream(patients): 
    while True: 
        data = [] 
        for p in patients: 
            reading = { 
                "name": p, 
                "heart_rate": random.randint(50, 110), 
                "temperature": round(random.uniform(96.0, 101.0), 1), 
                "oxygen_level": random.randint(88, 100) 
            } 
            data.append(reading) 
        yield data 
        time.sleep(1) 
 
# --- Create placeholders for each patient --- 
patient_placeholders = {} 
for p in patients: 
    with st.container(): 
        st.subheader(f"Patient: {p}") 
        hr_bar = st.progress(0, text="Heart Rate") 
        temp_bar = st.progress(0, text="Temperature") 
        ox_bar = st.progress(0, text="Oxygen Level") 
        hr_text = st.empty() 
        temp_text = st.empty() 
        ox_text = st.empty() 
        alert = st.empty() 
        st.divider() 
 
        patient_placeholders[p] = { 
            "hr_bar": hr_bar, 
            "temp_bar": temp_bar, 
            "ox_bar": ox_bar, 
            "hr_text": hr_text, 
            "temp_text": temp_text, 
            "ox_text": ox_text, 
            "alert": alert 
        } 
 
# --- Helper function: clamp between 0–100 --- 
def clamp(value): 
    return max(0, min(100, int(value))) 
 
# --- Run live updates --- 
for readings in patient_sensor_stream(patients): 
    for reading in readings: 
        p = reading["name"] 
        hr = reading["heart_rate"] 
        temp = reading["temperature"] 
        ox = reading["oxygen_level"] 
 
        # --- Normalize bar values to 0–100 range --- 
        hr_bar_value = clamp(hr) 
        temp_bar_value = clamp((temp - 95) * 25)   # roughly scale 9599.5°F to 0–100 
        ox_bar_value = clamp(ox) 
 
        # --- Update progress bars --- 
        patient_placeholders[p]["hr_bar"].progress(hr_bar_value, 
text=f"Heart Rate: {hr} bpm") 
        patient_placeholders[p]["temp_bar"].progress(temp_bar_value, 
text=f"Temperature: {temp} °F") 
        patient_placeholders[p]["ox_bar"].progress(ox_bar_value, 
text=f"Oxygen Level: {ox}%") 
 
        # --- Update numeric display --- 
        patient_placeholders[p]["hr_text"].text(f"Heart Rate: {hr} bpm") 
        patient_placeholders[p]["temp_text"].text(f"Temperature: {temp} °F") 
        patient_placeholders[p]["ox_text"].text(f"Oxygen Level: {ox}%") 
 
        # --- Alerts --- 
        alerts = [] 
        if hr < NORMAL_RANGES["heart_rate"][0] or hr >  NORMAL_RANGES["heart_rate"][1]: 
            alerts.append(f"Heart Rate abnormal: {hr} bpm") 
        if temp < NORMAL_RANGES["temperature"][0] or temp > NORMAL_RANGES["temperature"][1]: 
            alerts.append(f"Temperature abnormal: {temp} °F") 
        if ox < NORMAL_RANGES["oxygen_level"][0]: 
            alerts.append(f"Oxygen Level low: {ox}%") 
 
        if alerts: 
            patient_placeholders[p]["alert"].warning("\n".join(alerts)) 
        else: 
            patient_placeholders[p]["alert"].success("All vitals normal") 
 
    # small delay before next update 
    time.sleep(1) 
 