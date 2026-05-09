"""
main.py — FutureLens FastAPI Application
Predicting Disease Trends & Hospital Resource Demand
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from .models.prophet_model import DiseaseTrendPredictor
from .models.xgboost_model import ICUDemandPredictor
from .data.generator import generate_daily_admissions, generate_hospital_registry
from .data.hospitals import INDIA_HOSPITAL_DATA, CITY_COORDINATES

# Initialize FastAPI app
app = FastAPI(
    title="FutureLens API",
    description="AI-Powered Disease Trend & Hospital Resource Demand Prediction",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances
disease_predictor = DiseaseTrendPredictor()
icu_predictor = ICUDemandPredictor()
hospital_registry = pd.DataFrame()
admissions_data = pd.DataFrame()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")


@app.on_event("startup")
async def startup():
    global hospital_registry, admissions_data
    os.makedirs(DATA_DIR, exist_ok=True)

    # Load or generate data
    adm_path = os.path.join(DATA_DIR, "daily_admissions.csv")
    reg_path = os.path.join(DATA_DIR, "hospital_registry.csv")

    if os.path.exists(adm_path):
        print("📂 Loading existing admissions data...")
        admissions_data = pd.read_csv(adm_path)
    else:
        print("🏥 Generating synthetic admissions data...")
        admissions_data = generate_daily_admissions(days=730)
        admissions_data.to_csv(adm_path, index=False)
        print(f"   ✅ Generated {len(admissions_data)} records")

    if os.path.exists(reg_path):
        print("📂 Loading existing hospital registry...")
        hospital_registry = pd.read_csv(reg_path)
    else:
        print("🏥 Generating hospital registry...")
        hospital_registry = generate_hospital_registry()
        hospital_registry.to_csv(reg_path, index=False)
        print(f"   ✅ Generated {len(hospital_registry)} hospitals")

    # Train models
    print("🔮 Training disease trend models...")
    cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata"]
    diseases = ["dengue", "flu", "covid"]
    for city in cities:
        for disease in diseases:
            disease_predictor.train(admissions_data, city, disease)
    print("   ✅ Disease models ready")

    print("📊 Training ICU demand model...")
    icu_predictor.train(admissions_data)
    print(f"   ✅ ICU model ready | Metrics: {icu_predictor.metrics}")


# Register routes
from .routes.predictions import router as pred_router
from .routes.hospitals import router as hosp_router
from .routes.alerts import router as alert_router

app.include_router(pred_router)
app.include_router(hosp_router)
app.include_router(alert_router)


@app.get("/")
async def root():
    return {
        "name": "FutureLens API",
        "version": "1.0.0",
        "description": "Predicting Disease Trends & Hospital Resource Demand",
        "endpoints": {
            "predictions": "/api/predictions/disease-trend",
            "icu_demand": "/api/predictions/icu-demand",
            "hospitals": "/api/hospitals/registry",
            "alerts": "/api/alerts/generate",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "models_loaded": True,
            "hospitals_count": len(hospital_registry),
            "admissions_records": len(admissions_data)}
