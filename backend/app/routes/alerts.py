"""
alerts.py — Alert system API endpoints
"""
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/generate")
async def generate_alerts(
    city: str = Query("Mumbai"),
    disease: str = Query("dengue"),
    days: int = Query(14, ge=7, le=30)
):
    """Generate alerts for a city based on forecasts."""
    from ..main import disease_predictor, icu_predictor
    from ..utils.helpers import generate_alerts as gen_alerts
    import numpy as np
    
    disease_forecast = disease_predictor.predict(city, disease, days)
    current = {
        "admissions": int(np.random.randint(30, 80)),
        "icu_admissions": int(np.random.randint(5, 15)),
        "rolling_avg": float(np.random.uniform(40, 65)),
        "temperature": float(np.random.uniform(25, 38)),
        "humidity": float(np.random.uniform(40, 85)),
        "rainfall_mm": float(np.random.uniform(0, 30)),
    }
    icu_forecast = icu_predictor.predict_occupancy(city, current, days)
    alerts = gen_alerts(disease_forecast, icu_forecast, city)
    return {"city": city, "alerts": alerts, "total_alerts": len(alerts)}


@router.get("/all-cities")
async def get_all_city_alerts():
    """Get alerts across all major cities."""
    from ..main import disease_predictor, icu_predictor
    from ..utils.helpers import generate_alerts as gen_alerts
    import numpy as np
    
    cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata",
              "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
    diseases = ["dengue", "malaria", "flu", "covid", "respiratory"]
    all_alerts = []
    
    for city in cities:
        for disease in diseases:
            df = disease_predictor.predict(city, disease, 14)
            current = {
                "admissions": int(np.random.randint(30, 80)),
                "icu_admissions": int(np.random.randint(5, 15)),
                "rolling_avg": float(np.random.uniform(40, 65)),
                "temperature": float(np.random.uniform(25, 38)),
                "humidity": float(np.random.uniform(40, 85)),
                "rainfall_mm": float(np.random.uniform(0, 30)),
            }
            icu = icu_predictor.predict_occupancy(city, current, 14)
            alerts = gen_alerts(df, icu, city)
            all_alerts.extend(alerts)
    
    # Sort by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    all_alerts.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 3))
    return {"alerts": all_alerts[:20], "total": len(all_alerts)}
