import { useState, useEffect } from 'react';
import StatsCards from './StatsCards';
import ForecastChart from './ForecastChart';
import RiskGauge from './RiskGauge';
import AlertPanel from './AlertPanel';
import HospitalMap from './HospitalMap';
import {
  fetchDiseaseTrend, fetchICUDemand, fetchHospitalSummary,
  fetchAlerts, fetchMapData, fetchAllCityAlerts, fetchFeatureImportance
} from '../utils/api';

const CITIES = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Kolkata',
  'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
  'Kochi', 'Bhopal', 'Patna', 'Chandigarh', 'Bhubaneswar'];
const DISEASES = ['dengue', 'malaria', 'flu', 'covid', 'respiratory', 'gastro'];

export default function Dashboard() {
  const [city, setCity] = useState('Mumbai');
  const [disease, setDisease] = useState('dengue');
  const [days, setDays] = useState(30);
  const [forecast, setForecast] = useState(null);
  const [icuData, setIcuData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [mapData, setMapData] = useState(null);
  const [features, setFeatures] = useState(null);
  const [loading, setLoading] = useState({});
  const [useFallback, setUseFallback] = useState(false);

  // Fallback data generator
  const generateFallback = () => {
    const today = new Date();
    const preds = Array.from({ length: days }, (_, i) => {
      const d = new Date(today);
      d.setDate(d.getDate() + i);
      const base = 30 + Math.sin(i / 5) * 15 + Math.random() * 10;
      return {
        date: d.toISOString().split('T')[0],
        predicted: Math.round(base * 10) / 10,
        lower_bound: Math.round((base * 0.7) * 10) / 10,
        upper_bound: Math.round((base * 1.3) * 10) / 10,
      };
    });
    const pv = preds.map(p => p.predicted);
    const pi = pv.indexOf(Math.max(...pv));
    return {
      city, disease, forecast_days: days, predictions: preds,
      trend_direction: pv[pv.length - 1] > pv[0] ? 'rising' : 'falling',
      peak_date: preds[pi].date,
      peak_value: Math.round(Math.max(...pv) * 10) / 10,
      avg_predicted: Math.round(pv.reduce((a, b) => a + b, 0) / pv.length * 10) / 10,
    };
  };

  const generateFallbackICU = () => {
    const today = new Date();
    return {
      city, forecast_days: 14,
      predictions: Array.from({ length: 14 }, (_, i) => {
        const d = new Date(today);
        d.setDate(d.getDate() + i);
        const occ = 55 + Math.random() * 35;
        return {
          date: d.toISOString().split('T')[0],
          icu_occupancy_pct: Math.round(occ * 10) / 10,
          crisis_probability: occ > 85 ? 0.75 : occ > 70 ? 0.45 : 0.15,
          risk_level: occ > 85 ? 'critical' : occ > 70 ? 'high' : occ > 55 ? 'moderate' : 'low',
        };
      }),
      model_metrics: { mae: 4.82, rmse: 6.31, crisis_accuracy: 0.87 },
    };
  };

  const generateFallbackAlerts = () => ({
    city,
    alerts: [
      { type: 'icu_crisis', severity: 'critical', title: `ICU Capacity Crisis — ${city}`,
        message: `ICU occupancy predicted to reach 92% by ${new Date(Date.now() + 3 * 86400000).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}`,
        recommendation: 'Activate overflow protocols. Delay non-critical procedures.',
        timestamp: new Date().toISOString() },
      { type: 'disease_surge', severity: 'high', title: `Dengue Outbreak Warning — ${city}`,
        message: 'Dengue cases expected to rise by 45% in the next 14 days.',
        recommendation: 'Increase dengue treatment supplies and staff.',
        timestamp: new Date().toISOString() },
      { type: 'icu_warning', severity: 'medium', title: `Respiratory Cases Rising — ${city}`,
        message: 'Winter respiratory admissions trending 20% above baseline.',
        recommendation: 'Prepare additional ventilators and respiratory care staff.',
        timestamp: new Date().toISOString() },
    ],
    total_alerts: 3,
  });

  const generateFallbackMap = () =>
    [{ city: 'Mumbai', lat: 19.076, lng: 72.877, hospital_count: 28, total_beds: 8500, icu_beds: 620, free_beds: 2100, free_icu_beds: 85, avg_occupancy: 75.3, avg_icu_occupancy: 86.3, risk_level: 'critical' },
     { city: 'Delhi', lat: 28.614, lng: 77.209, hospital_count: 32, total_beds: 9200, icu_beds: 710, free_beds: 3100, free_icu_beds: 120, avg_occupancy: 66.3, avg_icu_occupancy: 83.1, risk_level: 'high' },
     { city: 'Bengaluru', lat: 12.972, lng: 77.595, hospital_count: 24, total_beds: 7200, icu_beds: 540, free_beds: 2800, free_icu_beds: 95, avg_occupancy: 61.1, avg_icu_occupancy: 82.4, risk_level: 'high' },
     { city: 'Chennai', lat: 13.083, lng: 80.271, hospital_count: 22, total_beds: 6800, icu_beds: 490, free_beds: 2400, free_icu_beds: 110, avg_occupancy: 64.7, avg_icu_occupancy: 77.6, risk_level: 'moderate' },
     { city: 'Kolkata', lat: 22.573, lng: 88.364, hospital_count: 20, total_beds: 5900, icu_beds: 380, free_beds: 1800, free_icu_beds: 65, avg_occupancy: 69.5, avg_icu_occupancy: 82.9, risk_level: 'high' },
     { city: 'Hyderabad', lat: 17.385, lng: 78.487, hospital_count: 21, total_beds: 6400, icu_beds: 460, free_beds: 2200, free_icu_beds: 90, avg_occupancy: 65.6, avg_icu_occupancy: 80.4, risk_level: 'moderate' },
     { city: 'Pune', lat: 18.52, lng: 73.857, hospital_count: 18, total_beds: 5200, icu_beds: 370, free_beds: 1900, free_icu_beds: 75, avg_occupancy: 63.5, avg_icu_occupancy: 79.7, risk_level: 'moderate' },
     { city: 'Ahmedabad', lat: 23.023, lng: 72.571, hospital_count: 16, total_beds: 4800, icu_beds: 320, free_beds: 1600, free_icu_beds: 60, avg_occupancy: 66.7, avg_icu_occupancy: 81.3, risk_level: 'high' },
     { city: 'Jaipur', lat: 26.912, lng: 75.787, hospital_count: 14, total_beds: 3800, icu_beds: 260, free_beds: 1400, free_icu_beds: 55, avg_occupancy: 63.2, avg_icu_occupancy: 78.8, risk_level: 'moderate' },
     { city: 'Lucknow', lat: 26.847, lng: 80.946, hospital_count: 15, total_beds: 4100, icu_beds: 280, free_beds: 1500, free_icu_beds: 50, avg_occupancy: 63.4, avg_icu_occupancy: 82.1, risk_level: 'high' },
    ];

  const loadData = async () => {
    setLoading({ forecast: true, icu: true, summary: true, alerts: true, map: true });
    try {
      const [f, icu, sum, al, map, featsRes] = await Promise.all([
        fetchDiseaseTrend(city, disease, days).catch(() => null),
        fetchICUDemand(city, 14).catch(() => null),
        fetchHospitalSummary().catch(() => null),
        fetchAlerts(city, disease, 14).catch(() => null),
        fetchMapData().catch(() => null),
        fetchFeatureImportance().catch(() => null),
      ]);

      if (!f && !icu && !sum) {
        setUseFallback(true);
        setForecast(generateFallback());
        setIcuData(generateFallbackICU());
        setSummary({ total_hospitals: 69800, total_beds: 1900000, total_free_icu: 12400, critical_hospitals: 8 });
        setAlerts(generateFallbackAlerts());
        setMapData(generateFallbackMap());
      } else {
        setUseFallback(false);
        setForecast(f || generateFallback());
        setIcuData(icu || generateFallbackICU());
        setSummary(sum || { total_hospitals: 69800, total_beds: 1900000, total_free_icu: 12400, critical_hospitals: 8 });
        setAlerts(al || generateFallbackAlerts());
        setMapData(map || generateFallbackMap());
        if (featsRes) setFeatures(featsRes);
      }
    } catch {
      setUseFallback(true);
      setForecast(generateFallback());
      setIcuData(generateFallbackICU());
      setSummary({ total_hospitals: 69800, total_beds: 1900000, total_free_icu: 12400, critical_hospitals: 8 });
      setAlerts(generateFallbackAlerts());
      setMapData(generateFallbackMap());
    }
    setLoading({});
  };

  useEffect(() => { loadData(); }, [city, disease, days]);

  return (
    <div>
      <div className="page-header">
        <div className="header-row">
          <div>
            <h1>🔮 FutureLens Dashboard</h1>
            <p>Predicting Disease Trends & Hospital Resource Demand — India</p>
          </div>
          <div className="header-controls">
            <select className="select-input" value={city} onChange={e => setCity(e.target.value)}>
              {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
            <select className="select-input" value={disease} onChange={e => setDisease(e.target.value)}>
              {DISEASES.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
            </select>
            <select className="select-input" value={days} onChange={e => setDays(Number(e.target.value))}>
              {[7, 14, 30, 60].map(d => <option key={d} value={d}>{d} Days</option>)}
            </select>
          </div>
        </div>
      </div>

      {useFallback && (
        <div style={{ background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.3)', borderRadius: 'var(--radius-lg)', padding: '12px 16px', marginBottom: '24px', fontSize: '13px', color: 'var(--warning)' }}>
          ⚡ Running in demo mode — Start the backend server for live predictions: <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '4px' }}>uvicorn backend.app.main:app --reload</code>
        </div>
      )}

      <StatsCards summary={summary} />

      <div className="content-grid thirds">
        <ForecastChart forecast={forecast} disease={disease} loading={loading.forecast} />
        <RiskGauge icuData={icuData} loading={loading.icu} />
      </div>

      <div className="content-grid">
        <HospitalMap mapData={mapData} loading={loading.map} />
        <AlertPanel alerts={alerts} loading={loading.alerts} />
      </div>

      {/* Feature Importance */}
      <div className="content-grid" style={{ marginTop: '0' }}>
        <div className="glass-card">
          <div className="glass-card-header">
            <span className="glass-card-title">XGBoost Feature Importance</span>
            {icuData?.model_metrics && (
              <div style={{ display: 'flex', gap: '16px' }}>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>MAE: <strong style={{ color: 'var(--success)' }}>{icuData.model_metrics.mae}</strong></span>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>RMSE: <strong style={{ color: 'var(--primary)' }}>{icuData.model_metrics.rmse}</strong></span>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Accuracy: <strong style={{ color: 'var(--tertiary)' }}>{(icuData.model_metrics.crisis_accuracy * 100).toFixed(1)}%</strong></span>
              </div>
            )}
          </div>
          {(() => {
            const feats = features || {
              base_cases: 0.25, weekday: 0.12, weekly_pattern: 0.08, month: 0.15,
              seasonal_spike: 0.10, dengue_cases: 0.15, temperature: 0.05,
              rainfall: 0.05, total_cases: 0.05
            };
            const maxVal = Math.max(...Object.values(feats));
            const labels = {
              base_cases: 'Base Admission Count',
              weekday: 'Day of Week',
              weekly_pattern: 'Weekend/Weekday Pattern',
              month: 'Month of Year',
              seasonal_spike: 'Seasonal Outbreak Factor',
              dengue_cases: 'Dengue Co-infection',
              temperature: 'Temperature',
              rainfall: 'Rainfall (mm)',
              total_cases: 'Total Combined Cases',
            };
            return Object.entries(feats)
              .sort(([, a], [, b]) => b - a)
              .map(([key, val]) => (
                <div className="feature-bar-container" key={key}>
                  <div className="feature-bar-label">
                    <span className="feature-bar-name">{labels[key] || key}</span>
                    <span className="feature-bar-value">{(val * 100).toFixed(1)}%</span>
                  </div>
                  <div className="feature-bar-track">
                    <div className="feature-bar-fill" style={{ width: `${(val / maxVal) * 100}%` }} />
                  </div>
                </div>
              ));
          })()}
        </div>
        <div className="glass-card">
          <div className="glass-card-header">
            <span className="glass-card-title">Decision Support</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { icon: '🏥', title: 'Increase ICU Capacity', desc: `Based on rising ${disease} trends in ${city}, prepare 20% additional ICU beds.`, priority: 'high' },
              { icon: '👨‍⚕️', title: 'Staff Reallocation', desc: 'Redeploy nursing staff from low-occupancy departments to emergency and ICU.', priority: 'medium' },
              { icon: '💊', title: 'Supply Procurement', desc: `Order additional ${disease} treatment supplies for predicted surge.`, priority: 'high' },
              { icon: '🚑', title: 'Transfer Protocols', desc: 'Activate inter-hospital patient transfer for non-critical cases.', priority: 'low' },
              { icon: '📢', title: 'Public Advisory', desc: 'Issue regional health advisory for upcoming disease outbreak risk.', priority: 'medium' },
            ].map((rec, i) => (
              <div key={i} style={{
                background: 'rgba(0,0,0,0.2)', borderRadius: '12px', padding: '14px 16px',
                display: 'flex', gap: '12px', alignItems: 'flex-start',
                border: '1px solid transparent', transition: 'border-color 0.2s',
              }}
                onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--border)'}
                onMouseLeave={e => e.currentTarget.style.borderColor = 'transparent'}
              >
                <span style={{ fontSize: '20px' }}>{rec.icon}</span>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '2px' }}>
                    {rec.title} <span className={`badge ${rec.priority}`} style={{ marginLeft: '8px' }}>{rec.priority}</span>
                  </div>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{rec.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
