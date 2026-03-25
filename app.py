import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.distance import geodesic
import requests
import time
import speech_recognition as sr   # ✅ ADDED ONLY THIS

st.set_page_config(page_title="Ovarian Cancer AI", layout="wide")
st.title("🧬 Ovarian Cancer Detection & Care System")

# ---------------- BACKGROUND ----------------
def set_bg(color):
    st.markdown(f"""
    <style>
    .stApp {{
        background: {color};
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------- LOCATION FUNCTIONS ----------------
def get_location(address):
    geolocator = Nominatim(user_agent="hospital_app", timeout=10)
    for _ in range(3):
        try:
            return geolocator.geocode(address)
        except (GeocoderTimedOut, GeocoderUnavailable):
            time.sleep(2)
    return None

def get_hospitals_osm(lat, lon, radius=5000):
    url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="hospital"](around:{radius},{lat},{lon});
    out;
    """
    try:
        response = requests.get(url, params={'data': query}, timeout=15)
        data = response.json()
    except:
        return []

    hospitals = []
    for e in data.get('elements', []):
        name = e.get('tags', {}).get('name', 'Unknown Hospital')
        hospitals.append((name, e.get('lat'), e.get('lon')))
    return hospitals

def search_hospitals_by_name(name, city, state):
    geolocator = Nominatim(user_agent="hospital_app", timeout=10)
    loc = geolocator.geocode(f"{city}, {state}, India")
    if not loc:
        return []

    lat, lon = loc.latitude, loc.longitude
    url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="hospital"]["name"~"{name}",i](around:10000,{lat},{lon});
    out;
    """
    try:
        response = requests.get(url, params={'data': query}, timeout=15)
        data = response.json()
    except:
        return []

    results = []
    for e in data.get('elements', []):
        h_name = e.get('tags', {}).get('name', 'Unknown Hospital')
        results.append((h_name, e.get('lat'), e.get('lon')))
    return results

# ---------------- VOICE FUNCTION ----------------
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        st.success(f"🗣 You said: {text}")
        return text.lower()
    except:
        st.error("❌ Voice not recognized")
        return ""

# ---------------- ROLE ----------------
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ================= PATIENT =================
if role == "Patient":
    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")
    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    if option == "Predict Risk":
        st.header("👩 Patient Assessment")

        age = st.number_input("Enter Age", 10, 100)
        family_history = st.radio("Family History", ["Yes", "No"])
        family_value = 1 if family_history == "Yes" else 0

        if age < 50:
            menstrual_status = st.selectbox("Menstrual Flow", ["Regular","Irregular","Heavy","Absent"])
            menstrual_value = ["Regular","Irregular","Heavy","Absent"].index(menstrual_status)
            menopause_value = 0
        else:
            menopause = st.selectbox("Menopause Status", ["Yes","No","Unsure"])
            menopause_value = ["No","Yes","Unsure"].index(menopause)
            menstrual_value = 0

        symptoms = {
            "Pelvic Pain": st.checkbox("Pelvic Pain"),
            "Bloating": st.checkbox("Bloating"),
            "Fatigue": st.checkbox("Fatigue"),
        }

        # ✅ VOICE UI ADDED (ONLY THIS BLOCK)
        st.subheader("🎤 Voice Input (Optional)")
        if st.button("🎙 Speak Symptoms"):
            voice_text = voice_input()

            if "pain" in voice_text:
                symptoms["Pelvic Pain"] = True
            if "bloating" in voice_text:
                symptoms["Bloating"] = True
            if "fatigue" in voice_text or "tired" in voice_text:
                symptoms["Fatigue"] = True

            st.write("✅ Voice symptoms updated!")

        if st.button("🔍 Predict Risk"):
            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value
            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 3:
                st.session_state["risk_level"] = "High"
                st.error("🔴 High Risk")
            elif risk_score >= 2:
                st.session_state["risk_level"] = "Medium"
                st.warning("🟠 Medium Risk")
            else:
                st.session_state["risk_level"] = "Low"
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

