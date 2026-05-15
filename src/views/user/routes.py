from flask import render_template, Blueprint


user_blueprint = Blueprint(
    "user",
    __name__
)

@user_blueprint.route("/user")
def user():
    return render_template("user/user.html")

