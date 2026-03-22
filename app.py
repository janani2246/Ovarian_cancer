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
                risk = "🔴 High Risk"
                st.error(risk)
            elif risk_score >= 2:
                risk = "🟠 Medium Risk"
                st.warning(risk)
            else:
                risk = "🟢 Low Risk"
                st.success(risk)

            st.write(f"Score: {risk_score}/12")

    # -------- Care Plan --------
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

            st.subheader("🥗 Diet Plan")

            if risk == "High":
                st.write("Strict diet: Fruits, Vegetables, No Oil")
            else:
                st.write("Balanced Diet")

# ============================
# 👨‍⚕️ DOCTOR
# ============================
# ============================
# 👨‍⚕️ DOCTOR DASHBOARD (IMPROVED)
# ============================

elif role == "Doctor":

    import datetime
    from fpdf import FPDF

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Smart Doctor Dashboard")

    # --------------------------
    # Doctor Info
    # --------------------------
    st.subheader("🩺 Doctor Information")
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    # --------------------------
    # Patient Details
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
    # Food Plan
    # --------------------------
    def food_plan(risk):
        if risk == "High":
            return """High Risk Diet:
- Morning: Oats + Fruits
- Lunch: Brown Rice + Vegetables
- Dinner: Soup + Salad
- Avoid Oil & Sugar"""
        elif risk == "Medium":
            return """Medium Risk Diet:
- Idli / Dosa
- Rice + Veg Curry
- Chapati"""
        else:
            return """Low Risk Diet:
- Normal Healthy Food
- Exercise Daily"""

    st.subheader("🥗 Food Recommendation")
    st.text(food_plan(risk_level))

    # --------------------------
    # Save Records
    # --------------------------
    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save Patient Record"):

        record = {
            "Doctor": doctor_name,
            "Patient": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Medicines": medicines,
            "Notes": notes,
            "Food Plan": food_plan(risk_level),
            "Last Visit": str(last_visit),
            "Next Visit": str(next_visit)
        }

        st.session_state["records"].append(record)

        st.success("✅ Patient Record Saved")

    # --------------------------
    # Show Records
    # --------------------------
    if st.session_state["records"]:
        st.subheader("📊 All Patients Data")

        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        # --------------------------
        # Search
        # --------------------------
        st.subheader("🔍 Search Patient")
        search = st.text_input("Enter Patient Name")

        if search:
            result = df[df["Patient"].str.contains(search, case=False)]
            st.write(result)

        # --------------------------
        # Delete
        # --------------------------
        st.subheader("❌ Delete Patient")
        delete_name = st.text_input("Enter Name to Delete")

        if st.button("Delete Record"):
            st.session_state["records"] = [
                r for r in st.session_state["records"]
                if r["Patient"].lower() != delete_name.lower()
            ]
            st.success("Deleted Successfully")

        # --------------------------
        # CSV Download (ALL DATA)
        # --------------------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download FULL Data (CSV)",
            csv,
            "full_patient_data.csv",
            "text/csv"
        )

        # --------------------------
        # Chart
        # --------------------------
        st.subheader("📈 Risk Analysis Chart")
        st.bar_chart(df["Risk"].value_counts())

    # --------------------------
    # PDF FULL REPORT (ALL DETAILS)
    # --------------------------
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="OVARIAN CANCER FULL REPORT", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Doctor: {doctor_name}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {doctor_phone}", ln=True)

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Patient: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {patient_phone}", ln=True)

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Risk Level: {risk_level}", ln=True)

        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=f"Medicines:\n{medicines}")
        pdf.multi_cell(0, 10, txt=f"Consultation Notes:\n{notes}")

        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=f"Food Plan:\n{food_plan(risk_level)}")

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Last Visit: {last_visit}", ln=True)
        pdf.cell(200, 10, txt=f"Next Visit: {next_visit}", ln=True)

        file = "full_patient_report.pdf"
        pdf.output(file)

        return file

    if st.button("📄 Download Full Report"):
        file = create_pdf()

        with open(file, "rb") as f:
            st.download_button(
                "⬇️ Click to Download PDF",
                f,
                "patient_full_report.pdf"
            )

    # --------------------------
    # Alerts
    # --------------------------
    st.subheader("🔔 Alerts")

    today = str(datetime.date.today())

    for r in st.session_state["records"]:
        if r["Next Visit"] == today:
            st.warning(f"⚠️ {r['Patient']} has visit today!")
