import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF

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

    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")

    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    # -------- Risk Prediction --------
    if option == "Predict Risk":

        st.header("👩 Patient Assessment")

        age = st.number_input("Enter Age", 10, 100)

        family_history = st.radio("Family History", ["Yes", "No"])
        family_value = 1 if family_history == "Yes" else 0

        if age < 50:
            st.subheader("🩸 Menstrual Details")

            menstrual_status = st.selectbox(
                "Menstrual Flow",
                ["Regular", "Irregular", "Heavy", "Absent"]
            )

            menstrual_value = ["Regular","Irregular","Heavy","Absent"].index(menstrual_status)
            menopause_value = 0

        else:
            st.subheader("🌸 Menopause Details")

            menopause = st.selectbox("Menopause Status", ["Yes", "No", "Unsure"])
            menopause_value = ["No","Yes","Unsure"].index(menopause)
            menstrual_value = 0

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

        if st.button("🔍 Predict Risk"):

            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value

            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 3:
                st.error("🔴 High Risk")
            elif risk_score >= 2:
                st.warning("🟠 Medium Risk")
            else:
                st.success("🟢 Low Risk")

            st.write(f"Score: {risk_score}/12")

    # -------- Care Plan --------
    else:

        st.header("🧾 Cancer Confirmed Care Plan")

        name = st.text_input("Patient Name")
        age = st.number_input("Age", 10, 100)
        phone = st.text_input("Phone Number")

        risk = st.selectbox("Risk Level", ["High", "Medium", "Low"])

        if st.button("Generate Care Plan"):

            st.success(f"Care Plan for {name}")


            # -------- WEEKLY PLAN --------
            st.subheader("📅 Weekly Diet & Exercise Plan")

            if risk == "High":

                data = {
                    "Day": ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"],
                    "Food": [
                        "Milk, Soup, Juice, Kanji",
                        "Protein drink, Soup, Coconut water",
                        "Milk, Dal soup, Juice",
                        "Soup, Porridge",
                        "Veg soup, Juice",
                        "Protein drink, Soup",
                        "Milk, Soup"
                    ],
                    "Exercise": [
                        "Breathing (5 mins)",
                        "Light stretching",
                        "Deep breathing",
                        "Relaxation",
                        "Light movement",
                        "Breathing",
                        "Rest"
                    ]
                }

                st.error("🔴 Severe Stage Plan")

            elif risk == "Medium":

                data = {
                    "Day": ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"],
                    "Food": [
                        "Idli, Rice + Dal, Banana",
                        "Oats, Khichdi, Juice",
                        "Upma, Rice + Veg",
                        "Idli, Soft rice",
                        "Oats, Khichdi",
                        "Dosa, Rice + Dal",
                        "Idli, Soft rice"
                    ],
                    "Exercise": [
                        "Walking (10 mins)",
                        "Stretching",
                        "Light yoga",
                        "Walking",
                        "Breathing",
                        "Stretching",
                        "Light yoga"
                    ]
                }

                st.warning("🟠 Mid Level Plan")

            else:

                data = {
                    "Day": ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"],
                    "Food": [
                        "Oats + Fruits, Rice + Veg",
                        "Idli, Spinach rice",
                        "Dosa, Brown rice",
                        "Upma, Veg rice",
                        "Oats, Veg biryani",
                        "Idli, Sambar",
                        "Dosa, Brown rice"
                    ],
                    "Exercise": [
                        "Walking (20 mins)",
                        "Yoga",
                        "Walking",
                        "Stretching",
                        "Yoga",
                        "Walking",
                        "Light workout"
                    ]
                }

                st.success("🟢 Starting Stage Plan")

            df_plan = pd.DataFrame(data)
            st.dataframe(df_plan)

# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Smart Doctor Dashboard")

    st.subheader("🩺 Doctor Info")
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("📋 Patient Details")

    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", 1, 120)
    patient_phone = st.text_input("Phone")

    risk_level = st.selectbox("Risk Level", ["High", "Medium", "Low"])

    last_visit = st.date_input("Last Visit")
    next_visit = st.date_input("Next Visit")

    medicines = st.text_area("Medicines")
    notes = st.text_area("Notes")

    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save"):

        record = {
            "Doctor": doctor_name,
            "Patient": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Medicines": medicines,
            "Next Visit": str(next_visit)
        }

        st.session_state["records"].append(record)
        st.success("Saved")

    if st.session_state["records"]:
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button("Download CSV", csv, "patients.csv")

    st.subheader("📄 PDF Report")

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Patient Report", ln=True)

        pdf.cell(200, 10, txt=f"Doctor: {doctor_name}", ln=True)
        pdf.cell(200, 10, txt=f"Patient: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk_level}", ln=True)

        file = "report.pdf"
        pdf.output(file)
        return file

    if st.button("Download PDF"):
        file = create_pdf()
        with open(file, "rb") as f:
            st.download_button("Click to Download", f, "report.pdf")
