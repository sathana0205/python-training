import streamlit as st 
import random 
import time 
 
st.title("Multi-Patient Live Monitoring Dashboard") 
st.write("Simulating live sensor data for multiple patients: Heart Rate, Temperature, Oxygen Level") 
 
# --- List of patients --- 
patients = ["Arun", "Meena", "John", "Priya", "Ravi"] 
 
# --- Generator: Simulate live sensor data per patient --- 
def patient_sensor_stream(patients): 
    while True: 
        data = [] 
        for p in patients: 
            reading = { 
                "name": p, 
                "heart_rate": random.randint(60, 100), 
                "temperature": round(random.uniform(97.0, 100.0), 1), 
                "oxygen_level": random.randint(90, 100) 
            } 
            data.append(reading) 
        yield data 
        time.sleep(1)  # simulate real-time delay 
 
# --- Create placeholders for each patient --- 
patient_placeholders = {} 
for p in patients: 
    patient_placeholders[p] = { 
        "container": st.container(), 
        "hr_bar": None, 
        "temp_bar": None, 
        "ox_bar": None, 
        "hr_text": None, 
        "temp_text": None, 
        "ox_text": None 
    } 
 
# Initialize patient sections 
for p in patients: 
    with patient_placeholders[p]["container"]: 
        st.subheader(f"Patient: {p}") 
        patient_placeholders[p]["hr_bar"] = st.progress(0) 
        patient_placeholders[p]["temp_bar"] = st.progress(0) 
        patient_placeholders[p]["ox_bar"] = st.progress(0) 
        patient_placeholders[p]["hr_text"] = st.empty() 
        patient_placeholders[p]["temp_text"] = st.empty() 
        patient_placeholders[p]["ox_text"] = st.empty() 
 
# --- Run live stream --- 
for readings in patient_sensor_stream(patients): 
    for reading in readings: 
        p = reading["name"] 
        hr = reading["heart_rate"] 
        temp = reading["temperature"] 
        ox = reading["oxygen_level"] 
 
        # Update progress bars 
        patient_placeholders[p]["hr_bar"].progress(min(hr, 100)) 
        patient_placeholders[p]["temp_bar"].progress(int((temp-97)/3*100)) 
        patient_placeholders[p]["ox_bar"].progress(ox) 
 
        # Update text 
        patient_placeholders[p]["hr_text"].text(f"Heart Rate: {hr} bpm") 
        patient_placeholders[p]["temp_text"].text(f"Temperature: {temp} °F") 
        patient_placeholders[p]["ox_text"].text(f"Oxygen Level: {ox}%") 
 
 