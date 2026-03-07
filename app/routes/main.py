from flask import Blueprint, render_template, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    services = [
        {
            "icon": "cctv",
            "title": "CCTV Installation",
            "short": "Professional surveillance camera systems for homes and businesses.",
        },
        {
            "icon": "lock",
            "title": "Electric Door Locks",
            "short": "Smart access control with keypad, card, or remote entry systems.",
        },
        {
            "icon": "chip",
            "title": "Chip Duplication",
            "short": "Fast and reliable duplication of key chips, cards, and fobs.",
        },
        {
            "icon": "network",
            "title": "Network & Wiring",
            "short": "Structured cabling, Wi-Fi setup, and network infrastructure.",
        },
        {
            "icon": "alarm",
            "title": "Alarm Systems",
            "short": "Motion-triggered alarms and 24/7 monitoring integrations.",
        },
        {
            "icon": "intercom",
            "title": "Intercom Systems",
            "short": "Video and audio intercom solutions for buildings and gates.",
        },
    ]
    return render_template("index.html", services=services)


@main_bp.route("/about")
def about():
    return render_template("about.html")
