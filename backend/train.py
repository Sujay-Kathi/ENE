"""
train.py — Standalone training script for FutureLens models
Run: python -m backend.train
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app.data.generator import save_generated_data
from backend.app.models.prophet_model import DiseaseTrendPredictor
from backend.app.models.xgboost_model import ICUDemandPredictor


def main():
    print("=" * 60)
    print("🏥 FutureLens — Model Training Pipeline")
    print("=" * 60)

    # Step 1: Generate data
    print("\n📊 Step 1: Generating synthetic data...")
    admissions_df, registry_df, agg_df = save_generated_data()

    # Step 2: Train Prophet models
    print("\n🔮 Step 2: Training Prophet disease models...")
    prophet = DiseaseTrendPredictor()
    cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata",
              "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
    diseases = ["dengue", "malaria", "flu", "covid", "respiratory", "gastro"]

    for city in cities:
        for disease in diseases:
            prophet.train(admissions_df, city, disease)
            print(f"   ✅ Trained: {city} — {disease}")

    prophet.save_models()

    # Step 3: Train XGBoost model
    print("\n📊 Step 3: Training XGBoost ICU model...")
    xgb = ICUDemandPredictor()
    metrics = xgb.train(admissions_df)
    print(f"   ✅ Model metrics: {metrics}")
    xgb.save_models()

    # Step 4: Test predictions
    print("\n🧪 Step 4: Testing predictions...")
    forecast = prophet.predict("Mumbai", "dengue", 14)
    print(f"   Dengue forecast (Mumbai): trend={forecast['trend_direction']}, avg={forecast['avg_predicted']}")

    icu = xgb.predict_occupancy("Delhi", {
        "admissions": 60, "icu_admissions": 10, "rolling_avg": 55,
        "temperature": 32, "humidity": 70, "rainfall_mm": 15
    }, 7)
    print(f"   ICU forecast (Delhi): {len(icu['predictions'])} days predicted")

    print("\n" + "=" * 60)
    print("✅ All models trained and saved successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
