import streamlit as st
import pandas as pd
import numpy as np
import speech_recognition as sr   # ✅ ADDED

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

# ================= VOICE FUNCTION =================
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak your symptoms (Tamil / English)...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            return text.lower()
        except:
            st.error("❌ Could not understand")
            return ""

# Sidebar Role
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ============================
# 👩 PATIENT
# ============================
if role == "Patient":

    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")

    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    if option == "Predict Risk":
        st.header("👩 Patient Assessment")

        age = st.number_input("Enter Age", 10, 100)

        family_history = st.radio("Family History", ["Yes", "No"])
        family_value = 1 if family_history == "Yes" else 0

        # -------- AGE LOGIC --------
        if age < 50:
            st.subheader("🩸 Menstrual Details")

            menstrual_status = st.selectbox(
                "Menstrual Flow",
                ["Regular", "Irregular", "Heavy", "Absent"]
            )

            if menstrual_status == "Regular":
                menstrual_value = 0
            elif menstrual_status == "Irregular":
                menstrual_value = 1
            elif menstrual_status == "Heavy":
                menstrual_value = 2
            else:
                menstrual_value = 3

            menopause_value = 0

        else:
            st.subheader("🌸 Menopause Details")

            menopause = st.selectbox(
                "Menopause Status",
                ["Yes", "No", "Unsure"]
            )

            if menopause == "Yes":
                menopause_value = 1
            elif menopause == "No":
                menopause_value = 0
            else:
                menopause_value = 2

            menstrual_value = 0

        # -------- SYMPTOMS --------
        st.subheader("Select Symptoms")

        symptoms = {
            "Pelvic Pain": st.checkbox("Pelvic Pain"),
            "Stomach Swelling": st.checkbox("Stomach Swelling"),
            "Bloating": st.checkbox("Persistent Bloating"),
            "Fatigue": st.checkbox("Fatigue"),
            "Back Pain": st.checkbox("Back Pain"),
            "Feeling_Full_Quickly": st.checkbox("Feeling Full Quickly"),
            "Urinary_Urgency": st.checkbox("Urinary Urgency"),
            "Weight_Loss": st.checkbox("Weight Loss"),
            "Vaginal_Bleeding": st.checkbox("Vaginal Bleeding"),
        }

        # 🎤 VOICE ASSISTANT (ADDED)
        st.subheader("🎤 Voice Assistant (Optional)")

        if st.button("Speak Symptoms"):
            voice_text = get_voice_input()

            st.write("📝 Detected Text:", voice_text)

            detected = []

            # English
            if "pain" in voice_text:
                detected.append("Pelvic Pain")
            if "bloating" in voice_text:
                detected.append("Bloating")
            if "fatigue" in voice_text:
                detected.append("Fatigue")
            if "back" in voice_text:
                detected.append("Back Pain")
            if "weight" in voice_text:
                detected.append("Weight Loss")
            if "bleeding" in voice_text:
                detected.append("Vaginal Bleeding")

            # Tamil
            if "வலி" in voice_text:
                detected.append("Pelvic Pain")
            if "வயிறு" in voice_text:
                detected.append("Stomach Swelling")
            if "சோர்வு" in voice_text:
                detected.append("Fatigue")
            if "முதுகு" in voice_text:
                detected.append("Back Pain")
            if "இரத்தம்" in voice_text:
                detected.append("Vaginal Bleeding")

            if detected:
                st.success("Detected Symptoms: " + ", ".join(detected))
            else:
                st.warning("No symptoms detected")

        # -------- PREDICTION --------
        if st.button("🔍 Predict Risk"):

            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value

            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 3:
                risk = "🔴 High Risk"
            elif risk_score >= 2:
                risk = "🟠 Medium Risk"
            else:
                risk = "🟢 Low Risk"

            st.subheader("Prediction Result")
            st.success(f"Risk Level: {risk}")
            st.write(f"Score: {risk_score}/12")

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
            """)

# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Doctor Dashboard")

    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Patient Phone")

    medicines = st.text_area("Medicines Prescribed")

    if st.button("Save Consultation"):
        st.success("✅ Saved Successfully")
