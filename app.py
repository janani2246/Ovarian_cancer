from flask import Flask, request, render_template_string
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

columns = [
    'age','menopause','family_history',
    'symptom1','symptom2','symptom3','symptom4',
    'symptom5','symptom6','symptom7','symptom8',
    'symptom9','symptom10','symptom11','symptom12'
]

# ================= HOME =================
@app.route('/')
def home():
    return render_template_string("""
    <h1>Ovarian Cancer App</h1>
    <a href="/patient"><button style="background:pink">Patient</button></a>
    <a href="/doctor"><button style="background:blue;color:white">Doctor</button></a>
    """)

# ================= PATIENT MENU =================
@app.route('/patient')
def patient():
    return render_template_string("""
    <h2>Patient Options</h2>

    <a href="/predict_form"><button>Option 1: Predict Risk</button></a><br><br>

    <a href="/care_plan"><button>Option 2: Cancer Confirmed Care Plan</button></a>
    """)

# ================= OPTION 1 =================
@app.route('/predict_form')
def predict_form():
    return render_template_string("""
    <h2>Prediction</h2>
    <form action="/predict" method="post">

    Age: <input type="number" name="age"><br><br>

    Menopause:
    <select name="menopause">
      <option value="1">Yes</option>
      <option value="0">No</option>
    </select><br><br>

    Family History:
    <select name="family_history">
      <option value="1">Yes</option>
      <option value="0">No</option>
    </select><br><br>

    <h3>Symptoms</h3>
    {% for i in range(1,13) %}
    <input type="checkbox" name="symptom{{i}}"> Symptom {{i}}<br>
    {% endfor %}

    <br><button type="submit">Predict</button>
    </form>
    """)

@app.route('/predict', methods=['POST'])
def predict():
    data = []

    data.append(int(request.form['age']))
    data.append(int(request.form['menopause']))
    data.append(int(request.form['family_history']))

    for i in range(1,13):
        val = request.form.get(f'symptom{i}')
        data.append(1 if val == 'on' else 0)

    data = np.array(data).reshape(1,-1)

    pred = model.predict_proba(data)[0][1]*100

    if pred < 30:
        level = "Low"
        color = "green"
    elif pred < 70:
        level = "Medium"
        color = "orange"
    else:
        level = "High"
        color = "red"

    return render_template_string(f"""
    <h2 style="color:{color}">{level} Risk</h2>
    <h3>{round(pred,2)}%</h3>
    <a href="/">Home</a>
    """)

# ================= OPTION 2 =================
@app.route('/care_plan', methods=['GET','POST'])
def care_plan():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        risk = request.form['risk']

        return render_template_string(f"""
        <h2>Care Plan for {name}</h2>
        <p>Age: {age}</p>
        <p>Risk Level: {risk}</p>
        <p>Phone: {phone}</p>

        <h3>📅 Daily Timetable</h3>
        <ul>
        <li>7-8 AM: Exercise</li>
        <li>9-10 AM: Breakfast + Medicine</li>
        <li>1-2 PM: Lunch + Medicine</li>
        <li>7-8 PM: Dinner + Medicine</li>
        <li>Drink Water Frequently</li>
        </ul>

        <h3>🥗 Diet Plan</h3>
        <ul>
        <li>Fruits & Vegetables</li>
        <li>Avoid Junk Food</li>
        <li>Low Oil Diet</li>
        </ul>

        <h3>🔔 Alerts</h3>
        <p>Reminder: Breakfast time (9-10 AM)</p>
        <p>Reminder: Lunch time (1-2 PM)</p>
        <p>Reminder: Dinner time (7-8 PM)</p>

        <a href="/">Home</a>
        """)

    return render_template_string("""
    <h2>Cancer Confirmed Care Plan</h2>

    <form method="post">
    Patient Name: <input type="text" name="name"><br><br>
    Age: <input type="number" name="age"><br><br>
    Phone: <input type="text" name="phone"><br><br>

    Risk Level:
    <select name="risk">
    <option>High</option>
    <option>Medium</option>
    </select><br><br>

    <button type="submit">Generate Plan</button>
    </form>
    """)

# ================= DOCTOR =================
@app.route('/doctor', methods=['GET','POST'])
def doctor():
    if request.method == 'POST':
        doc = request.form['doc']
        patient = request.form['patient']
        meds = request.form['meds']

        return render_template_string(f"""
        <h2>Doctor Record</h2>
        <p>Doctor: {doc}</p>
        <p>Patient: {patient}</p>
        <p>Medicines: {meds}</p>
        <a href="/">Home</a>
        """)

    return render_template_string("""
    <h2>Doctor Dashboard</h2>
    <form method="post">
    Doctor Name: <input name="doc"><br><br>
    Patient Name: <input name="patient"><br><br>
    Medicines: <input name="meds"><br><br>
    <button>Save</button>
    </form>
    """)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
