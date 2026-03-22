import streamlit as st
import pandas as pd
import numpy as np
from datetime import date


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
# 👩 PATIENT (Unchanged)
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

        # Age-based Logic
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

        # Symptoms
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

        # Prediction
        if st.button("🔍 Predict Risk"):
            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value

            risk_score = sum([int(v) for v in symptoms.values()])
            if risk_score >= 4:
                risk = "🔴 High Risk"
            elif risk_score >= 3:
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
# 👨‍⚕️ DOCTOR (Enhanced)
# ============================
elif role == "Doctor":
    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")  # Blue
    st.header("👨‍⚕️ Doctor Dashboard")

    # Doctor Details
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    # Patient Details
    st.subheader("Patient Info / Checkup")
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", 10, 100)
    
    st.write("Select symptoms observed:")
    patient_symptoms = {
        "Pelvic Pain": st.checkbox("Pelvic Pain"),
        "Stomach Swelling": st.checkbox("Stomach Swelling"),
        "Bloating": st.checkbox("Persistent Bloating"),
        "Fatigue": st.checkbox("Fatigue"),
        "Back Pain": st.checkbox("Back Pain"),
        "Feeling Full Quickly": st.checkbox("Feeling Full Quickly"),
        "Urinary Urgency": st.checkbox("Urinary Urgency"),
        "Weight Loss": st.checkbox("Weight Loss"),
        "Vaginal Bleeding": st.checkbox("Vaginal Bleeding"),
    }

    medicines = st.text_area("Medicines Prescribed")
    next_checkup = st.date_input("Next Check-up Date", min_value=date.today())

    # Save Consultation as PDF
    if st.button("Save Consultation"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(0, 10, f"Doctor: {doctor_name}, Phone: {doctor_phone}", ln=True)
        pdf.cell(0, 10, f"Patient: {patient_name}, Age: {patient_age}", ln=True)
        pdf.cell(0, 10, "Symptoms Observed:", ln=True)
        for sym, val in patient_symptoms.items():
            if val:
                pdf.cell(0, 10, f"- {sym}", ln=True)
        pdf.cell(0, 10, f"Medicines Prescribed: {medicines}", ln=True)
        pdf.cell(0, 10, f"Next Check-up Date: {next_checkup}", ln=True)

        filename = f"{patient_name}_consultation.pdf"
        pdf.output(filename)

        st.success(f"✅ Consultation saved as PDF: {filename}")
        st.info("You can open the PDF from your computer")

    # Display Saved Record
    if "patient" in st.session_state:
        st.subheader("📁 Last Saved Record")
        st.write(st.session_state["patient"])
