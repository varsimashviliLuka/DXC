# DXC.GE – How Everything Works

A complete guide so you can confidently upgrade the project in the future.

---

## 1. The Big Picture

```
Browser  →  run.py  →  Flask app  →  Blueprint route  →  Template  →  HTML response
```

When someone visits `dxc.ge`, their browser sends an HTTP request. Flask receives
it, matches the URL to a route function, the function prepares data, renders an
HTML template, and sends the page back. That's the full cycle.

---

## 2. Project Structure Explained File by File

```
dxc/
├── run.py                    ← START HERE. Boots the server.
├── config.py                 ← All settings in one place.
├── requirements.txt          ← Python packages to install.
├── .env.example              ← Environment variable template.
│
└── app/
    ├── __init__.py           ← App factory. Wires everything together.
    ├── errors.py             ← Handles 404 / 500 pages.
    ├── utils.py              ← Language/translation helpers.
    │
    ├── translations/
    │   ├── en.json           ← All English text in one file.
    │   └── ka.json           ← All Georgian text in one file.
    │
    ├── routes/
    │   ├── main.py           ← Homepage ( / ) and About ( /about )
    │   ├── services.py       ← /services/* pages
    │   └── contact.py        ← /contact form (GET + POST)
    │
    ├── templates/
    │   ├── base.html         ← Shared layout (navbar + footer)
    │   ├── index.html        ← Homepage content
    │   ├── about.html
    │   ├── services.html
    │   ├── contact.html
    │   ├── service_detail.html
    │   └── errors/
    │       ├── 404.html
    │       └── 500.html
    │
    └── static/
        ├── css/style.css     ← All styles
        ├── js/main.js        ← Mobile nav, animations
        └── img/              ← Put images here
```

---

## 3. run.py — The Entry Point

```python
from app import create_app
import config

app = create_app(config.DevelopmentConfig)

if __name__ == "__main__":
    app.run()
```

This is the only file you run directly (`python run.py`). It:
1. Calls `create_app()` with the Development config
2. Flask starts listening on `http://localhost:5000`

**To switch to production config:** change `DevelopmentConfig` to `ProductionConfig`,
or better, use an environment variable to pick the config automatically.

---

## 4. config.py — All Settings

```python
class DevelopmentConfig(Config):
    DEBUG = True          # Shows error details in browser
    DATABASE_URI = "..."  # SQLite file for local dev

class ProductionConfig(Config):
    DEBUG = False         # NEVER show errors in production
    SECRET_KEY = os.environ.get("SECRET_KEY")  # Must be set on server
```

**Rule of thumb:** Never put real passwords or secret keys in this file.
Use environment variables (the `.env` file) for sensitive values.

To add a new setting:
```python
# In config.py, inside Config class:
COMPANY_PHONE = "+995 555 123 456"

# In any template automatically via Flask config:
{{ config.COMPANY_PHONE }}

# Or pass it from a route:
return render_template("index.html", phone=current_app.config["COMPANY_PHONE"])
```

---

## 5. app/__init__.py — The App Factory

```python
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Register blueprints (groups of routes)
    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(contact_bp,  url_prefix="/contact")

    # Language switcher route
    @app.route("/set-lang/<lang>")
    def set_lang(lang): ...

    # Context processor — injects `t` into EVERY template automatically
    @app.context_processor
    def inject_translations():
        lang = get_current_lang()
        return dict(t=load_translations(lang), lang=lang)

    return app
```

The **context processor** is the key piece. It runs before every single
template render and injects the variable `t` (a dictionary of translated
strings) so every template can use `{{ t.some_key }}` without any extra work.

---

## 6. Blueprints — How Routes Are Organized

A Blueprint is just a group of related routes. Think of it as a mini-app.

```python
# app/routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")
```

The Blueprint is **registered** in `__init__.py`:
```python
app.register_blueprint(services_bp, url_prefix="/services")
```

This means every route inside `services_bp` automatically starts with `/services`.
So `@services_bp.route("/cctv")` becomes the URL `/services/cctv`.

**To add a new page:**
1. Add a route function to the right blueprint (or create a new one)
2. Create a matching template in `app/templates/`
3. If it's a new blueprint, register it in `__init__.py`

---

## 7. Templates — Jinja2 Basics

Templates are HTML files with special `{{ }}` and `{% %}` tags.

```html
<!-- base.html — the shared layout -->
<nav>...</nav>
<main>{% block content %}{% endblock %}</main>
<footer>...</footer>
```

```html
<!-- index.html — extends the layout -->
{% extends "base.html" %}
{% block content %}
  <h1>{{ t.hero_title_top }}</h1>   ← variable from translation dict
{% endblock %}
```

Every child template (`index.html`, `about.html`, etc.) extends `base.html`.
This means the navbar and footer are written only once.

**Passing data from a route to a template:**
```python
# In the route:
return render_template("index.html", username="Giorgi", items=[1, 2, 3])

# In the template:
<p>Hello {{ username }}</p>
{% for item in items %}
  <p>{{ item }}</p>
{% endfor %}
```

