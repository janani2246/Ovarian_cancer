import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")

# ----------------------------
# Title
# ----------------------------
st.title("🧬 Ovarian Cancer Detection & Care System")

# ----------------------------
# Sidebar Role Selection
# ----------------------------
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ============================
# 🧍 PATIENT FLOW
# ============================
if role == "Patient":
    st.header("👩 Patient Assessment")

    # Step A: Age
    age = st.number_input("Enter Age", 10, 100)

    # Step B: Menopause
    menopause = st.selectbox("Menopause Status", ["Yes", "No", "Unsure"])

    # Step C: Family History
    family_history = st.radio("Family History", ["Yes", "No"])

    # Step D: Symptoms
    st.subheader("Select Symptoms")
    symptoms = {
        "Pelvic Pain": st.checkbox("Pelvic Pain"),
        "Stomach Swelling": st.checkbox("Stomach Swelling"),
        "Bloating": st.checkbox("Persistent Bloating"),
        "Fatigue": st.checkbox("Fatigue"),
        "Back Pain": st.checkbox("Back Pain")
    }

    # Step E: Upload Reports
    st.subheader("Upload Medical Reports")
    report = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg"])

    medicines = st.text_input("Current Medicines (optional)")

    # ----------------------------
    # Step F: Prediction
    # ----------------------------
    if st.button("🔍 Predict Risk"):
        
        # Simple rule-based (you can replace with your ML model)
        risk_score = sum(symptoms.values())

        if risk_score >= 3:
            risk = "High Risk 🔴"
        elif risk_score == 2:
            risk = "Medium Risk 🟠"
        else:
            risk = "Low Risk 🟢"

        st.subheader("Prediction Result")
        st.write(f"Risk Level: **{risk}**")
        st.write(f"Risk Score: {risk_score}/5")

        # Recommendation
        if risk_score >= 2:
            st.warning("⚠️ Please consult a doctor immediately")
        else:
            st.success("✅ Maintain healthy lifestyle")

    # ----------------------------
    # Step G: Diet Suggestions
    # ----------------------------
    st.subheader("🥗 Diet & Lifestyle Advice")

    st.write("""
    - Eat fruits and vegetables
    - Avoid fried/junk foods
    - Drink plenty of water
    - Exercise regularly
    """)

# ============================
# 👨‍⚕️ DOCTOR DASHBOARD
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

    st.subheader("Upload Reports / Notes")
    report = st.file_uploader("Upload Patient Reports")

    notes = st.text_area("Consultation Notes")

    if st.button("Save Consultation"):
        st.success("✅ Consultation Saved")

    # ----------------------------
    # AI Follow-up
    # ----------------------------
    st.subheader("🤖 AI Follow-up")

    if st.button("Generate Follow-up"):
        st.write("### AI Recommendation")

        st.write("""
        - Continue prescribed medicines
        - Follow strict diet plan
        - Avoid oily and junk foods
        - Regular checkups every 3 months
        """)

        st.info("Follow doctor instructions strictly")