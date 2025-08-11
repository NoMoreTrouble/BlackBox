from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models import Reading

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    last = Reading.query.order_by(Reading.id.desc()).first()
    return render_template("index.html", last=last)

@bp.post("/manual/irrigate")
@login_required
def manual_irrigate():
    from flask import current_app
    try:
        seconds = max(1, int(request.form.get("seconds", "5")))
    except Exception:
        seconds = 5
    cl = current_app.extensions["control_loop"]
    cl.pulse_irrigation(seconds)
    return redirect(url_for("main.index"))

@bp.post("/manual/light")
@login_required
def manual_light():
    from flask import current_app
    action = request.form.get("action", "on")
    cl = current_app.extensions["control_loop"]
    if action == "on":
        cl.light_on()
    else:
        cl.light_off()
    return redirect(url_for("main.index"))
