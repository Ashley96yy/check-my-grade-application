# Check My Grade (CLI)

A tiny, reproducible CLI app for **grade tracking** with **role-based access** (admin / professor / student) and **password obfuscation** (simple Caesar cipher for demo purposes).  
All data are **synthetic** and generated locally.

## Features
- **Roles & menus:** admin, professor, student — each with its own actions (view, add/delete/modify, reports).
- **Synthetic dataset:** quick generator creates students, professors, courses, grades, and login files.
- **CSV-backed storage:** reads/writes simple CSV files; runs anywhere with Python.
- **Credentials:** passwords stored with a basic Caesar shift (for learning only, **not secure**).

## Quickstart
```bash
# 1) Python 3.9+ recommended
# 2) Install minimal deps
pip install pandas faker

# 3) Generate sample data (creates Course.csv, Student.csv, Professor.csv, Grades.csv,
#    and login files: Login.csv (obfuscated) and Login_decrypted.csv (plaintext))
python data_simulate.py

# 4) Run the app
python main.py

First login: open Login_decrypted.csv, pick any row (email + role + plaintext password), and sign in at the prompt.
The app verifies against the obfuscated Login.csv.

## Repository layout
data_simulate.py   # one-click data generator (CSV files)
main.py            # entry point; login + role-specific menus
login_user.py      # login / change-password logic (reads Login.csv)
encdyc.py          # simple Caesar cipher (educational)
common.py          # domain classes & CSV helpers (students, professors, courses, grades)

## Notes
This is a local demo for learning workflows (data generation → access control → basic reporting).
No confidential or real data. The Caesar cipher is for demonstration only.
If you prefer zero extra packages, only pandas is required at runtime; faker is used to generate sample data.

## License
MIT
