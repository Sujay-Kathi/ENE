"""
helpers.py — Utility functions for FutureLens
"""
from datetime import datetime, timedelta
import numpy as np


def generate_alerts(disease_forecast, icu_forecast, city):
    """Generate early warning alerts based on forecasts."""
    alerts = []
    
    # Disease trend alerts
    if disease_forecast:
        preds = disease_forecast.get("predictions", [])
        if preds:
            avg = disease_forecast.get("avg_predicted", 0)
            trend = disease_forecast.get("trend_direction", "stable")
            disease = disease_forecast.get("disease", "unknown")
            peak = disease_forecast.get("peak_value", 0)
            
            if trend == "rising" and peak > avg * 1.3:
                pct_rise = round((peak - avg) / max(avg, 1) * 100)
                alerts.append({
                    "type": "disease_surge",
                    "severity": "high" if pct_rise > 50 else "medium",
                    "title": f"{disease.title()} Outbreak Warning — {city}",
                    "message": f"{disease.title()} cases expected to rise by {pct_rise}% in the next {disease_forecast['forecast_days']} days. Peak: {peak} cases on {disease_forecast['peak_date']}",
                    "recommendation": f"Increase {disease} treatment supplies and staff allocation",
                    "timestamp": datetime.now().isoformat()
                })
    
    # ICU capacity alerts
    if icu_forecast:
        for pred in icu_forecast.get("predictions", []):
            if pred["crisis_probability"] > 0.7:
                alerts.append({
                    "type": "icu_crisis",
                    "severity": "critical",
                    "title": f"ICU Capacity Crisis — {city}",
                    "message": f"ICU occupancy predicted to reach {pred['icu_occupancy_pct']}% by {pred['date']}. Crisis probability: {round(pred['crisis_probability'] * 100)}%",
                    "recommendation": "Activate overflow protocols. Delay non-critical elective procedures. Consider patient transfers.",
                    "timestamp": datetime.now().isoformat()
                })
                break
            elif pred["crisis_probability"] > 0.5:
                alerts.append({
                    "type": "icu_warning",
                    "severity": "high",
                    "title": f"ICU High Demand Alert — {city}",
                    "message": f"ICU occupancy projected at {pred['icu_occupancy_pct']}% by {pred['date']}",
                    "recommendation": "Prepare additional ICU capacity. Increase staffing for next 48 hours.",
                    "timestamp": datetime.now().isoformat()
                })
                break
    
    return alerts


def get_national_summary(registry_df):
    """Calculate national-level hospital statistics."""
    return {
        "total_hospitals": len(registry_df),
        "total_beds": int(registry_df["total_beds"].sum()),
        "total_icu_beds": int(registry_df["icu_beds"].sum()),
        "total_free_beds": int(registry_df["free_beds"].sum()),
        "total_free_icu": int(registry_df["free_icu_beds"].sum()),
        "avg_occupancy": round(float(registry_df["occupancy_pct"].mean()), 1),
        "avg_icu_occupancy": round(float(registry_df["icu_occupancy_pct"].mean()), 1),
        "states_covered": int(registry_df["state"].nunique()),
        "cities_covered": int(registry_df["city"].nunique()),
        "critical_hospitals": int((registry_df["icu_occupancy_pct"] > 85).sum()),
    }
