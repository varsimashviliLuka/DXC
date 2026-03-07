from flask import Blueprint, render_template

services_bp = Blueprint("services", __name__)


@services_bp.route("/")
def services():
    return render_template("services.html")


@services_bp.route("/cctv")
def cctv():
    return render_template("service_detail.html", service="cctv")


@services_bp.route("/locks")
def locks():
    return render_template("service_detail.html", service="locks")


@services_bp.route("/chips")
def chips():
    return render_template("service_detail.html", service="chips")
