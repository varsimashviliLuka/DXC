from flask import render_template, Blueprint
from src.config import Config

auth_blueprint = Blueprint(
    "auth",
    __name__
)

@auth_blueprint.route("/login")
def login():
    return render_template("auth/login.html")


@auth_blueprint.route("/register")
def register():
    return render_template("auth/register.html")