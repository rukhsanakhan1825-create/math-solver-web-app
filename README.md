# MathSolve — Math Problem Solver Web App

A full-stack web application that solves mathematical problems and displays step-by-step solutions with interactive graphs. Developed as a CS50 Final Project.

**Video Demo:** https://youtu.be/d3QSmxZ9JoA

## Features

- **Arithmetic:** expressions evaluated using order of operations
- **Algebra:** linear and quadratic equations, factoring and expansion
- **Calculus:** derivatives, integrals and limits
- **Statistics:** mean, median, variance and standard deviation
- **Step-by-step solutions** for every problem
- **Interactive graphs** of functions and derivatives (Chart.js)
- **User accounts** with secure password hashing
- **Problem history** saved for each user (SQLite)

## Technologies

| Area | Tools |
|---|---|
| Backend | Python, Flask, SymPy, SQLite |
| Frontend | HTML, CSS, JavaScript, Bootstrap, Chart.js, MathJax |
| Security | Flask-Session, Werkzeug password hashing |

## Project Structure

```
MathSolve/
├── app.py            # Flask routes and database logic
├── solver.py         # Math engine (SymPy)
├── requirements.txt  # Python dependencies
├── templates/        # HTML pages (layout, index, login, register, history)
└── static/           # JavaScript, icons and PWA files
```

## How to Run

```bash
git clone https://github.com/Rukhsanabibi/MathSolve.git
cd MathSolve
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. The database (`math.db`) is created automatically on the first run.

## Example Inputs

```
25 * 4 + 100 / 5
x^2 - 5x + 6 = 0
factor x^2 - 9
derivative of x^3 + 2x
integrate x^2 dx
mean 4 7 13 2 1
```

## Author

Rukhsana Bibi — Mianwali, Pakistan
CS50 Final Project, Harvard University
