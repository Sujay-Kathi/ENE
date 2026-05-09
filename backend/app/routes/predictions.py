"""
predictions.py — Prediction API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.get("/disease-trend")
async def get_disease_trend(
    city: str = Query("Mumbai", description="City name"),
    disease: str = Query("dengue", description="Disease name"),
    days: int = Query(30, description="Forecast days", ge=7, le=90)
):
    """Forecast disease trend for a city."""
    from ..main import disease_predictor
    result = disease_predictor.predict(city, disease, days)
    return result


@router.get("/icu-demand")
async def get_icu_demand(
    city: str = Query("Mumbai", description="City name"),
    days: int = Query(14, description="Forecast days", ge=7, le=30)
):
    """Forecast ICU demand for a city."""
    from ..main import icu_predictor
    import numpy as np
    current = {
        "admissions": int(np.random.randint(30, 80)),
        "icu_admissions": int(np.random.randint(5, 15)),
        "rolling_avg": float(np.random.uniform(40, 65)),
        "temperature": float(np.random.uniform(25, 38)),
        "humidity": float(np.random.uniform(40, 85)),
        "rainfall_mm": float(np.random.uniform(0, 30)),
    }
    result = icu_predictor.predict_occupancy(city, current, days)
    return result


@router.get("/feature-importance")
async def get_feature_importance():
    """Get XGBoost feature importance scores."""
    from ..main import icu_predictor
    return icu_predictor.get_feature_importance()


@router.get("/all-diseases")
async def get_all_disease_trends(
    city: str = Query("Mumbai"),
    days: int = Query(14, ge=7, le=90)
):
    """Get forecasts for all diseases for a city."""
    from ..main import disease_predictor
    diseases = ["dengue", "malaria", "flu", "covid", "respiratory", "gastro"]
    results = {}
    for d in diseases:
        results[d] = disease_predictor.predict(city, d, days)
    return results
