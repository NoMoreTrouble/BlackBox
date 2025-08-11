from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_babel import _
from ..models import db, Reading, ActuationLog
from ..control.controller import ControlLoop
from datetime import datetime, timedelta

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    # Stats for header
    last = Reading.query.order_by(Reading.id.desc()).first()
    return render_template("index.html", last=last)

@bp.post("/manual/irrigate")
@login_required
def manual_irrigate():
    seconds = int(request.form.get("seconds", 5))
    from flask import current_app
    cl = current_app.before_request_funcs[None][0].__self__  # hacky: get ControlLoop instance bound in app factory
    cl.pulse_irrigation(seconds)
    return redirect(url_for("main.index"))

@bp.post("/manual/light")
@login_required
def manual_light():
    action = request.form.get("action", "on")
    from flask import current_app
    cl = current_app.before_request_funcs[None][0].__self__
    if action == "on":
        cl.light_on()
    else:
        cl.light_off()
    return redirect(url_for("main.index"))
