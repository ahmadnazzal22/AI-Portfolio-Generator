# 🤖 AI Portfolio Generator

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-1.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/Powered%20By-Groq%20Cloud-00ff88?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An intelligent, lightweight web application that leverages the ultra-fast **Groq API (Llama 3.3 70B)** to dynamically architect and generate complete, modern, single-page portfolio websites in seconds. 

Input your professional details, pick your signature accent color, and let the AI handle the typography, responsiveness, and layout.

---

## ✨ Key Features

*   ⚡ **Lightning Fast Generation:** Powered by `llama-3.3-70b-versatile` via Groq, delivering optimized code production within milliseconds.
*   🎨 **Dynamic Accent Theming:** Seamlessly injects user-selected hex colors into the generated CSS variable architecture.
*   👁️ **Sandboxed Live Preview:** Features an instant code injector utilizing an `iframe` with `srcdoc` for safe, real-time feedback.
*   💾 **One-Click Export:** Instantly download the standalone `portfolio.html` file or copy the raw text straight to your clipboard.
*   🌌 **Cyberpunk Tech Aesthetic:** Designed with a sleek, minimalist dark theme focused on scannability and clean layout structures.
*   🌐 **Bi-directional Support:** Engineered prompts ensure the AI handles both English and Arabic typographic layouts natively.

---

## 🛠️ Tech Stack & Architecture


```
portfolio-generator/
├── app.py               # Flask Web Server & API Gateways
├── generator.py         # Groq LLM Client Orchestration
├── templates/
│   └── index.html       # Single Page Application (SPA) UI
├── .env                 # Protected Environment Variables
└── requirements.txt     # Python Engine Dependencies
```

*   **Backend Backend Engine:** Python 3.x / Flask (RESTful Endpoints)
*   **Inference Pipeline:** Groq Cloud SDK (`Llama-3.3-70B`)
*   **Frontend Client:** Semantic HTML5, Custom CSS3 Utilities, and Asynchronous Vanilla JS (`Fetch API`).

---

## 🚀 Quick Start (Local Deployment)

### 1. Clone & Navigate
```bash
git clone [https://github.com/your-username/portfolio-generator.git](https://github.com/your-username/portfolio-generator.git)
cd portfolio-generator

```
### 2. Environment Setup
Initialize your dependencies within a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

```
### 3. API Authentication
Create a .env file in the root directory and inject your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_high_speed_groq_key_here

```
### 4. Fire It Up
Ensure the environment handles standard encodings properly and run the server:
```bash
# Windows PowerShell
$env:PYTHONIOENCODING = "utf-8"
python app.py

```
Open your browser and navigate to: http://127.0.0.1:5000 🚀
## 🦾 System Prompt Architecture
The engine works by isolating the LLM from generating markdown clutter and forcing it to act strictly as an executive compiler. It requests:
 * Fully encapsulated CSS inside a <style> block.
 * A strict **Dark Theme UI** with smooth CSS layout animations.
 * Structured sections: *Hero, About, Skills, and Contact*.
 * Zero markdown wrapper backticks (```html) to maintain smooth iframe injection.
## 📜 License
Distributed under the **MIT License**. See LICENSE for more information.

