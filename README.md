# Rakta Sewa Django Project

## ⚠️ Python Version Requirement

**This project requires Python 3.8–3.12.**

- **Recommended:** Python 3.12 (see `runtime.txt`)
- **NOT supported:** Python 3.13 or newer (Django 3.2 does not support Python 3.13+)

If you use Python 3.13+, you will get errors like `ModuleNotFoundError: No module named 'cgi'`.

---

## Setup Instructions

1. **Install Python 3.12** (or 3.8–3.12)
2. **Create a virtual environment:**
   ```bash
   python3.12 -m venv .venv
   # or for Windows:
   py -3.12 -m venv .venv
   ```
3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Troubleshooting
- If you see `ModuleNotFoundError: No module named 'cgi'`, you are using Python 3.13+. Downgrade to Python 3.12 or lower.
- If you need help, contact the project maintainer. .....