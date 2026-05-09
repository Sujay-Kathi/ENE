import re
import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    city: str = "Mumbai"

CITIES = ['mumbai', 'delhi', 'bengaluru', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad', 'jaipur', 'lucknow']
DISEASES = ['dengue', 'malaria', 'flu', 'covid', 'respiratory', 'gastro']

@router.post("/")
async def chat_with_bot(request: ChatRequest):
    from ..main import icu_predictor, disease_predictor
    
    msg = request.message.lower()
    
    # Extract intent
    target_city = request.city
    for c in CITIES:
        if c in msg:
            target_city = c.capitalize()
            
    target_disease = "dengue"
    for d in DISEASES:
        if d in msg:
            target_disease = d
            
    is_icu_query = any(word in msg for word in ["icu", "bed", "capacity", "full", "hospital"])
    is_disease_query = any(word in msg for word in ["disease", "trend", "surge", "cases", "outbreak"] + DISEASES)
    
    # Context generation
    response = ""
    
    if is_icu_query:
        # Generate synthetic current state to feed into the .pkl model
        current = {
            "admissions": int(np.random.randint(40, 90)),
            "icu_admissions": int(np.random.randint(10, 25)),
            "rolling_avg": float(np.random.uniform(50, 70)),
            "temperature": float(np.random.uniform(28, 35)),
            "humidity": float(np.random.uniform(60, 85)),
            "rainfall_mm": float(np.random.uniform(5, 40)),
        }
        
        # This calls the user's custom .pkl model!
        icu_forecast = icu_predictor.predict_occupancy(target_city, current, 7)
        
        latest = icu_forecast["predictions"][0]
        peak = max(icu_forecast["predictions"], key=lambda x: x["icu_occupancy_pct"])
        
        response += f"According to the AI model predictions for {target_city}, current ICU utilization is at {latest['icu_occupancy_pct']}%. "
        
        if peak['risk_level'] in ['high', 'critical']:
            response += f"⚠️ **Warning**: The model detects a critical surge. ICU occupancy is predicted to peak at {peak['icu_occupancy_pct']}% on {peak['date']}. "
            response += "Emergency reallocation of beds is highly recommended."
        else:
            response += f"Capacity is currently stable. The maximum projected occupancy over the next 7 days is {peak['icu_occupancy_pct']}%."
            
    elif is_disease_query:
        # Query Prophet disease models
        trend = disease_predictor.predict(target_city, target_disease, 14)
        response += f"For {target_disease.capitalize()} in {target_city}, the 14-day forecast indicates a **{trend['trend_direction']}** trend. "
        response += f"Cases are expected to peak at {trend['peak_value']} cases around {trend['peak_date']}. "
        
        if trend['trend_direction'] == 'rising':
            response += "Hospitals should prepare adequate treatment supplies."
            
    else:
        # General response
        response = "I am the FutureLens AI assistant. I can analyze our predictive models to tell you about upcoming ICU capacity shortages, bed availability, or disease outbreak trends. For example, try asking: 'What is the ICU capacity in Bengaluru?' or 'Are Dengue cases rising in Delhi?'"

    return {"response": response, "city": target_city}
