from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from ..models import Reading

bp = Blueprint("api", __name__)

@bp.get("/history")
def history():
    rng = request.args.get("range", "24h")
    now = datetime.utcnow()
    if rng.endswith("h"):
        hours = int(rng[:-1])
        start = now - timedelta(hours=hours)
    elif rng.endswith("d"):
        days = int(rng[:-1])
        start = now - timedelta(days=days)
    else:
        start = now - timedelta(hours=24)

    q = Reading.query.filter(Reading.ts >= start).order_by(Reading.ts.asc()).all()
    data = {
        "ts": [r.ts.isoformat() for r in q],
        "temperature": [r.temperature for r in q],
        "humidity": [r.humidity for r in q],
        "soil1": [r.soil1 for r in q],
        "soil2": [r.soil2 for r in q],
        "soil3": [r.soil3 for r in q],
        "soil_avg": [r.soil_avg for r in q],
        "soil_avg_ewma": [r.soil_avg_ewma for r in q],
        "water_level_pct": [r.water_level_pct for r in q],
    }
    return jsonify(data)
