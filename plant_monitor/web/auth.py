from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
try:
    from flask_babel import _
except Exception:
    _ = lambda s: s  # fallback if Babel not installed
from ..models import User

bp = Blueprint("auth", __name__, template_folder="templates")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.index"))
        flash(_("Invalid credentials"), "danger")
    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
