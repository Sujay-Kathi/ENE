"""
generator.py — Synthetic data generation for FutureLens
Generates realistic Indian hospital admission data with disease seasonality,
weather effects, festival spikes, and occupancy patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from .hospitals import INDIA_HOSPITAL_DATA, DISEASE_SEASONS, CITY_COORDINATES

# Seed for reproducibility
np.random.seed(42)


def generate_daily_admissions(days: int = 730, cities: list = None) -> pd.DataFrame:
    """
    Generate synthetic daily hospital admission data for Indian cities.
    
    Args:
        days: Number of days of historical data (default: 2 years)
        cities: List of cities to generate data for
        
    Returns:
        DataFrame with columns: date, city, state, disease, admissions,
        icu_admissions, bed_occupancy_pct, icu_occupancy_pct, temperature,
        humidity, rainfall_mm, is_festival, day_of_week, month
    """
    if cities is None:
        cities = [
            "Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata",
            "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
            "Kochi", "Bhopal", "Patna", "Chandigarh", "Bhubaneswar"
        ]
    
    # Map cities to states
    city_state_map = {}
    for state, info in INDIA_HOSPITAL_DATA["states"].items():
        for city in info["major_cities"]:
            city_state_map[city] = state
    
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Indian festivals (approximate dates - recurring yearly)
    festivals = {
        "Diwali": [(10, 25), (10, 26), (10, 27)],  # Oct-Nov
        "Holi": [(3, 14), (3, 15)],                   # March
        "Eid": [(4, 10), (4, 11)],                     # Varies
        "Ganesh_Chaturthi": [(9, 7), (9, 8), (9, 9)],  # Sep
        "Durga_Puja": [(10, 10), (10, 11), (10, 12)],  # Oct
        "Pongal": [(1, 14), (1, 15), (1, 16)],         # Jan
        "Christmas": [(12, 25), (12, 26)],              # Dec
        "New_Year": [(1, 1), (1, 2)],                   # Jan
    }
    
    records = []
    diseases = list(DISEASE_SEASONS.keys())
    
    for date in dates:
        month = date.month
        day_of_week = date.weekday()
        day_of_year = date.timetuple().tm_yday
        
        # Check if festival
        is_festival = 0
        for fest_name, fest_dates in festivals.items():
            for fd in fest_dates:
                if month == fd[0] and date.day == fd[1]:
                    is_festival = 1
                    break
        
        for city in cities:
            state = city_state_map.get(city, "Maharashtra")
            state_data = INDIA_HOSPITAL_DATA["states"].get(state, {})
            
            # Weather simulation based on Indian patterns
            if month in [3, 4, 5]:  # Summer
                temperature = np.random.normal(38, 4)
                humidity = np.random.normal(40, 10)
                rainfall = max(0, np.random.exponential(2))
            elif month in [6, 7, 8, 9]:  # Monsoon
                temperature = np.random.normal(30, 3)
                humidity = np.random.normal(85, 8)
                rainfall = max(0, np.random.exponential(25))
            elif month in [10, 11]:  # Post-monsoon
                temperature = np.random.normal(28, 4)
                humidity = np.random.normal(60, 12)
                rainfall = max(0, np.random.exponential(5))
            else:  # Winter
                temperature = np.random.normal(18, 5)
                humidity = np.random.normal(55, 10)
                rainfall = max(0, np.random.exponential(1))
            
            for disease in diseases:
                disease_info = DISEASE_SEASONS[disease]
                
                # Base admission rate
                base = disease_info["base_rate"]
                
                # Seasonal multiplier
                if month in disease_info["peak_months"]:
                    seasonal_mult = disease_info["peak_multiplier"]
                    # Gradual ramp-up at edges
                    if month == disease_info["peak_months"][0]:
                        seasonal_mult *= 0.6
                    elif month == disease_info["peak_months"][-1]:
                        seasonal_mult *= 0.7
                else:
                    seasonal_mult = 1.0
                
                # Regional relevance
                regional_mult = 1.5 if state in disease_info["affected_regions"] else 0.4
                
                # City size multiplier (population proxy)
                city_pop_mult = {
                    "Mumbai": 2.5, "Delhi": 2.8, "Bengaluru": 2.0, "Chennai": 1.8,
                    "Kolkata": 2.0, "Hyderabad": 1.9, "Pune": 1.5, "Ahmedabad": 1.5,
                    "Jaipur": 1.2, "Lucknow": 1.3, "Kochi": 0.8, "Bhopal": 0.9,
                    "Patna": 1.1, "Chandigarh": 0.7, "Bhubaneswar": 0.8
                }.get(city, 1.0)
                
                # Day-of-week effect (weekends = fewer elective, but more emergency)
                dow_mult = 0.85 if day_of_week in [5, 6] else 1.0
                
                # Festival effect
                festival_mult = 1.4 if is_festival else 1.0
                
                # Trend component (slight year-over-year increase)
                trend = 1.0 + (day_of_year / 365) * 0.05
                
                # Calculate admissions
                expected = base * seasonal_mult * regional_mult * city_pop_mult * dow_mult * festival_mult * trend
                admissions = max(0, int(np.random.poisson(max(1, expected))))
                
                # ICU admissions (10-20% of total depending on disease)
                icu_rate = {"dengue": 0.15, "malaria": 0.12, "flu": 0.08,
                           "covid": 0.20, "respiratory": 0.18, "gastro": 0.06}[disease]
                icu_admissions = max(0, int(np.random.binomial(admissions, icu_rate)))
                
                # Bed occupancy calculation
                total_beds = state_data.get("total_beds", 100000)
                icu_beds = state_data.get("icu_beds", 5000)
                
                # Scale to city level (~20% of state)
                city_beds = int(total_beds * 0.20 * city_pop_mult / 2)
                city_icu = int(icu_beds * 0.20 * city_pop_mult / 2)
                
                base_occupancy = 55 + seasonal_mult * 8 + (festival_mult - 1) * 15
                bed_occupancy_pct = min(99, max(30, base_occupancy + np.random.normal(0, 8)))
                
                base_icu_occ = 50 + seasonal_mult * 10 + (festival_mult - 1) * 12
                icu_occupancy_pct = min(99, max(25, base_icu_occ + np.random.normal(0, 10)))
                
                records.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "city": city,
                    "state": state,
                    "disease": disease,
                    "admissions": admissions,
                    "icu_admissions": icu_admissions,
                    "total_beds_city": city_beds,
                    "total_icu_city": city_icu,
                    "bed_occupancy_pct": round(bed_occupancy_pct, 1),
                    "icu_occupancy_pct": round(icu_occupancy_pct, 1),
                    "temperature": round(temperature, 1),
                    "humidity": round(humidity, 1),
                    "rainfall_mm": round(rainfall, 1),
                    "is_festival": is_festival,
                    "day_of_week": day_of_week,
                    "month": month
                })
    
    df = pd.DataFrame(records)
    return df


def generate_hospital_registry(num_hospitals_per_city: int = 20) -> pd.DataFrame:
    """
    Generate a registry of hospitals per city with bed counts.
    """
    cities_data = []
    hospital_id = 1000
    
    hospital_types = ["Government General", "Government District", "Private Multi-Specialty",
                      "Private Super-Specialty", "PHC", "CHC", "Medical College Hospital"]
    
    for state, info in INDIA_HOSPITAL_DATA["states"].items():
        for city in info["major_cities"]:
            n_hospitals = np.random.randint(15, num_hospitals_per_city + 10)
            
            for _ in range(n_hospitals):
                h_type = np.random.choice(hospital_types, p=[0.15, 0.1, 0.25, 0.15, 0.15, 0.1, 0.1])
                
                if "Government" in h_type or "Medical College" in h_type:
                    total_beds = np.random.randint(100, 800)
                    icu_beds = int(total_beds * np.random.uniform(0.05, 0.12))
                elif "Super-Specialty" in h_type:
                    total_beds = np.random.randint(200, 1200)
                    icu_beds = int(total_beds * np.random.uniform(0.10, 0.20))
                elif "Multi-Specialty" in h_type:
                    total_beds = np.random.randint(50, 500)
                    icu_beds = int(total_beds * np.random.uniform(0.08, 0.15))
                else:  # PHC/CHC
                    total_beds = np.random.randint(10, 50)
                    icu_beds = np.random.randint(0, 3)
                
                # Current occupancy (simulated real-time)
                current_occupied = int(total_beds * np.random.uniform(0.45, 0.90))
                current_icu_occupied = int(icu_beds * np.random.uniform(0.50, 0.95))
                
                coords = CITY_COORDINATES.get(city, {"lat": 20.0, "lng": 78.0})
                
                cities_data.append({
                    "hospital_id": f"H{hospital_id}",
                    "hospital_name": f"{city} {h_type} Hospital #{hospital_id - 999}",
                    "hospital_type": h_type,
                    "city": city,
                    "state": state,
                    "latitude": coords["lat"] + np.random.uniform(-0.05, 0.05),
                    "longitude": coords["lng"] + np.random.uniform(-0.05, 0.05),
                    "total_beds": total_beds,
                    "icu_beds": icu_beds,
                    "emergency_beds": int(total_beds * 0.1),
                    "pediatric_beds": int(total_beds * 0.08),
                    "maternity_beds": int(total_beds * 0.06),
                    "current_occupied": current_occupied,
                    "current_icu_occupied": current_icu_occupied,
                    "free_beds": total_beds - current_occupied,
                    "free_icu_beds": icu_beds - current_icu_occupied,
                    "occupancy_pct": round(current_occupied / total_beds * 100, 1) if total_beds > 0 else 0,
                    "icu_occupancy_pct": round(current_icu_occupied / icu_beds * 100, 1) if icu_beds > 0 else 0
                })
                hospital_id += 1
    
    return pd.DataFrame(cities_data)


def save_generated_data():
    """Generate and save all synthetic datasets."""
    data_dir = os.path.join(os.path.dirname(__file__), "processed")
    os.makedirs(data_dir, exist_ok=True)
    
    print("[DATA] Generating daily admissions data (2 years)...")
    admissions_df = generate_daily_admissions(days=730)
    admissions_path = os.path.join(data_dir, "daily_admissions.csv")
    admissions_df.to_csv(admissions_path, index=False)
    print(f"   [OK] Saved {len(admissions_df)} records to {admissions_path}")
    
    print("[DATA] Generating hospital registry...")
    registry_df = generate_hospital_registry()
    registry_path = os.path.join(data_dir, "hospital_registry.csv")
    registry_df.to_csv(registry_path, index=False)
    print(f"   [OK] Saved {len(registry_df)} hospitals to {registry_path}")
    
    # Aggregate daily data for Prophet (city + disease level)
    print("[DATA] Creating aggregated time series...")
    agg_df = admissions_df.groupby(["date", "city", "disease"]).agg({
        "admissions": "sum",
        "icu_admissions": "sum",
        "bed_occupancy_pct": "mean",
        "icu_occupancy_pct": "mean",
        "temperature": "mean",
        "humidity": "mean",
        "rainfall_mm": "mean",
        "is_festival": "max"
    }).reset_index()
    
    agg_path = os.path.join(data_dir, "aggregated_timeseries.csv")
    agg_df.to_csv(agg_path, index=False)
    print(f"   [OK] Saved aggregated data to {agg_path}")
    
    return admissions_df, registry_df, agg_df


if __name__ == "__main__":
    save_generated_data()