---

## 8. Language System — How It Works

The entire translation system has 3 moving parts:

### Part 1 — Translation files (`app/translations/en.json`, `ka.json`)

Each file is a flat dictionary of key → text pairs:
```json
{
  "nav_home": "Home",
  "hero_title_top": "DIGITAL X CONTROL"
}
```
The Georgian file has the same keys, just different values.
**To add a new text string:** add the key to BOTH files.

### Part 2 — Language stored in session

When the user clicks the language button, they hit `/set-lang/ka` (or `/set-lang/en`).
This route saves the chosen language code into Flask's `session` object:

```python
@app.route("/set-lang/<lang>")
def set_lang(lang):
    session["lang"] = lang          # Saved in a secure cookie
    return redirect(request.referrer or "/")   # Go back to previous page
```

The `session` is like a per-user cookie managed by Flask. It persists across
page loads until the browser is closed (or the cookie expires).

### Part 3 — Context processor injects `t` everywhere

```python
@app.context_processor
def inject_translations():
    lang = session.get("lang", "en")
    return dict(t=load_translations(lang), lang=lang)
```

This runs before EVERY template render. It reads the session, loads the right
JSON file, and makes the `t` variable available in all templates automatically.

### In templates:
```html
<h1>{{ t.hero_title_top }}</h1>
<a href="/set-lang/{{ t.lang_other_code }}">{{ t.lang_other }}</a>
```

The language toggle button shows the OTHER language's name (e.g. when you're
in English it shows "ქართული", and when in Georgian it shows "English").

### To add a third language (e.g. Russian):
1. Create `app/translations/ru.json` with all the same keys
2. Add `"ru"` to `SUPPORTED_LANGS` in `utils.py`
3. Update `en.json` and `ka.json`: add `"lang_other"` logic (you'd need to make
   this a list or add a dedicated nav switcher for 3+ languages)

---

## 9. Static Files (CSS, JS, Images)

Files in `app/static/` are served directly by Flask.

**In templates, always use `url_for`:**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"/>
<img src="{{ url_for('static', filename='img/logo.png') }}"/>
```

Never hardcode `/static/...` paths — `url_for` handles subdirectory deployments correctly.

**CSS structure (`style.css`):**
- CSS variables at the top (`:root { --blue: ... }`) — change these to retheme the site
- Sections are clearly commented: Reset, Buttons, Navbar, Hero, Services, etc.
- Media queries at the very bottom

---

## 10. The Contact Form

```python
@contact_bp.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":           # Form was submitted
        name = request.form.get("name")    # Read form field
        ...
        flash("Thank you!", "success")     # Show one-time message
        return redirect(url_for("contact.contact"))  # Redirect (prevents resubmit)

    return render_template("contact.html") # Normal GET: just show the form
```

The POST/Redirect/GET pattern (`redirect` after POST) is important — it
prevents the "resubmit form?" browser warning if the user refreshes.

**To actually send emails**, replace the `# TODO` comment with:
```python
# pip install flask-mail
from flask_mail import Mail, Message
mail.send_message(
    subject=f"New enquiry from {name}",
    recipients=["info@dxc.ge"],
    body=message
)
```

---

## 11. Error Pages

```python
# app/errors.py
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404
```

These catch errors globally. The templates in `errors/` extend `base.html`
so they share the same navbar and footer automatically.

---

## 12. Common Upgrade Scenarios

### Add a new page (e.g. /gallery)
```python
# 1. In app/routes/main.py:
@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")

# 2. Create app/templates/gallery.html:
{% extends "base.html" %}
{% block content %}...{% endblock %}

# 3. Add nav link in base.html and translation keys in en.json / ka.json
```

### Add a database (SQLAlchemy)
```bash
pip install flask-sqlalchemy
```
```python
# config.py — already has SQLALCHEMY_DATABASE_URI
# app/__init__.py — add:
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# Create a model:
class Project(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
```

### Add user login (Flask-Login)
```bash
pip install flask-login
```
Create a `User` model, add login/logout routes in a new `auth` blueprint.

### Deploy to a server
1. Set `SECRET_KEY` as an environment variable
2. Use `ProductionConfig` in `run.py`
3. Serve with `gunicorn`: `gunicorn "app:create_app(config.ProductionConfig)"`
4. Put Nginx in front of gunicorn

---

## 13. Quick Reference Cheatsheet

| What you want to do | Where to look |
|---|---|
| Change site colors | `static/css/style.css` → `:root` variables |
| Change English text | `translations/en.json` |
| Change Georgian text | `translations/ka.json` |
| Add a new route/page | `routes/main.py` (or new blueprint) |
| Add a new nav link | `templates/base.html` + both JSON files |
| Change site settings (email, phone) | `config.py` or JSON files |
| Add a new service | JSON files + `index.html` service_data list |
| Add a 3rd language | New JSON + add to `SUPPORTED_LANGS` in `utils.py` |
| Handle form submission | `routes/contact.py` |
| Add images | `static/img/` then `{{ url_for('static', filename='img/x.jpg') }}` |
