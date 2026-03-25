import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF

# 🔥 NEW IMPORTS (Location)
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
    for element in data.get('elements', []):
        name = element.get('tags', {}).get('name', 'Unknown Hospital')
        hospitals.append((name, element.get('lat'), element.get('lon')))
    return hospitals


# ---------------- ROLE ----------------
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

            # RESULT
            if risk_score >= 3:
                st.error("🔴 High Risk")
                risk_level = "High"
            elif risk_score >= 2:
                st.warning("🟠 Medium Risk")
                risk_level = "Medium"
            else:
                st.success("🟢 Low Risk")
                risk_level = "Low"

            st.write(f"Score: {risk_score}/12")

            # ================= HOSPITAL FINDER =================
            if risk_level in ["High", "Medium"]:

                st.subheader("🏥 Find Nearby Hospitals")

                area = st.text_input("Area")
                city = st.text_input("City")
                state = st.text_input("State")

                if st.button("📍 Search Hospitals"):

                    full_address = f"{area}, {city}, {state}, India"

                    with st.spinner("📍 Finding location..."):
                        location = get_location(full_address)

                    if location:
                        lat, lon = location.latitude, location.longitude
                        st.success("✅ Location Found")

                        with st.spinner("🏥 Fetching hospitals..."):
                            hospitals = get_hospitals_osm(lat, lon)

                        if hospitals:
                            st.subheader("🏥 Nearby Hospitals")

                            hospitals_sorted = sorted(
                                hospitals,
                                key=lambda h: geodesic((lat, lon), (h[1], h[2])).km
                            )

                            # MAP
                            map_data = pd.DataFrame(
                                [(lat, lon)] + [(h[1], h[2]) for h in hospitals_sorted[:10]],
                                columns=["lat", "lon"]
                            )
                            st.map(map_data)

                            # DISPLAY
                            data_list = []
                            for h in hospitals_sorted[:10]:
                                name, h_lat, h_lon = h
                                dist = round(geodesic((lat, lon), (h_lat, h_lon)).km, 2)

                                st.markdown(f"""
                                <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:8px;">
                                    <b>🏥 {name}</b><br>
                                    📏 {dist} km<br>
                                    <a href="https://www.google.com/maps?q={h_lat},{h_lon}" target="_blank">Open Map</a>
                                </div>
                                """, unsafe_allow_html=True)

                                data_list.append([name, dist, h_lat, h_lon])

                            # CSV DOWNLOAD
                            df_hosp = pd.DataFrame(data_list, columns=["Name", "Distance", "Lat", "Lon"])
                            csv = df_hosp.to_csv(index=False).encode("utf-8")
                            st.download_button("⬇ Download Hospitals CSV", csv, "hospitals.csv")

                        else:
                            st.warning("No hospitals found")

                    else:
                        st.error("Location not found")

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

            st.subheader("🍽 1 Week Food Timetable")

            if risk == "High":
                st.error("🔴 Severe Stage Diet")
            elif risk == "Medium":
                st.warning("🟠 Medium Stage Diet")
            else:
                st.success("🟢 Starting Stage Diet")


# ================= DOCTOR =================
elif role == "Doctor":

    set_bg("linear-gradient(to right, #dbeafe, #cce0ff)")

    st.header("👨‍⚕️ Smart Doctor Dashboard")

    st.subheader("👨‍⚕️ Doctor Details")
    doctor_name = st.text_input("Doctor Name")
    doctor_phone = st.text_input("Doctor Phone")

    st.subheader("🧾 Patient Details")

    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Age", 1, 120)
    patient_phone = st.text_input("Phone Number")

    risk_level = st.selectbox("Risk Level", ["High", "Medium", "Low"])
    medicines = st.text_area("Medicines Prescribed")
    notes = st.text_area("Doctor Notes")

    last_visit = st.date_input("Last Visit")
    next_visit = st.date_input("Next Visit")

    if "records" not in st.session_state:
        st.session_state["records"] = []

    if st.button("💾 Save Patient Record"):
        st.session_state["records"].append({
            "Name": patient_name,
            "Age": patient_age,
            "Phone": patient_phone,
            "Risk": risk_level,
            "Next Visit": str(next_visit)
        })
        st.success("Saved")

    if st.session_state["records"]:
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        st.bar_chart(df["Risk"].value_counts())
