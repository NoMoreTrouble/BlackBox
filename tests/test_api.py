from plant_monitor.models import db, Reading
from datetime import datetime, timedelta

def test_history(client, app):
    with app.app_context():
        for i in range(5):
            db.session.add(Reading(temperature=20+i, humidity=50, soil1=60, soil2=55, soil3=50, soil_avg=55, soil_avg_ewma=55, water_level_pct=80))
        db.session.commit()
    res = client.get('/api/history?range=24h')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data['temperature']) >= 5
