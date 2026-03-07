from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.utils import load_translations, get_current_lang

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        t       = load_translations(get_current_lang())
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash(t["form_error"], "error")
            return redirect(url_for("contact.contact"))

        # TODO: send email / save to DB
        flash(t["form_success"], "success")
        return redirect(url_for("contact.contact"))

    return render_template("contact.html")
