import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")

st.title("🧬 Ovarian Cancer Detection & Care System")

# ================= BACKGROUND STYLE =================
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

    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")  # 💗 Pink Gradient

    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

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
            "Feeling_Full_Quickly": st.checkbox("Feeling Full Quickly"),
            "Urinary_Urgency": st.checkbox("Urinary Urgency"),
            "Weight_Loss": st.checkbox("Weight Loss"),
            "Vaginal_Bleeding": st.checkbox("Vaginal Bleeding"),
        }

        # ✅ FIXED Menstrual Dropdown
        menstrual_status = st.selectbox(
            "🩸 Menstrual Flow",
            ["Regular", "Irregular", "Heavy"]
        )

        # ✅ ENCODING
        if menstrual_status == "Regular":
            menstrual_value = 0
        elif menstrual_status == "Irregular":
            menstrual_value = 1
        else:
            menstrual_value = 2

        report = st.file_uploader("Upload Reports (Optional)", type=["pdf","png","jpg"])

        if st.button("🔍 Predict Risk"):

            # ✅ ADD menstrual into symptoms
            symptoms["Menstrual"] = menstrual_value

            # ✅ FIXED SUM
            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 3:
                risk = "🔴 High Risk"
            elif risk_score == 2:
                risk = "🟠 Medium Risk"
            else:
                risk = "🟢 Low Risk"

            st.subheader("Prediction Result")
            st.success(f"Risk Level: {risk}")
            st.write(f"Score: {risk_score}/10")

            if "High" in risk:
                st.error("⚠️ Immediate doctor consultation required")
            elif "Medium" in risk:
                st.warning("⚠️ Regular checkup needed")
            else:
                st.success("✅ You are healthy")

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

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")  # 💙 Blue Gradient

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
