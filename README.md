# MathSolver

#### Video Demo:  <https://youtu.be/d3QSmxZ9JoA>
#### Description:

Math Web App Solver | Flask + Python + SymPy
PROJECT OVERVIEW
MathSolve is a full-stack web application that solves math problems with
step-by-step explanations and interactive graphs. Built as a CS50 Final Project.
What it solves:
Arithmetic (PEMDAS/BODMAS)
Algebra (linear, quadratic, polynomials, factor, expand)
Calculus (derivatives, integrals, limits)
Statistics (mean, median, mode, variance, std dev)
Tech stack:
Backend:  Python, Flask, SQLite, SymPy, CS50 library
Frontend: HTML, CSS, JavaScript, Bootstrap 5, Chart.js, MathJax
Auth:     Flask-Session, Werkzeug password hashing
STEP-BY-STEP SETUP GUIDE
STEP 1 — Prerequisites
Make sure you have these installed:
Python 3.10 or higher
pip (Python package manager)
A terminal / command prompt
Check Python version:
python3 --version
STEP 2 — Download the Project
Option A: Download the ZIP from your submission and unzip it.
Option B: Clone from GitHub (if you uploaded it):
git clone https://github.com/yourusername/math-solver.git
Navigate into the folder:
cd math-solver
STEP 3 — Create a Virtual Environment (Recommended)
On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
On Windows:
python -m venv venv
venv\Scripts\activate
You should see (venv) appear in your terminal prompt.
STEP 4 — Install Dependencies
Code
This installs:
flask
flask-session
cs50
sympy
numpy
werkzeug
Wait for all packages to download and install.
STEP 5 — Run the Application
Code
You should see output like:
* Running on http://127.0.0.1:5000
* Debug mode: on
STEP 6 — Open in Browser
Open your browser and go to:
http://127.0.0.1:5000
The app will automatically create the SQLite database (math.db) on first run.
HOW TO USE THE APP
Solving Problems
Go to the home page
Select the problem type (or leave as "Auto Detect")
Type your math problem in the input box
Press "Solve" or hit Enter
See the result, step-by-step solution, and graph
Input Formats
Arithmetic:
25 * 4 + 100 / 5
2^10 - 50
sqrt(144)
Algebra:
x^2 - 5x + 6 = 0
2x + 5 = 11
factor x^2 - 9
expand (x+3)^2
simplify (x^2-1)/(x-1)
Derivatives:
derivative of x^3 + 2x^2 - 5x
d/dx sin(x) + cos(x)
differentiate x^2 * log(x)
Integrals:
integrate x^2 + 3x dx
integral of sin(x) dx
integrate e^x dx
Limits:
limit of sin(x)/x as x->0
lim (x^2-1)/(x-1) as x->1
limit of 1/x as x->inf
Statistics:
mean 4 7 13 2 1
median 3 7 9 1 5
std 10 20 30 40
mean median std variance 2 4 6 8 10
User Accounts
Register a free account at /register
Log in at /login
All solved problems are saved to your history at /history
You can re-solve any past problem from the history page
PROJECT FILE STRUCTURE
math-solver/
├── app.py              Main Flask application and routes
├── solver.py           Math engine (SymPy-powered)
├── requirements.txt    Python dependencies
├── math.db             SQLite database (auto-created)
├── README.md           This file
│
├── templates/
│   ├── layout.html     Base HTML template (navbar, footer)
│   ├── index.html      Main solver page
│   ├── history.html    Problem history page
│   ├── login.html      Login page
│   └── register.html   Registration page
│
└── static/
    ├── style.css       Complete stylesheet (dark theme)
    └── solver.js       Frontend JavaScript
Code
DATABASE SCHEMA
users table:
id        INTEGER  Primary key
username  TEXT     Unique username
hash      TEXT     Bcrypt password hash
history table:
id            INTEGER   Primary key
user_id       INTEGER   Foreign key to users
problem       TEXT      Original problem entered
problem_type  TEXT      Detected type (algebra, calculus, etc.)
result        TEXT      Final answer
steps         TEXT      JSON array of step-by-step strings
timestamp     DATETIME  When it was solved
CS50 REQUIREMENTS CHECKLIST
[x] Uses Python and Flask (backend)
[x] Uses SQL database (SQLite via CS50 library)
[x] Uses HTML/CSS/JavaScript (frontend)
[x] User authentication with hashed passwords
[x] Multiple pages (index, history, login, register)
[x] Forms with POST and GET methods
[x] Session management
[x] Original and complex enough to be a final project
[x] README with setup instructions
[x] Video demo (record separately with Loom or OBS)
VIDEO DEMO OUTLINE (2 minutes)
(0:00) Show the home page and hero UI
(0:20) Solve an arithmetic problem — show steps
(0:40) Solve a quadratic equation — show graph
(1:00) Compute a derivative — show f(x) and f'(x) on graph
(1:20) Show statistics solver
(1:35) Register an account, solve a problem, show history page
(1:50) Close with project summary
DESIGN DECISIONS
Why SymPy?
SymPy is a full computer algebra system — it solves equations symbolically,
not numerically. This means it gives exact answers like sqrt(2) rather than
1.4142135..., and can factor, expand, and differentiate symbolically.
Why Flask + CS50 library?
CS50's SQL library simplifies SQLite queries to one line each, which is
perfect for a course project where the focus is on learning, not boilerplate.
Why Chart.js?
Chart.js is lightweight, well-documented, and produces clean line graphs
directly in the browser without a backend rendering step.
AUTHOR
Name: Rukhsna Bibi
CS50 Username: RUKHSANABIBI25
City/Country: Mianwali/Pakistan
Date: April-26-2026
This was CS50. This is CS50.
