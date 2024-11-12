from flask import Flask, render_template, request, jsonify
import pandas as pd
from rapidfuzz import process

app = Flask(__name__)

file_path = 'assets/ecri_equipment_assets.xlsx'
try:
    ecri_data = pd.read_excel(file_path, sheet_name='UMDNS__Alpha_Pref_Concept_Lis')
    print("Excel data loaded successfully.")
except Exception as e:
    print("Error loading Excel file:", e)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    equipment_type = request.form.get('equipment_type')
    print("Received equipment type:", equipment_type)

    matches = process.extract(
        equipment_type,
        ecri_data['Device Name'],
        limit=10
    )

    results = []
    for match in matches:
        device_name, confidence = match[0], match[1]
        device_code = ecri_data[ecri_data['Device Name'] == device_name]['Device Code'].values[0]
        results.append({
            "device_code": device_code,
            "equipment_type": device_name,
            "confidence": confidence
        })
    
    print("Search results:", results)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
