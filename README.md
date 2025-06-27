# 🎬 SDDAP_Proje

A lightweight web application built with **FastAPI**, **Jinja2**, and **SQLite** that allows users to register, log in, and review movies. This project is structured for scalability and educational purposes, focusing on modular design, user authentication, and film-based interactions.

---

## 🚀 Features

- 🔐 User registration & login system
- 🏠 Homepage with dynamic movie listings
- 📽️ Movie detail pages with user-specific ratings
- 💬 Commenting system for logged-in users
- 📁 Modular architecture using FastAPI routers
- 🗄️ SQLite database integration

---

## 🧱 Project Structure

```
SDDAP_Proje/
├── app.py                     # Main application entry point
├── auth/                     # Login, signup, logout logic
│   └── router.py
├── film/                     # Film details, listing, adding
│   └── router.py
├── comments/                 # Comment and rating routes
│   └── router.py
├── templates/                # Jinja2 HTML templates
│   └── login.html, homepage.html, film_detail.html, etc.
├── static/                   # CSS, JS, images
├── database/                # Database connection & models
│   └── db.py
└── README.md                 # This file
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sejinima/SDDAP_Proje.git
cd SDDAP_Proje
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Eğer `requirements.txt` yoksa, başlıca ihtiyaçlar şunlardır:
```bash
pip install fastapi uvicorn jinja2 sqlite3
```

---

## ▶️ Run the Application

```bash
uvicorn app:app --reload
```

Then open your browser and go to:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Roadmap / Planned Improvements

- [ ] Admin panel for managing films and users
- [ ] Film poster upload feature
- [ ] Ratings chart per film
- [ ] OAuth (Google, GitHub) login support
- [ ] Dockerization for deployment

---

## 🧪 Tech Stack

- **Backend:** FastAPI
- **Frontend:** HTML + CSS (Jinja2 Templates)
- **Database:** SQLite
- **Authentication:** Session-based login system

---

## 🤝 Contributing

Contributions, pull requests, and issues are welcome!  
Please open an issue or fork the repository to get started.

---

## 📝 License

This project is licensed under the MIT License.

---

## ✍️ Authors

Developed by:
- **[@sejinima](https://github.com/sejinima)**
- **[@tariccc](https://github.com/tariccc)**
- **[@NerdSlayer1](https://github.com/NerdSlayer1)**
