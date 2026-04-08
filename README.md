# AI-Phishing-Extension
AI Phishing Detection Extension is a browser extension that detects and warns users about malicious or phishing websites. It analyzes URLs and page content in real time using AI-based logic to identify threats and alert users, helping prevent scams, data theft, and unsafe browsing.

---

## 🚀 Features

* 🔍 Real-time URL and webpage analysis
* 🤖 AI-based phishing detection
* ⚠️ Instant alerts for suspicious sites
* 🌐 Lightweight and fast
* 🔐 Enhances safe browsing

---

## 🛠️ Tech Stack

* JavaScript
* HTML & CSS
* Python (Model + API)
* FastAPI
* Browser Extension APIs

---

## 📂 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Phishing-Extension.git
cd AI-Phishing-Extension
```

---

## ▶️ How to Run

### 🔹 Step 1: Train the Model

```bash
python Train_model.py
```

---

### 🔹 Step 2: Start the Backend Server

```bash
uvicorn app:app --reload
```

---

### 🔹 Step 3: Load the Extension

* Open Chrome → `chrome://extensions/`
* Enable **Developer Mode**
* Click **Load unpacked**
* Select the project folder

---

### 🔹 Step 4: Reload Extension (after backend starts)

* Go to Extensions page
* Click **Reload** on your extension

---

## ▶️ Usage

* Open any website
* The extension sends data to the backend
* AI model analyzes it
* If phishing is detected → warning shown ⚠️

---

## 📌 Project Structure (example)

```
ai-phishing-extension/
│── Train_model.py
│── app.py
│── manifest.json
│── background.js
│── content.js
│── popup.html
│── popup.js
│── styles.css
```

---

