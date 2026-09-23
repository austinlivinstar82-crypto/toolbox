# Flask Invoice Generator & Financial Tooling App

A lightweight, production-ready Flask web application designed for dynamic invoice generation, tax calculation, and PDF/print formatting.

## Features
- **Dynamic Calculation Engine:** Computes line item totals, subtotals, configurable tax rates, and grand totals automatically.
- **Defensive Input Handling:** Built-in error fallback handling for user input types and form parameters.
- **Print & PDF Export:** Integrated Tailwind CSS stylesheet with native `@media print` styling for clean document printing.
- **Production Ready:** Configured for local debugging and deployment via `gunicorn`.

## Tech Stack
- **Backend:** Python 3.8+, Flask 3.0
- **Frontend:** HTML5, Jinja2 Templating, Tailwind CSS
- **WSGI Server:** Gunicorn 21.2

## Project Structure
```text
toolbox/
├── app.py              # Core Flask application & calculation routes
├── fix.py              # Environment setup & template generator script
├── requirements.txt    # Python dependencies (Flask, Gunicorn)
└── templates/
    ├── index.html      # Invoice creation form
    └── invoice.html    # Generated invoice template & print view
```

## Getting Started

### Prerequisites
Python 3.8 or higher

### Local Setup
Clone the repository:
```bash
git clone https://github.com/austinlivinstar82-crypto/toolbox.git
cd toolbox
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the application:
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.
