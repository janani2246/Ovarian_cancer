from flask import Flask, request, render_template_string
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

# IMPORTANT: Match your dataset columns exactly
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
    <style>
    body {text-align:center; font-family:Arial;}
    button {padding:15px; margin:20px; border-radius:10px; border:none;}
    .p {background:pink;}
    .d {background:blue;color:white;}
    </style>

    <h1>Ovarian Cancer App</h1>
    <a href="/patient"><button class="p">Patient</button></a>
    <a href="/doctor"><button class="d">Doctor</button></a>
    """)

# ================= PATIENT =================
@app.route('/patient')
def patient():
    return render_template_string("""
    <h2>Patient Options</h2>
    <a href="/predict_form"><button>Predict Risk</button></a><br><br>
    <a href="/care_plan"><button>Care Plan</button></a>
    """)

# ================= FORM =================
@app.route('/predict_form')
def predict_form():
    return render_template_string("""
    <form action="/predict" method="post">

    Age: <input name="age"><br><br>

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

    <br><button>Predict</button>
    </form>
    """)

# ================= FIXED PREDICT =================
@app.route('/predict', methods=['POST'])
def predict():

    data_dict = {}

    # basic inputs
    data_dict['age'] = int(request.form['age'])
    data_dict['menopause'] = int(request.form['menopause'])
    data_dict['family_history'] = int(request.form['family_history'])

    # symptoms
    for i in range(1,13):
        data_dict[f'symptom{i}'] = 1 if request.form.get(f'symptom{i}') == 'on' else 0

    # correct order input
    input_data = [data_dict[col] for col in columns]
    input_data = np.array(input_data).reshape(1,-1)

    pred = model.predict_proba(input_data)[0][1]*100

    if pred < 30:
        level = "Low"
        color = "green"
        msg = "You are healthy 👍"
    elif pred < 70:
        level = "Medium"
        color = "orange"
        msg = "Consult doctor"
    else:
        level = "High"
        color = "red"
        msg = "Immediate action required!"

    return render_template_string(f"""
    <h2 style="color:{color}">{level}</h2>
    <h3>{round(pred,2)}%</h3>
    <p>{msg}</p>
    <a href="/">Home</a>
    """)

# ================= CARE PLAN =================
@app.route('/care_plan', methods=['GET','POST'])
def care_plan():
    if request.method == 'POST':
        name = request.form['name']

        return render_template_string(f"""
        <h2>Care Plan for {name}</h2>

        <ul>
        <li>7-8 AM: Exercise</li>
        <li>9-10 AM: Breakfast</li>
        <li>1-2 PM: Lunch</li>
        <li>7-8 PM: Dinner</li>
        </ul>

        <a href="/">Home</a>
        """)

    return render_template_string("""
    <form method="post">
    Name: <input name="name"><br><br>
    <button>Generate</button>
    </form>
    """)

# ================= DOCTOR =================
@app.route('/doctor', methods=['GET','POST'])
def doctor():
    if request.method == 'POST':
        return "<h2>Saved</h2><a href='/'>Home</a>"

    return render_template_string("""
    <h2>Doctor Dashboard</h2>
    <form method="post">
    Doctor Name: <input><br><br>
    <button>Save</button>
    </form>
    """)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
