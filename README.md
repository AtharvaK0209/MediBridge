💊 MediBridge — Expired Medicine Redistribution Platform

> **Reduce medicine wastage by connecting pharmacies and NGOs for safe, responsible redistribution.**

MediBridge is a full-stack web application that helps pharmacies manage near-expiry and expired medicine inventory, while enabling NGOs to discover and request available medicines for redistribution. The platform features a modern glassmorphism UI with light/dark theme support, secure authentication, automated email alerts, and a clean REST API architecture.

---

✨ Features

🎨 Frontend / UI
- **Light & Dark Mode** — Theme toggle with `localStorage` persistence; switches instantly across all pages
- **Glassmorphism Design** — Translucent cards with backdrop blur, subtle shadows, and smooth hover animations
- **Modern Typography** — Powered by [Inter](https://fonts.google.com/specimen/Inter) via Google Fonts
- **Responsive Layout** — Built on Bootstrap 5.3 with custom CSS overrides for a premium feel
- **Micro-Animations** — Fade-ins, floating hero backgrounds, alert slide-ins, button shimmer effects, and card lift-on-hover
- **Status Badges** — Color-coded pill badges for medicine status (`SAFE`, `NEAR_EXPIRY`, `EXPIRED`) and request status (`PENDING`, `APPROVED`, `REJECTED`)
- **Toast Notifications** — Non-intrusive popup feedback for user actions

🔐 Authentication & Security
- **Secure Password Hashing** — Uses `werkzeug.security` (`generate_password_hash` / `check_password_hash`) — no plaintext passwords stored
- **Role-Based Access** — Separate dashboards and workflows for **Pharmacy** and **NGO** users
- **Input Validation** — Server-side validation on all API endpoints

💊 Pharmacy Features
- Add medicines with automatic expiry status detection (`SAFE` / `NEAR_EXPIRY` / `EXPIRED`)
- View and manage full medicine inventory sorted by expiry date
- Delete medicines from inventory
- Review, approve, or reject redistribution requests from NGOs
- Stock validation before approving requests (prevents over-dispensing)
- Transaction logging on approved requests

🏥 NGO Features
- Browse all available (non-expired, in-stock) medicines across pharmacies
- Browse pharmacies and view per-pharmacy medicine listings
- Submit redistribution requests with quantity validation
- Track request history and status updates
- Dashboard stats: total requests and approved count (optimized single-query)

📧 Email Alerts
- Automated expiry alert emails sent to pharmacies via Gmail SMTP
- Notifications include counts of expired and near-expiry medicines

⚙️ Backend
- **Blueprint-based routing** — Clean separation: `auth`, `pharmacy`, `ngo` route modules under `/api/`
- **Centralized error handling** — Global `404` and `500` JSON error handlers
- **Environment-configurable** — Database credentials and email settings via environment variables with sensible defaults

---

🗂️ Project Structure

```
MediBridge/
├── 📄 README.md
├── 📄 requirements.txt
│
├── 📁 backend/
│   ├── 📄 app.py                  # Flask app entry point, page routes, blueprint registration
│   ├── 📄 database.py             # MySQL connection helper (env-configurable)
│   ├── 📄 email_service.py        # SMTP email alert service
│   │
│   ├── 📁 routes/                 # API Blueprints
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth.py             # /api/register, /api/login
│   │   ├── 📄 pharmacy.py         # /api/add-medicine, /api/get-medicines, etc.
│   │   └── 📄 ngo.py              # /api/available-medicines, /api/request-medicine, etc.
│   │
│   ├── 📁 templates/              # Jinja2 HTML templates
│   │   ├── 📄 index.html          # Landing / home page
│   │   ├── 📄 login.html          # Login form
│   │   ├── 📄 register.html       # Registration form
│   │   ├── 📄 pharmacy_dashboard.html
│   │   ├── 📄 pharmacy_requests.html
│   │   ├── 📄 ngo_dashboard.html
│   │   ├── 📄 ngo_requests.html
│   │   └── 📄 add_medicine.html
│   │
│   └── 📁 static/
│       └── 📁 css/
│           └── 📄 custom.css      # Full design system (light/dark, glassmorphism, components)
│
├── 📁 database/                   # (MySQL schema / migration scripts)
└── 📁 venv/                       # Python virtual environment (not committed)
```

---

🛠️ Tech Stack

| Layer        | Technology                                              |
| ------------ | ------------------------------------------------------- |
| **Backend**  | Python 3, Flask 3.1, Jinja2 3.1                        |
| **Database** | MySQL (via `mysql-connector-python 9.5`)                |
| **Security** | Werkzeug 3.1 (`generate_password_hash` / `check_password_hash`) |
| **Frontend** | HTML5, CSS3 (custom design system), JavaScript (vanilla)|
| **UI Framework** | Bootstrap 5.3.2 (CDN)                              |
| **Fonts**    | Google Fonts — Inter                                    |
| **Email**    | Python `smtplib` (Gmail SMTP with app passwords)        |

---

🔌 API Routes

All data endpoints are prefixed with `/api/` and return JSON. Page routes serve HTML templates.

📄 Page Routes (GET — serve HTML)

| Route                    | Description                |
| ------------------------ | -------------------------- |
| `/` or `/home`           | Landing page               |
| `/register-page`        | Registration form          |
| `/login-page`           | Login form                 |
| `/pharmacy-dashboard`   | Pharmacy inventory dashboard |
| `/ngo-dashboard`        | NGO browsing dashboard     |
| `/pharmacy-requests-page` | Pharmacy request management |
| `/ngo-requests-page`    | NGO request tracking       |

🔐 Auth API

| Method | Endpoint         | Description                        |
| ------ | ---------------- | ---------------------------------- |
| POST   | `/api/register`  | Register a new pharmacy or NGO user |
| POST   | `/api/login`     | Authenticate and return role + user ID |

💊 Pharmacy API

| Method | Endpoint                              | Description                              |
| ------ | ------------------------------------- | ---------------------------------------- |
| POST   | `/api/add-medicine`                   | Add a medicine with auto-status detection |
| GET    | `/api/get-medicines/<user_id>`        | Get all medicines for a pharmacy (+ email alert) |
| DELETE | `/api/delete-medicine/<medicine_id>`  | Delete a medicine by ID                  |
| GET    | `/api/pharmacy-requests/<user_id>`    | Get redistribution requests for a pharmacy |
| POST   | `/api/update-request`                 | Approve or reject a request (with stock validation) |

🏥 NGO API

| Method | Endpoint                                | Description                            |
| ------ | --------------------------------------- | -------------------------------------- |
| GET    | `/api/available-medicines`              | List all available (non-expired, in-stock) medicines |
| POST   | `/api/request-medicine`                 | Submit a redistribution request         |
| GET    | `/api/ngo-stats/<user_id>`              | Get request stats for an NGO            |
| GET    | `/api/pharmacies`                       | List all registered pharmacies          |
| GET    | `/api/pharmacy-medicines/<pharmacy_id>` | List medicines for a specific pharmacy  |
| GET    | `/api/my-requests/<user_id>`            | Get an NGO's request history            |

---

🚀 Installation & Setup

Prerequisites

- **Python 3.10+** installed
- **MySQL Server** installed and running
- **Git** (optional, for cloning)

1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/MediBridge.git
cd MediBridge
```

2️⃣ Create & Activate a Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows — PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows — CMD)
.\venv\Scripts\activate.bat

# Activate (macOS / Linux)
source venv/bin/activate
```

3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

4️⃣ Set Up the MySQL Database

Connect to your MySQL server and create the database:

```sql
CREATE DATABASE expired_medicine_db;
USE expired_medicine_db;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('pharmacy', 'ngo') NOT NULL
);

-- Pharmacy table
CREATE TABLE pharmacy (
    pharmacy_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pharmacy_name VARCHAR(100),
    address VARCHAR(255),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- NGO table
CREATE TABLE ngo (
    ngo_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ngo_name VARCHAR(100),
    address VARCHAR(255),
    contact VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Medicines table
CREATE TABLE medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    pharmacy_id INT NOT NULL,
    medicine_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    expiry_date DATE NOT NULL,
    original_price DECIMAL(10,2),
    discount_price DECIMAL(10,2),
    status ENUM('SAFE', 'NEAR_EXPIRY', 'EXPIRED') DEFAULT 'SAFE',
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacy(pharmacy_id)
);

-- Redistribution requests table
CREATE TABLE redistribution_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT NOT NULL,
    ngo_id INT NOT NULL,
    requested_quantity INT NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
    FOREIGN KEY (ngo_id) REFERENCES ngo(ngo_id)
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT NOT NULL,
    ngo_id INT NOT NULL,
    quantity INT NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
    FOREIGN KEY (ngo_id) REFERENCES ngo(ngo_id)
);
```

5️⃣ Configure Environment Variables *(optional)*

The app uses sensible defaults, but you can override them with environment variables:

```bash
# Database (defaults shown)
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=your_mysql_password
set DB_NAME=expired_medicine_db

# Email alerts (defaults shown)
set MAIL_SENDER=your_email@gmail.com
set MAIL_APP_PASSWORD=your_app_password
```

> 💡 **Tip:** For Gmail, generate an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

6️⃣ Run the Flask Server

```bash
cd backend
python app.py
```

The server will start at **http://127.0.0.1:5000** 

Open your browser and navigate to `http://localhost:5000` to see the landing page.

---

🖥️ Screenshots

| Light Mode 🌞 | Dark Mode 🌙 |
|---|---|
| Clean, bright interface with greenish-white gradients | Sleek dark UI with glowing emerald accents |

> *Toggle the theme anytime using the 🌙 / ☀️ button in the navbar.*

---

📌 Environment Defaults

| Variable           | Default Value          |
| ------------------ | ---------------------- |
| `DB_HOST`          | `localhost`            |
| `DB_USER`          | `root`                 |
| `DB_PASSWORD`      | *(set in database.py)* |
| `DB_NAME`          | `expired_medicine_db`  |
| `MAIL_SENDER`      | *(set in email_service.py)* |
| `MAIL_APP_PASSWORD` | *(set in email_service.py)* |

---

🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

📜 License

This project is developed for educational purposes.

---

<p align="center">
  Made with ❤️ by <strong>Team MediBridge</strong> · © 2026
</p>
