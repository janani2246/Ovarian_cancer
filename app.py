import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")

st.title("🧬 Ovarian Cancer Detection & Care System")

# Sidebar Role
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ============================
# 👩 PATIENT
# ============================
if role == "Patient":

    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    # ================= OPTION 1 =================
    if option == "Predict Risk":
        st.header("👩 Patient Assessment")

        age = st.number_input("Enter Age", 10, 100)

        menopause = st.selectbox("Menopause Status", ["Yes", "No", "Unsure"])

        family_history = st.radio("Family History", ["Yes", "No"])

        st.subheader("Select Symptoms")

        symptoms = {
            "Pelvic Pain": st.checkbox("Pelvic Pain"),
            "Stomach Swelling": st.checkbox("Stomach Swelling"),
            "Bloating": st.checkbox("Persistent Bloating"),
            "Fatigue": st.checkbox("Fatigue"),
            "Back Pain": st.checkbox("Back Pain"),
            "Feeling_Full_Quickly": st.checkbox("Feeling_Full_Quickly"),
            "Urinary_Urgency": st.checkbox("Urinary_Urgency"),
            "weight_loss": st.checkbox("weight_loss"),
            "vaginal_bleeding": st.checkbox("vaginal_bleeding"),
            "menstural_status": st.checkbox("menstural_status"),
            
            
            
        }

        report = st.file_uploader("Upload Reports (Optional)", type=["pdf","png","jpg"])

        if st.button("🔍 Predict Risk"):

            # Replace with your ML model later
            risk_score = sum(symptoms.values())

            if risk_score >= 3:
                risk = "🔴 High Risk"
            elif risk_score == 2:
                risk = "🟠 Medium Risk"
            else:
                risk = "🟢 Low Risk"

            st.subheader("Prediction Result")
            st.success(f"Risk Level: {risk}")
            st.write(f"Score: {risk_score}/5")

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

            # Timetable
            st.subheader("📅 Daily Timetable")
            st.write("""
            - 🏃 7–8 AM → Exercise  
            - 🍽 9–10 AM → Breakfast + Medicine  
            - 🍛 1–2 PM → Lunch + Medicine  
            - 🍽 7–8 PM → Dinner + Medicine  
            - 💧 Drink water regularly  
            """)

            # Diet Plan
            st.subheader("🥗 Diet Plan")
            st.write("""
            - Eat fruits & vegetables  
            - Avoid junk & oily food  
            - Balanced diet  
            """)

            # Alerts (Simulation)
            st.subheader("🔔 Alerts (Simulation)")
            st.info("Reminder: Breakfast at 9 AM")
            st.info("Reminder: Lunch at 1 PM")
            st.info("Reminder: Dinner at 7 PM")

# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    st.header("👨‍⚕️ Doctor Dashboard")

    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("Patient Info")
    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Patient Phone")

    last_visit = st.date_input("Last Visit")

    medicines = st.text_area("Medicines Prescribed")
    notes = st.text_area("Consultation Notes")

    # Store data (temporary)
    if st.button("Save Consultation"):
        st.session_state["patient"] = {
            "name": patient_name,
            "meds": medicines,
            "notes": notes
        }
        st.success("✅ Saved Successfully")

    # Show stored data
    if "patient" in st.session_state:
        st.subheader("📁 Saved Record")
        st.write(st.session_state["patient"])

    # AI Follow-up
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
