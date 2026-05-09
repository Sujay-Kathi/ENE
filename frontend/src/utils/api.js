const API_BASE = 'http://127.0.0.1:8000';

export async function fetchDiseaseTrend(city, disease, days = 30) {
  const res = await fetch(`${API_BASE}/api/predictions/disease-trend?city=${city}&disease=${disease}&days=${days}`);
  return res.json();
}

export async function fetchICUDemand(city, days = 14) {
  const res = await fetch(`${API_BASE}/api/predictions/icu-demand?city=${city}&days=${days}`);
  return res.json();
}

export async function fetchAllDiseases(city, days = 14) {
  const res = await fetch(`${API_BASE}/api/predictions/all-diseases?city=${city}&days=${days}`);
  return res.json();
}

export async function fetchFeatureImportance() {
  const res = await fetch(`${API_BASE}/api/predictions/feature-importance`);
  return res.json();
}

export async function fetchHospitalSummary() {
  const res = await fetch(`${API_BASE}/api/hospitals/summary`);
  return res.json();
}

export async function fetchCityStats(city) {
  const res = await fetch(`${API_BASE}/api/hospitals/city-stats?city=${city}`);
  return res.json();
}

export async function fetchMapData() {
  const res = await fetch(`${API_BASE}/api/hospitals/map-data`);
  return res.json();
}

export async function fetchCities() {
  const res = await fetch(`${API_BASE}/api/hospitals/cities`);
  return res.json();
}

export async function fetchAlerts(city, disease = 'dengue', days = 14) {
  const res = await fetch(`${API_BASE}/api/alerts/generate?city=${city}&disease=${disease}&days=${days}`);
  return res.json();
}

export async function fetchAllCityAlerts() {
  const res = await fetch(`${API_BASE}/api/alerts/all-cities`);
  return res.json();
}
