"""
hospitals.py — Hospital data API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/hospitals", tags=["hospitals"])


@router.get("/registry")
async def get_hospital_registry(
    city: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500)
):
    """Get hospital registry with bed availability."""
    from ..main import hospital_registry
    df = hospital_registry.copy()
    if city:
        df = df[df["city"].str.contains(city, case=False)]
    if state:
        df = df[df["state"].str.contains(state, case=False)]
    df = df.head(limit)
    return df.to_dict(orient="records")


@router.get("/summary")
async def get_national_summary():
    """Get national hospital statistics summary."""
    from ..main import hospital_registry
    from ..utils.helpers import get_national_summary
    return get_national_summary(hospital_registry)


@router.get("/city-stats")
async def get_city_stats(city: str = Query("Mumbai")):
    """Get hospital stats for a specific city."""
    from ..main import hospital_registry
    df = hospital_registry[hospital_registry["city"].str.contains(city, case=False)]
    if df.empty:
        return {"error": f"No data found for {city}"}
    return {
        "city": city,
        "hospitals": len(df),
        "total_beds": int(df["total_beds"].sum()),
        "icu_beds": int(df["icu_beds"].sum()),
        "free_beds": int(df["free_beds"].sum()),
        "free_icu_beds": int(df["free_icu_beds"].sum()),
        "avg_occupancy": round(float(df["occupancy_pct"].mean()), 1),
        "avg_icu_occupancy": round(float(df["icu_occupancy_pct"].mean()), 1),
        "critical_count": int((df["icu_occupancy_pct"] > 85).sum()),
        "hospitals_list": df[["hospital_id", "hospital_name", "hospital_type",
                              "total_beds", "free_beds", "icu_beds", "free_icu_beds",
                              "occupancy_pct", "icu_occupancy_pct",
                              "latitude", "longitude"]].to_dict(orient="records")
    }


@router.get("/map-data")
async def get_map_data():
    """Get hospital data formatted for map visualization."""
    from ..main import hospital_registry
    df = hospital_registry.copy()
    city_agg = df.groupby("city").agg({
        "total_beds": "sum", "icu_beds": "sum",
        "free_beds": "sum", "free_icu_beds": "sum",
        "occupancy_pct": "mean", "icu_occupancy_pct": "mean",
        "latitude": "mean", "longitude": "mean",
        "hospital_id": "count"
    }).reset_index()
    city_agg.columns = ["city", "total_beds", "icu_beds", "free_beds", "free_icu_beds",
                         "avg_occupancy", "avg_icu_occupancy", "lat", "lng", "hospital_count"]
    for col in ["avg_occupancy", "avg_icu_occupancy"]:
        city_agg[col] = city_agg[col].round(1)
    city_agg["risk_level"] = city_agg["avg_icu_occupancy"].apply(
        lambda x: "critical" if x > 85 else "high" if x > 70 else "moderate" if x > 55 else "low")
    return city_agg.to_dict(orient="records")


@router.get("/cities")
async def get_available_cities():
    """Get list of cities with hospital data."""
    from ..main import hospital_registry
    return sorted(hospital_registry["city"].unique().tolist())
