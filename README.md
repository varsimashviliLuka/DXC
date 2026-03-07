# DXC.GE – Digital X Control

Flask web application for DXC.GE security services.

## Project Structure

```
dxc/
├── run.py                   # Entry point
├── config.py                # Dev / Prod / Test configs
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py          # App factory (create_app)
    ├── errors.py            # 404 / 500 handlers
    ├── routes/
    │   ├── main.py          # / and /about
    │   ├── services.py      # /services/*
    │   └── contact.py       # /contact  (GET + POST)
    ├── templates/
    │   ├── base.html        # Shared layout, navbar, footer
    │   ├── index.html       # Homepage
    │   ├── about.html
    │   ├── services.html
    │   ├── service_detail.html
    │   ├── contact.html
    │   └── errors/
    │       ├── 404.html
    │       └── 500.html
    └── static/
        ├── css/style.css
        ├── js/main.js
        └── img/             # Place logo/images here
```

## Quick Start

```bash
# 1. Clone / unzip the project
cd dxc

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and edit environment variables
cp .env.example .env

# 5. Run the development server
python run.py
```

The site will be available at **http://localhost:5000**

## Routes

| URL                  | Blueprint  | Description          |
|----------------------|------------|----------------------|
| `/`                  | main       | Homepage             |
| `/about`             | main       | About page           |
| `/services/`         | services   | Services overview    |
| `/services/cctv`     | services   | CCTV detail          |
| `/services/locks`    | services   | Locks detail         |
| `/services/chips`    | services   | Chips detail         |
| `/contact/`          | contact    | Contact form         |
