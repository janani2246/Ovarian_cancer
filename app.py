import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr

st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")

st.title("🧬 Ovarian Cancer Detection & Care System")

# ================= BACKGROUND =================
def set_bg(color):
    st.markdown(f"""
    <style>
    .stApp {{
        background: {color};
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar Role
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ============================
# 👩 PATIENT
# ============================
if role == "Patient":

    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")  # Pink
    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    # ================= OPTION 1 =================
    if option == "Predict Risk":
        st.header("👩 Patient Assessment")

        # Age
        age = st.number_input("Enter Age", 10, 100)

        # Family History
        family_history = st.radio("Family History", ["Yes", "No"])
        family_value = 1 if family_history == "Yes" else 0

        # ----------------------------
        # Age-based Logic
        # ----------------------------
        if age < 50:
            st.subheader("🩸 Menstrual Details")
            menstrual_status = st.selectbox(
                "Menstrual Flow",
                ["Regular", "Irregular", "Heavy", "Absent"]
            )
            menstrual_value = {"Regular":0, "Irregular":1, "Heavy":2, "Absent":3}[menstrual_status]
            menopause_value = 0
        else:
            st.subheader("🌸 Menopause Details")
            menopause = st.selectbox(
                "Menopause Status",
                ["Yes", "No", "Unsure"]
            )
            menopause_value = {"Yes":1, "No":0, "Unsure":2}[menopause]
            menstrual_value = 0

        # ----------------------------
        # Symptoms (Checkbox)
        # ----------------------------
        st.subheader("Select Symptoms (Optional)")
        symptom_list = ["Pelvic Pain", "Stomach Swelling", "Bloating", "Fatigue",
                        "Back Pain", "Feeling Full Quickly", "Urinary Urgency",
                        "Weight Loss", "Vaginal Bleeding"]
        symptoms = {symptom: st.checkbox(symptom) for symptom in symptom_list}

        # ----------------------------
        # 🎤 Voice Input (Optional)
        # ----------------------------
        st.subheader("🎤 Voice Input (Optional)")

        audio = st.audio_input("Speak your symptoms (Tamil / English)")
        if audio:
            st.audio(audio)

            # Convert to WAV
            audio_bytes = audio.getvalue()
            sound = AudioSegment.from_file(BytesIO(audio_bytes))
            sound = sound.set_channels(1).set_frame_rate(16000)
            sound.export("temp.wav", format="wav")

            # Speech Recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="en-IN")  # English/Indian accents
                    st.success("Voice recognized successfully!")
                    st.write("🗣 You said:", text)

                    # Auto-check symptoms from voice
                    for symptom in symptom_list:
                        if symptom.lower() in text.lower():
                            symptoms[symptom] = True

                except sr.UnknownValueError:
                    st.error("Could not understand the audio")
                except sr.RequestError as e:
                    st.error(f"API error: {e}")

        # ----------------------------
        # Prediction
        # ----------------------------
        if st.button("🔍 Predict Risk"):
            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value

            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 4:
                risk = "🔴 High Risk"
            elif risk_score >= 2:
                risk = "🟠 Medium Risk"
            else:
                risk = "🟢 Low Risk"

            st.subheader("Prediction Result")
            st.success(f"Risk Level: {risk}")
            st.write(f"Score: {risk_score}/12")

            if "High" in risk:
                st.error("⚠️ Immediate doctor consultation required")
            elif "Medium" in risk:
                st.warning("⚠️ Regular checkup needed")
            else:
                st.success("✅ You are healthy")

    # ================= OPTION 2 =================
    else:
        st.header("🧾 Cancer Confirmed Care Plan")

        name = st.text_input("Patient Name")
        age = st.number_input("Age", 10, 100)
        phone = st.text_input("Phone Number")
        risk = st.selectbox("Risk Level", ["High", "Medium"])

        if st.button("Generate Care Plan"):
            st.success(f"Care Plan for {name}")
            st.subheader("📅 Daily Timetable")
            st.write("""
            - 🏃 7–8 AM → Exercise  
            - 🍽 9–10 AM → Breakfast + Medicine  
            - 🍛 1–2 PM → Lunch + Medicine  
            - 🍽 7–8 PM → Dinner + Medicine  
            - 💧 Drink water regularly  
            """)
            st.subheader("🥗 Diet Plan")
            st.write("""
            - Eat fruits & vegetables  
            - Avoid junk & oily food  
            - Balanced diet  
            """)
            st.subheader("🔔 Alerts (Simulation)")
            st.info("Reminder: Breakfast at 9 AM")
            st.info("Reminder: Lunch at 1 PM")
            st.info("Reminder: Dinner at 7 PM")

# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")  # Blue
    st.header("👨‍⚕️ Doctor Dashboard")

    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("Patient Info")
    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Patient Phone")
    last_visit = st.date_input("Last Visit")

    medicines = st.text_area("Medicines Prescribed")

    notes = st.text_area("Consultation Notes", value="""
Patient shows symptoms indicating possible ovarian cancer.
Further tests like CA-125 and ultrasound are recommended.
Treatment will be decided based on reports.
Follow healthy diet and medication.
Next follow-up in 2 weeks.
""")

    if st.button("Save Consultation"):
        st.session_state["patient"] = {
            "name": patient_name,
            "meds": medicines,
            "notes": notes
        }
        st.success("✅ Saved Successfully")

    if "patient" in st.session_state:
        st.subheader("📁 Saved Record")
        st.write(st.session_state["patient"])

    st.subheader("🤖 AI Follow-up")

    if st.button("Generate Follow-up"):
        st.write("### 📋 Plan")
        st.write("""
        - Morning: Medicine + Light Exercise  
        - Afternoon: Balanced Lunch + Medicine  
        - Evening: Light walk  
        - Night: Dinner + Medicine  
        """)
        st.info("Follow doctor instructions strictly")
