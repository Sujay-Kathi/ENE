"""
prophet_model.py — Disease Trend Prediction using Facebook Prophet
"""
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime, timedelta

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

class DiseaseTrendPredictor:
    def __init__(self):
        self.models = {}
        self.model_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

    def train(self, df, city, disease):
        mask = (df["city"] == city) & (df["disease"] == disease)
        cdf = df[mask].copy()
        if len(cdf) < 30:
            return None
        pdf = cdf[["date", "admissions"]].copy()
        pdf.columns = ["ds", "y"]
        pdf["ds"] = pd.to_datetime(pdf["ds"])
        pdf = pdf.groupby("ds").agg({"y": "sum"}).reset_index()
        if not PROPHET_AVAILABLE:
            self.models[(city, disease)] = {"type": "fallback", "data": pdf}
            return pdf
        import logging
        logging.getLogger("prophet").setLevel(logging.WARNING)
        logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True,
                        daily_seasonality=False, changepoint_prior_scale=0.05,
                        seasonality_prior_scale=10, interval_width=0.90)
        model.fit(pdf)
        self.models[(city, disease)] = {"type": "prophet", "model": model, "train_data": pdf}
        return pdf

    def predict(self, city, disease, days=30):
        key = (city, disease)
        if key not in self.models:
            return self._fallback(city, disease, days)
        info = self.models[key]
        if info["type"] == "fallback":
            return self._fallback_data(info["data"], city, disease, days)
        model = info["model"]
        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)
        ff = forecast.tail(days)
        preds = []
        for _, r in ff.iterrows():
            preds.append({"date": r["ds"].strftime("%Y-%m-%d"),
                          "predicted": round(max(0, float(r["yhat"])), 1),
                          "lower_bound": round(max(0, float(r["yhat_lower"])), 1),
                          "upper_bound": round(max(0, float(r["yhat_upper"])), 1)})
        pv = [p["predicted"] for p in preds]
        pi = int(np.argmax(pv))
        return {"city": city, "disease": disease, "forecast_days": days,
                "predictions": preds,
                "trend_direction": "rising" if pv[-1] > pv[0] else "falling",
                "peak_date": preds[pi]["date"], "peak_value": round(max(pv), 1),
                "avg_predicted": round(float(np.mean(pv)), 1)}

    def _fallback(self, city, disease, days):
        from ..data.hospitals import DISEASE_SEASONS
        base_rates = {"dengue": 25, "malaria": 20, "flu": 35, "covid": 15, "respiratory": 30, "gastro": 22}
        base = base_rates.get(disease, 20)
        today = datetime.now()
        preds = []
        for i in range(days):
            d = today + timedelta(days=i)
            s = 1.0
            if disease in DISEASE_SEASONS and d.month in DISEASE_SEASONS[disease]["peak_months"]:
                s = DISEASE_SEASONS[disease]["peak_multiplier"] * 0.7
            dow = 0.85 if d.weekday() in [5, 6] else 1.0
            v = max(0, round(base * s * dow + np.random.normal(0, base * 0.15), 1))
            preds.append({"date": d.strftime("%Y-%m-%d"), "predicted": v,
                          "lower_bound": round(v * 0.7, 1), "upper_bound": round(v * 1.3, 1)})
        pv = [p["predicted"] for p in preds]
        pi = int(np.argmax(pv))
        return {"city": city, "disease": disease, "forecast_days": days, "predictions": preds,
                "trend_direction": "rising" if pv[-1] > pv[0] else "falling",
                "peak_date": preds[pi]["date"], "peak_value": round(max(pv), 1),
                "avg_predicted": round(float(np.mean(pv)), 1)}

    def _fallback_data(self, data, city, disease, days):
        recent = data.tail(30)
        mean_v, std_v = recent["y"].mean(), recent["y"].std()
        slope = (recent["y"].iloc[-1] - recent["y"].iloc[0]) / max(len(recent), 1)
        today = datetime.now()
        preds = []
        for i in range(days):
            d = today + timedelta(days=i)
            v = max(0, round(mean_v + slope * i + np.random.normal(0, std_v * 0.3), 1))
            preds.append({"date": d.strftime("%Y-%m-%d"), "predicted": v,
                          "lower_bound": round(max(0, v - std_v), 1), "upper_bound": round(v + std_v, 1)})
        pv = [p["predicted"] for p in preds]
        pi = int(np.argmax(pv))
        return {"city": city, "disease": disease, "forecast_days": days, "predictions": preds,
                "trend_direction": "rising" if slope > 0 else "falling",
                "peak_date": preds[pi]["date"], "peak_value": round(max(pv), 1),
                "avg_predicted": round(float(np.mean(pv)), 1)}

    def save_models(self, path=None):
        if path is None:
            path = os.path.join(self.model_dir, "prophet_models.pkl")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.models, path)

    def load_models(self, path=None):
        if path is None:
            path = os.path.join(self.model_dir, "prophet_models.pkl")
        if os.path.exists(path):
            self.models = joblib.load(path)
