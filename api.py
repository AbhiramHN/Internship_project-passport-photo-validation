from flask import Flask, request, jsonify
from pipeline.validation_pipeline import run_validation
import os

# ✅ DEFINE APP FIRST
app = Flask(__name__)

@app.route('/')
def home():
    return "Passport API Running 🚀"

@app.route('/validate', methods=['POST'])
def validate():
    try:
        file = request.files['file']

        # 🔥 Save uploaded image
        file_path = "temp.jpg"
        file.save(file_path)

        # ✅ Run validation
        result = run_validation(file_path)

        print("DEBUG RESULT:", result)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ RUN APP
if __name__ == '__main__':
    app.run(debug=True)