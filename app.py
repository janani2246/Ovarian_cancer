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
