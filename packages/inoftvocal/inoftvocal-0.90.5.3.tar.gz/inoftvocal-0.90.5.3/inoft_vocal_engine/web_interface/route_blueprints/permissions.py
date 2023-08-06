from flask import Blueprint, render_template


permissions_blueprint = Blueprint("permissions", __name__, template_folder="templates")

@permissions_blueprint.route("/permissions/missing")
def permissions_missing():
    return render_template("permissions/missing.html")
