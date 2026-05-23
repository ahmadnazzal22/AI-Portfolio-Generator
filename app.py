import os
from flask import Flask, render_template, request, jsonify
from generator import generate_portfolio

app = Flask(__name__)

@app.route("/")
def index():
    # الصفحة الرئيسية
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # استقبال البيانات من الفورم
    data = request.get_json()
    name   = data.get("name", "")
    field  = data.get("field", "")
    skills = data.get("skills", "")
    color  = data.get("color", "#00ff88")

    # التحقق إن الحقول مش فاضية
    if not name or not field or not skills:
        return jsonify({"error": "كل الحقول مطلوبة"}), 400

    # توليد الـ portfolio
    html_result = generate_portfolio(name, field, skills, color)
    return jsonify({"html": html_result})

if __name__ == "__main__":
    app.run(debug=True)