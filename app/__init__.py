from flask import Flask, session, redirect, request
from app.utils import load_translations, get_current_lang


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # ── Register blueprints ──────────────────────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.services import services_bp
    from app.routes.contact import contact_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(contact_bp, url_prefix="/contact")

    # ── Language switcher route ──────────────────────────────────────────────
    @app.route("/set-lang/<lang>")
    def set_lang(lang):
        """Store chosen language in session, then go back to previous page."""
        from app.utils import SUPPORTED_LANGS
        if lang in SUPPORTED_LANGS:
            session["lang"] = lang
        return redirect(request.referrer or "/")

    # ── Context processor: inject `t` (translations) into every template ─────
    @app.context_processor
    def inject_translations():
        lang = get_current_lang()
        return dict(t=load_translations(lang), lang=lang)

    # ── Custom error handlers ────────────────────────────────────────────────
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
