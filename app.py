import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF

# 👉 NEW IMPORTS (for location)
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

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

        # ✅ SESSION FIX
        if "show_location" not in st.session_state:
            st.session_state.show_location = False

        if st.button("🔍 Predict Risk"):

            symptoms["Menstrual"] = menstrual_value
            symptoms["Menopause"] = menopause_value
            symptoms["Family"] = family_value

            risk_score = sum([int(v) for v in symptoms.values()])

            if risk_score >= 3:
                st.error("🔴 High Risk")
                st.session_state.show_location = True
            elif risk_score >= 2:
                st.warning("🟠 Medium Risk")
                st.session_state.show_location = True
            else:
                st.success("🟢 Low Risk")
                st.session_state.show_location = False

            st.write(f"Score: {risk_score}/12")

        # ================= LOCATION =================
        if st.session_state.show_location:

            st.subheader("🏥 Nearby Hospitals (Recommended)")
            st.warning("⚠️ Please consult a doctor")

            location_input = st.text_input(
                "📍 Enter Your Area",
                placeholder="Eg: Urapakkam / Pallavaram"
            )

            if st.button("📍 Show Hospitals"):

                if location_input:

                    geolocator = Nominatim(user_agent="health_app")
                    location = geolocator.geocode(f"{location_input}, India", addressdetails=True)

                    if location:
                        lat, lon = location.latitude, location.longitude

                        # ✅ Extract Area / City / State
                        address = location.raw.get("address", {})

                        area = address.get("suburb") or address.get("village") or address.get("town") or location_input
                        city = address.get("city") or address.get("county") or address.get("state_district") or "Unknown City"
                        state = address.get("state") or "Unknown State"

                        st.success(f"📍 Area: {area}")
                        st.info(f"🏙 City: {city}")
                        st.info(f"🌍 State: {state}")

                        # OSM API
                        url = "http://overpass-api.de/api/interpreter"
                        query = f"""
                        [out:json];
                        node["amenity"="hospital"](around:5000,{lat},{lon});
                        out;
                        """

                        response = requests.get(url, params={'data': query})
                        data = response.json()

                        hospitals = []

                        for e in data.get("elements", []):
                            name = e.get("tags", {}).get("name", "Unknown Hospital")
                            hospitals.append((name, e["lat"], e["lon"]))

                        if hospitals:
                            st.subheader("🏥 Hospitals Near You")

                            # Map
                            map_data = pd.DataFrame(
                                [(lat, lon)] + [(h[1], h[2]) for h in hospitals[:10]],
                                columns=["lat", "lon"]
                            )
                            st.map(map_data)

                            # Hospital cards
                            for h in hospitals[:5]:
                                name, h_lat, h_lon = h
                                dist = round(geodesic((lat, lon), (h_lat, h_lon)).km, 2)

                                map_link = f"https://www.google.com/maps?q={h_lat},{h_lon}"

                                st.markdown(f"""
                                <div style="border:1px solid #ddd; padding:12px; border-radius:10px; margin-bottom:10px;">
                                <b>🏥 {name}</b><br>
                                📍 Area: {area}<br>
                                🏙 City: {city}<br>
                                🌍 State: {state}<br>
                                📏 Distance: {dist} km<br>
                                <a href="{map_link}" target="_blank">📌 Open in Google Maps</a>
                                </div>
                                """, unsafe_allow_html=True)

                        else:
                            st.warning("No hospitals found nearby")

                    else:
                        st.error("❌ Location not found")

                else:
                    st.warning("⚠️ Please enter location")

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

    if st.session_state["records"]:
        df = pd.DataFrame(st.session_state["records"])
        st.dataframe(df)

        st.download_button("⬇ Download Patients CSV", df.to_csv(index=False), "patients.csv")

        st.bar_chart(df["Risk"].value_counts())
