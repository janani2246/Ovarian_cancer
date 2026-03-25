import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF

st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")

st.title("🧬 Ovarian Cancer Detection & Care System")

def set_bg(color):
    st.markdown(f"""
    <style>
    .stApp {{
        background: {color};
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ================= PATIENT =================
if role == "Patient":

    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")

    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    # -------- Predict --------
    if option == "Predict Risk":

        st.header("👩 Patient Assessment")

        age = st.number_input("Enter Age", 10, 100)

        family_history = st.radio("Family History", ["Yes", "No"])
        family_value = 1 if family_history == "Yes" else 0

        if age < 50:
            menstrual_status = st.selectbox(
                "Menstrual Flow",
                ["Regular", "Irregular", "Heavy", "Absent"]
            )
            menstrual_value = ["Regular","Irregular","Heavy","Absent"].index(menstrual_status)
            menopause_value = 0
        else:
            menopause = st.selectbox("Menopause Status", ["Yes", "No", "Unsure"])
            menopause_value = ["No","Yes","Unsure"].index(menopause)
            menstrual_value = 0

        symptoms = {
            "Pelvic Pain": st.checkbox("Pelvic Pain"),
            "Bloating": st.checkbox("Bloating"),
            "Fatigue": st.checkbox("Fatigue"),
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

            st.subheader("📅 Daily Timetable")
            st.write("""
- 🏃 7–8 AM → Exercise  
- 🍽 9–10 AM → Breakfast  
- 🍛 1–2 PM → Lunch  
- 🍽 7–8 PM → Dinner  
""")

            # ================= FOOD TIMETABLE =================
            st.subheader("🍽 1 Week Food Timetable")

            if risk == "High":

                data = {
                    "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                    "Breakfast": ["Milk+Oats","Soup","Juice","Milk","Oats","Soup","Juice"],
                    "Lunch": ["Veg Soup","Dal Soup","Rice+Veg","Soup","Veg Soup","Dal Soup","Soup"],
                    "Dinner": ["Kanji","Porridge","Soup","Milk","Soup","Porridge","Kanji"]
                }
                st.error("🔴 Severe Stage Diet")

            elif risk == "Medium":

                data = {
                    "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                    "Breakfast": ["Idli","Oats","Upma","Dosa","Idli","Oats","Dosa"],
                    "Lunch": ["Rice+Dal","Khichdi","Veg Rice","Curd Rice","Rice+Dal","Veg Rice","Curd Rice"],
                    "Dinner": ["Chapati","Soup","Chapati","Soup","Chapati","Soup","Chapati"]
                }
                st.warning("🟠 Medium Stage Diet")

            else:

                data = {
                    "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                    "Breakfast": ["Oats+Fruits","Idli","Dosa","Upma","Oats","Idli","Dosa"],
                    "Lunch": ["Brown Rice","Veg Rice","Dal Rice","Curd Rice","Veg Rice","Dal Rice","Curd Rice"],
                    "Dinner": ["Chapati","Soup","Chapati","Soup","Chapati","Soup","Chapati"]
                }
                st.success("🟢 Starting Stage Diet")

            df_food = pd.DataFrame(data)
            st.table(df_food)



# ============================
# 👨‍⚕️ DOCTOR
# ============================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Smart Doctor Dashboard")

    # ---------------- DOCTOR INFO ----------------
    st.subheader("👨‍⚕️ Doctor Details")
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    # ---------------- PATIENT INFO ----------------
    st.subheader("🧾 Patient Details")

    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", 1, 120)
    patient_phone = st.text_input("Phone Number")

    risk_level = st.selectbox("Risk Level", ["High", "Medium", "Low"])
    medicines = st.text_area("Medicines Prescribed")
    notes = st.text_area("Doctor Notes")

    last_visit = st.date_input("Last Visit")
    next_visit = st.date_input("Next Visit")

    # ---------------- SESSION STORAGE ----------------
    if "records" not in st.session_state:
        st.session_state["records"] = []

    # ---------------- SAVE RECORD ----------------
    if st.button("💾 Save Patient Record"):

        record = {
            "Doctor": doctor_name,
            "Doctor Phone": doctor_phone,
            "Name": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Medicines": medicines,
            "Notes": notes,
            "Last Visit": str(last_visit),
            "Next Visit": str(next_visit)
        }

        st.session_state["records"].append(record)
        st.success("✅ Patient Record Saved")

    # ---------------- DISPLAY DATA ----------------
    if st.session_state["records"]:

        df = pd.DataFrame(st.session_state["records"])

        st.subheader("📊 Patient Records")
        st.dataframe(df)

        # ---------------- SEARCH ----------------
        st.subheader("🔍 Search Patient")
        search = st.text_input("Enter Name")

        if search:
            filtered = df[df["Name"].str.contains(search, case=False)]
            st.write(filtered)

        # ---------------- DELETE ----------------
        st.subheader("❌ Delete Record")
        delete_name = st.text_input("Enter Name to Delete")

        if st.button("Delete Record"):
            st.session_state["records"] = [
                r for r in st.session_state["records"]
                if r["Name"].lower() != delete_name.lower()
            ]
            st.success("Deleted Successfully")

        # ---------------- DOWNLOAD CSV ----------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV", csv, "patients.csv")

        # ---------------- CHART ----------------
        st.subheader("📈 Risk Analysis")
        st.bar_chart(df["Risk"].value_counts())

        # ---------------- PDF GENERATION ----------------
        st.subheader("📄 Generate Patient Report")

        selected_patient = st.selectbox("Select Patient", df["Name"])

        def create_pdf(data):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Patient Medical Report", ln=True, align='C')
            pdf.ln(10)

            for key, value in data.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

            file = f"{data['Name']}_report.pdf"
            pdf.output(file)
            return file

        if st.button("📄 Generate PDF"):
            patient_data = next(
                r for r in st.session_state["records"]
                if r["Name"] == selected_patient
            )

            file = create_pdf(patient_data)

            with open(file, "rb") as f:
                st.download_button("⬇ Download Report", f, file)

        # ---------------- ALERT SYSTEM ----------------
        st.subheader("⏰ Today Alerts")

        today = str(datetime.date.today())

        for r in st.session_state["records"]:
            if r["Next Visit"] == today:
                st.warning(f"⚠️ {r['Name']} has appointment today!")
