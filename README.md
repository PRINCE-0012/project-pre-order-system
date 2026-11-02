# 🍔 Smart Campus Food Pre-Order System

> **Campus Canteen Food Pre-Order & Real-Time Queue Management Web Application**  
> Technology: **Python (Flask)**, **HTML5**, **CSS3**, **JavaScript**

---

## 📌 Dusre Ke Laptop Me Kaise Bhejein Aur Chalayein (Hinglish Guide)

Agar aapko ye project kisi friend, classmate ya teacher ke laptop me bhej kar chalana hai, toh niche diye steps follow karein:

---

### 📦 Step 1: Ye Folder Ya ZIP File Share Karein
Aap unhe ye poora folder ya fir is folder ki ZIP file **`Smart_Campus_Food_PreOrder.zip`** share kar sakte hain (WhatsApp, Pen Drive ya Google Drive se).

---

### 💻 Step 2: Unke Laptop Me Python Check Karein
Project chalane ke liye samne wale ke laptop me **Python** install hona zaroori hai.

1. Unke laptop me **CMD (Command Prompt)** khole aur type karein:
   ```cmd
   python --version
   ```
2. **Agar Python install nahi hai:**
   - Unhe bolo [https://www.python.org/downloads/](https://www.python.org/downloads/) se Python download karke install karein.
   - ⚠️ **Sabse Important:** Install karte waqt pehli screen par **`Add python.exe to PATH`** checkbox par zaroor tick lagayein!

---

### 🚀 Step 3: Project Run Kaise Karein (2 Simple Tareeqe)

#### 🌟 Tareeqa 1: Sirf 1-Click (Sabse Aasan)
1. Project folder open karein.
2. Usme **`run.bat`** naam ki file par **Double-Click** karein!
3. `run.bat` apne aap:
   - Python check karega.
   - Flask package khud install karega (agar pehle se nahi hai).
   - Server start karega.
   - Browser me **http://127.0.0.1:5000** apne aap open kar dega!
4. **Note:** Jo black CMD window khulegi, use band mat karna jab tak project use karna ho.

---

#### 🛠️ Tareeqa 2: Manual Terminal / CMD Se Run Karna
Agar kisi vajah se `run.bat` na chale, toh:
1. Project folder ke andar khali jagah par **Shift + Right Click** karein aur **"Open in Terminal"** ya **"Open PowerShell/Command Prompt here"** chunein.
2. Ye do commands ek-ek karke run karein:
   ```cmd
   pip install -r requirements.txt
   ```
   ```cmd
   python app.py
   ```
3. Terminal me message aayega:
   ```text
   ============================================================
    [OK] SMART CAMPUS FOOD PRE-ORDER SYSTEM RUNNING
    Access Web Interface at: http://127.0.0.1:5000
   ============================================================
   ```
4. Apne browser (Chrome / Edge / Firefox) me ye link open karein:  
   👉 **http://127.0.0.1:5000**

---

## 🖥️ Project Me Kya-Kya Open Karke Dekhna Hai (Demo Flow)

1. **Menu & 1-Click Order (`http://127.0.0.1:5000`)**:
   - Food items ke `+` button par click karein.
   - Real-time cart tray me live clock, orders queue count aur estimated pickup time dekhein.
   - ₹300 se zyada order par **10% Flat Campus Discount** calculate hoga.
   - **"Confirm & Generate Token"** button par click karein.

2. **Digital Token & Live Countdown (`/receipt/<token>`)**:
   - Turant digital token number (jaise `#1001`) generate hoga.
   - Second-by-second **Live Countdown Timer** dikhega (e.g. `14m 50s remaining`).
   - Yahan se **"Print Receipt"** button se receipt print kar sakte hain.

3. **Live Order Tracker (`/status`)**:
   - Kisi bhi time apna token daal kar track kar sakte hain ki order *Preparing* hai ya *Ready for Pickup*.
   - Page bina refresh kiye apne aap live sync hota hai!

4. **Kitchen / Canteen Live Display (`/admin`)**:
   - Canteen counter ke liye screen jahan staff live incoming orders dekh sakta hai aur token status update kar sakta hai.

---

## 📁 Project Folder Structure

```text
project prince/
│
├── app.py                  # Main Flask Web Server (Backend & Routes)
├── cli_app.py              # Original Terminal / CLI Version (Safe script)
├── requirements.txt        # Python Packages (Flask)
├── run.bat                 # 1-Click Auto-Setup & Launcher Script
├── README.md               # Ye instruction guide
│
├── templates/              # HTML Frontend Templates
│   ├── base.html           # Base Navbar, Layout & Footers
│   ├── index.html          # Menu, Real-Time Tray & Pre-Order
│   ├── receipt.html        # Digital Receipt with Live Countdown
│   ├── status.html         # Real-Time Order Tracking & Progress Bar
│   └── admin.html          # Kitchen Live Queue Management Dashboard
│
└── static/                 # Styles & Client Scripts
    ├── css/
    │   └── style.css       # Modern Campus Canteen Theme
    └── js/
        └── main.js         # Real-Time Ticking Clock, Queue Polling & Cart Calculations
```

---

## ❓ Frequently Asked Questions (Problems & Solutions)

- **Q: Browser me site nahi khul rahi?**  
  **Ans:** Check karein ki `run.bat` ya `python app.py` wali black CMD window open hai ya nahi. Agar band ho gayi ho toh dubara `run.bat` par click karein.

- **Q: Port 5000 already in use error?**  
  **Ans:** Agar pehle se koi purani python window chal rahi ho, toh use task manager se ya window close karke band karein aur dubara `run.bat` chalayein.
