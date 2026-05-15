from flask import render_template, Blueprint


admin_blueprint = Blueprint(
    "admin",
    __name__
)

@admin_blueprint.route("/admin")
def admin():
    return render_template("admin/admin.html")

