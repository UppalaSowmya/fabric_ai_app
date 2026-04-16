from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import json
import os

app = Flask(__name__)

# Set your API key
os.environ["OPENAI_API_KEY"] = "sk-7Z7x6vGg3frMzOCvc0QfeStwgI6qHheFrxxnW2pDSJQ7m2U1"
client = OpenAI()

def extract_details(text):
    prompt = f"""
    Extract fabric details from the sentence below.

    Sentence: "{text}"

    Extract:
    - fabric type (cotton, silk, polyester, etc.)
    - gsm (number only)
    - quantity (number only)
    - color
    - delivery time

    Return ONLY valid JSON:
    {{
        "fabric": "",
        "gsm": "",
        "quantity": "",
        "color": "",
        "delivery": ""
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content.strip()

        # Convert string → JSON
        return json.loads(result)

    except Exception as e:
        print("Error:", e)
        return {
            "fabric": "",
            "gsm": "",
            "quantity": "",
            "color": "",
            "delivery": ""
        }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    text = data.get("text", "")

    extracted = extract_details(text)
    return jsonify(extracted)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    print("DATA RECEIVED:", data)

    return render_template("summary.html", data=data) 

if __name__ == "__main__":
    app.run(debug=True)