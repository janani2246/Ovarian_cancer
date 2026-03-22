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

    # ================= OPTION 1 =================
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
                risk = "🔴 High Risk"
            elif risk_score >= 2:
                risk = "🟠 Medium Risk"
            else:
                risk = "🟢 Low Risk"

            st.success(f"Risk Level: {risk}")
            st.write(f"Score: {risk_score}/12")

    # ================= OPTION 2 =================
    else:
        st.header("🧾 Cancer Care Plan")

        st.write("Follow diet, medicine and exercise regularly.")

# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Smart Doctor Dashboard")

    # Basic Info (OLD)
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("Patient Info")
    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Patient Phone")

    last_visit = st.date_input("Last Visit")

    medicines = st.text_area("Medicines Prescribed")

    notes = st.text_area("Consultation Notes")

    if st.button("Save Consultation"):
        st.session_state["patient"] = {
            "name": patient_name,
            "meds": medicines,
            "notes": notes
        }
        st.success("Saved")

    if "patient" in st.session_state:
        st.write(st.session_state["patient"])

    # ================= NEW FEATURES =================

    st.subheader("➕ Additional Details")

    patient_age = st.number_input("Age", 1, 120)
    risk_level = st.selectbox("Risk Level", ["High", "Medium", "Low"])
    next_visit = st.date_input("Next Visit")

    # Food Plan
    def food_plan(risk):
        if risk == "High":
            return "Strict Diet (No Oil, Fruits, Veg)"
        elif risk == "Medium":
            return "Controlled Diet"
        else:
            return "Normal Diet"

    st.info(food_plan(risk_level))

    # Save multiple patients
    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save Full Record"):
        st.session_state["records"].append({
            "Name": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Next Visit": str(next_visit)
        })
        st.success("Saved")

    # Show data
    if st.session_state["records"]:
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        # Search
        search = st.text_input("Search Patient")
        if search:
            st.write(df[df["Name"].str.contains(search, case=False)])

        # Delete
        delete_name = st.text_input("Delete Name")
        if st.button("Delete"):
            st.session_state["records"] = [
                r for r in st.session_state["records"]
                if r["Name"].lower() != delete_name.lower()
            ]
            st.success("Deleted")

        # CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "patients.csv")

        # Chart
        st.bar_chart(df["Risk"].value_counts())

    # PDF
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Patient: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk_level}", ln=True)

        file = "report.pdf"
        pdf.output(file)
        return file

    if st.button("📄 Download PDF"):
        file = create_pdf()
        with open(file, "rb") as f:
            st.download_button("Download", f, "report.pdf")

    # Alerts
    today = str(datetime.date.today())
    for r in st.session_state["records"]:
        if r["Next Visit"] == today:
            st.warning(f"{r['Name']} has visit today!")
