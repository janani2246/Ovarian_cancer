# ============================
# 👨‍⚕️ DOCTOR DASHBOARD (FULL)
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
        # CSV Download
        # --------------------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download All Patients (CSV)",
            csv,
            "patients_data.csv",
            "text/csv"
        )

        # --------------------------
        # Chart
        # --------------------------
        st.subheader("📈 Risk Analysis Chart")
        st.bar_chart(df["Risk"].value_counts())

    # --------------------------
    # PDF FULL REPORT
    # --------------------------
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="OVARIAN CANCER PATIENT REPORT", ln=True, align='C')

        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Doctor: {doctor_name}", ln=True)

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {patient_age}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {patient_phone}", ln=True)

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Risk Level: {risk_level}", ln=True)

        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=f"Medicines:\n{medicines}")

        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=f"Consultation Notes:\n{notes}")

        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=f"Food Plan:\n{food_plan(risk_level)}")

        pdf.ln(5)

        pdf.cell(200, 10, txt=f"Next Visit: {next_visit}", ln=True)

        file = "full_patient_report.pdf"
        pdf.output(file)

        return file

    if st.button("📄 Download Full Report"):
        file = create_pdf()

        with open(file, "rb") as f:
            st.download_button(
                "⬇️ Click to Download",
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
