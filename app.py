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

# ---------------- ROLE ----------------
role = st.sidebar.radio("Select Role", ["Patient", "Doctor"])

# ================= PATIENT =================
if role == "Patient":
    set_bg("linear-gradient(to right, #ffdde1, #ffccdd)")
    option = st.radio("Choose Option", ["Predict Risk", "Care Plan (Cancer Confirmed)"])

    # -------- Predict Risk --------
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

        # Predict button
        if st.button("🔍 Predict Risk"):
            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value
            risk_score = sum([int(v) for v in symptoms.values()])

            # Persist risk_level in session_state
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

    # -------- Hospital Finder for High/Medium Risk --------
    if "risk_level" in st.session_state and st.session_state["risk_level"] in ["High", "Medium"]:
        st.subheader("🏥 Find Nearby Hospitals")

        area = st.text_input("Area")
        city = st.text_input("City")
        state = st.text_input("State")
        search = st.text_input("🔍 Search Hospital Name (optional)")

        if st.button("📍 Find Hospitals Near You"):
            if not city or not state:
                st.warning("⚠️ Please enter City and State")
            else:
                full_address = f"{area}, {city}, {state}, India"
                with st.spinner("📍 Finding your location..."):
                    location = get_location(full_address)

                if location:
                    lat, lon = location.latitude, location.longitude
                    st.success(f"✅ Location found: ({lat}, {lon})")

                    with st.spinner("🏥 Fetching nearby hospitals..."):
                        nearby = get_hospitals_osm(lat, lon)
                        searched = search_hospitals_by_name(search, city, state) if search else []
                        combined = {(h[1], h[2]): h for h in nearby + searched}
                        final = list(combined.values())

                    if final:
                        # Sort by distance
                        final_sorted = sorted(final, key=lambda h: geodesic((lat, lon), (h[1], h[2])).km)
                        
                        # Map
                        map_data = pd.DataFrame([(lat, lon)] + [(h[1], h[2]) for h in final_sorted[:10]],
                                                columns=["lat", "lon"])
                        st.map(map_data)

                        # Display hospitals
                        data_list = []
                        for h in final_sorted[:10]:
                            name, h_lat, h_lon = h
                            dist = round(geodesic((lat, lon), (h_lat, h_lon)).km, 2)
                            map_link = f"https://www.google.com/maps?q={h_lat},{h_lon}"
                            st.markdown(f"""
                            <div style="border:1px solid #ddd; padding:10px; border-radius:10px;">
                                <b>🏥 {name}</b><br>
                                📏 {dist} km<br>
                                <a href="{map_link}" target="_blank">Open Map</a>
                            </div>
                            """, unsafe_allow_html=True)
                            data_list.append([name, dist, h_lat, h_lon])

                        df = pd.DataFrame(data_list, columns=["Hospital Name", "Distance (km)", "Latitude", "Longitude"])
                        st.download_button("⬇ Download Hospital List", df.to_csv(index=False), "hospitals.csv")

                    else:
                        st.warning("⚠️ No hospitals found. Check spelling or try another location.")
                else:
                    st.error("❌ Location not found. Check city/state or network.")

    # -------- Care Plan --------
    if option == "Care Plan (Cancer Confirmed)":
        st.header("🧾 Cancer Confirmed Care Plan")
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 10, 100)
        phone = st.text_input("Phone Number")
        risk = st.selectbox("Risk Level", ["High","Medium","Low"])

        if st.button("Generate Care Plan"):
            st.success(f"Care Plan for {name}")

            st.subheader("📅 Daily Timetable")
            st.write("""
- 🏃 7–8 AM → Exercise  
- 🍽 9–10 AM → Breakfast  
- 🍛 1–2 PM → Lunch  
- 🍽 7–8 PM → Dinner  
""")

            # Food Table
            if risk == "High":
                data = {"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                        "Breakfast":["Milk+Oats","Soup","Juice","Milk","Oats","Soup","Juice"],
                        "Lunch":["Veg Soup","Dal Soup","Rice+Veg","Soup","Veg Soup","Dal Soup","Soup"],
                        "Dinner":["Kanji","Porridge","Soup","Milk","Soup","Porridge","Kanji"]}
                st.error("🔴 Severe Stage Diet")
            elif risk == "Medium":
                data = {"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                        "Breakfast":["Idli","Oats","Upma","Dosa","Idli","Oats","Dosa"],
                        "Lunch":["Rice+Dal","Khichdi","Veg Rice","Curd Rice","Rice+Dal","Veg Rice","Curd Rice"],
                        "Dinner":["Chapati","Soup","Chapati","Soup","Chapati","Soup","Chapati"]}
                st.warning("🟠 Medium Stage Diet")
            else:
                data = {"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                        "Breakfast":["Oats+Fruits","Idli","Dosa","Upma","Oats","Idli","Dosa"],
                        "Lunch":["Brown Rice","Veg Rice","Dal Rice","Curd Rice","Veg Rice","Dal Rice","Curd Rice"],
                        "Dinner":["Chapati","Soup","Chapati","Soup","Chapati","Soup","Chapati"]}
                st.success("🟢 Starting Stage Diet")

            df_food = pd.DataFrame(data)
            st.table(df_food)

# ============================ DOCTOR ===========================
elif role == "Doctor":
    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")
    st.header("👨‍⚕️ Smart Doctor Dashboard")

    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("Patient Info")
    patient_name = st.text_input("Patient Name")
    patient_phone = st.text_input("Patient Phone")
    patient_age = st.number_input("Age", 1, 120)
    risk_level = st.selectbox("Risk Level", ["High","Medium","Low"])
    last_visit = st.date_input("Last Visit")
    next_visit = st.date_input("Next Visit")
    medicines = st.text_area("Medicines Prescribed")
    notes = st.text_area("Consultation Notes")

    # Save patient record
    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save Full Record"):
        st.session_state["records"].append({
            "Name": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Next Visit": str(next_visit),
            "Medicines": medicines,
            "Notes": notes
        })
        st.success("Saved")

    # Show records
    if st.session_state["records"]:
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        # CSV download
        st.download_button("⬇ Download Patients CSV", df.to_csv(index=False), "patients.csv")

        # Risk chart
        st.bar_chart(df["Risk"].value_counts())

        # PDF generation
        def create_pdf(rec):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Patient: {rec['Name']}", ln=True)
            pdf.cell(200, 10, txt=f"Age: {rec['Age']}", ln=True)
            pdf.cell(200, 10, txt=f"Risk: {rec['Risk']}", ln=True)
            pdf.cell(200, 10, txt=f"Next Visit: {rec['Next Visit']}", ln=True)
            pdf.cell(200, 10, txt=f"Medicines: {rec['Medicines']}", ln=True)
            pdf.cell(200, 10, txt=f"Notes: {rec['Notes']}", ln=True)
            filename = f"{rec['Name']}_report.pdf"
            pdf.output(filename)
            return filename

        for rec in st.session_state["records"]:
            if st.button(f"📄 Download PDF for {rec['Name']}"):
                file = create_pdf(rec)
                with open(file, "rb") as f:
                    st.download_button("Download PDF", f, file)
