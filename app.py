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


    # ============================
# 👨‍⚕️ DOCTOR DASHBOARD
# ============================

elif role == "Doctor":

    import datetime
    from fpdf import FPDF

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Doctor Dashboard")

    # --------------------------
    # Doctor Info
    # --------------------------
    st.subheader("🩺 Doctor Info")
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    # --------------------------
    # Patient Info
    # --------------------------
    st.subheader("📋 Patient Details")

    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", 1, 120)
    patient_phone = st.text_input("Phone Number")

    risk_level = st.selectbox("Risk Level", ["High", "Medium", "Low"])

    last_visit = st.date_input("Last Visit")
    next_visit = st.date_input("Next Visit")

    medicines = st.text_area("Medicines Prescribed")

    notes = st.text_area("Consultation Notes")

    # --------------------------
    # Food Plan Logic
    # --------------------------
    def get_food_plan(risk):
        if risk == "High":
            return """High Risk Diet:
- Oats, Fruits
- Brown rice, Vegetables
- Soup, Salad
- Avoid Oil & Sugar"""
        elif risk == "Medium":
            return """Medium Risk Diet:
- Idli / Dosa
- Rice + Veg Curry
- Chapati"""
        else:
            return """Low Risk:
- Normal Healthy Diet
- Exercise Daily"""

    st.subheader("🥗 Food Recommendation")
    st.text(get_food_plan(risk_level))

    # --------------------------
    # Save Multiple Patients
    # --------------------------
    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save Patient Record"):

        record = {
            "Name": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Next Visit": str(next_visit),
            "Medicines": medicines
        }

        st.session_state["records"].append(record)

        st.success("✅ Patient Saved Successfully")

    # --------------------------
    # Show All Patients
    # --------------------------
    if st.session_state["records"]:
        st.subheader("📊 All Patients Data")

        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        # --------------------------
        # Search
        # --------------------------
        st.subheader("🔍 Search Patient")
        search = st.text_input("Enter Name")

        if search:
            result = df[df["Name"].str.contains(search, case=False)]
            st.write(result)

        # --------------------------
        # Delete
        # --------------------------
        st.subheader("❌ Delete Patient")
        delete_name = st.text_input("Enter Name to Delete")

        if st.button("Delete"):
            st.session_state["records"] = [
                r for r in st.session_state["records"]
                if r["Name"].lower() != delete_name.lower()
            ]
            st.success("Deleted Successfully")

        # --------------------------
        # CSV Download
        # --------------------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "patients_data.csv",
            "text/csv"
        )

        # --------------------------
        # Chart
        # --------------------------
        st.subheader("📈 Risk Analysis")
        st.bar_chart(df["Risk"].value_counts())

    # --------------------------
    # PDF Report
    # --------------------------
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Patient Report", ln=True)

        pdf.cell(200, 10, txt=f"Doctor: {doctor_name}", ln=True)
        pdf.cell(200, 10, txt=f"Patient: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {patient_phone}", ln=True)
        pdf.cell(200, 10, txt=f"Risk: {risk_level}", ln=True)

        pdf.multi_cell(0, 10, txt=f"Medicines:\n{medicines}")
        pdf.multi_cell(0, 10, txt=f"Notes:\n{notes}")

        pdf.cell(200, 10, txt=f"Next Visit: {next_visit}", ln=True)

        file = "patient_report.pdf"
        pdf.output(file)

        return file

    if st.button("📄 Generate PDF"):
        file = create_pdf()

        with open(file, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                "patient_report.pdf"
            )

    # --------------------------
    # Alerts
    # --------------------------
    st.subheader("🔔 Alerts")

    today = str(datetime.date.today())

    for r in st.session_state["records"]:
        if r["Next Visit"] == today:
            st.warning(f"⚠️ {r['Name']} has visit today!")
