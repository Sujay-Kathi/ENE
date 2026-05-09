import { useEffect, useState } from 'react';

export default function RiskGauge({ icuData, loading }) {
  const [animatedValue, setAnimatedValue] = useState(0);

  // Get current occupancy from prediction data or default
  const occupancy = icuData?.predictions?.[0]?.icu_occupancy_pct || 72;
  const riskLevel = icuData?.predictions?.[0]?.risk_level || 'moderate';
  const crisisProb = icuData?.predictions?.[0]?.crisis_probability || 0.35;

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedValue(occupancy), 300);
    return () => clearTimeout(timer);
  }, [occupancy]);

  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedValue / 100) * circumference;

  const getColor = (val) => {
    if (val >= 85) return '#ef4444';
    if (val >= 70) return '#f59e0b';
    if (val >= 55) return '#0ea5e9';
    return '#10b981';
  };

  const color = getColor(animatedValue);

  if (loading) {
    return (
      <div className="glass-card">
        <div className="loading-container"><div className="loading-spinner" /></div>
      </div>
    );
  }

  return (
    <div className="glass-card">
      <div className="glass-card-header">
        <span className="glass-card-title">ICU Occupancy</span>
        <span className={`badge ${riskLevel}`}>{riskLevel}</span>
      </div>
      <div className="gauge-wrapper">
        <svg className="gauge-svg" viewBox="0 0 200 200">
          <circle className="gauge-bg" cx="100" cy="100" r={radius} />
          <circle
            className="gauge-fill"
            cx="100" cy="100" r={radius}
            stroke={color}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ filter: `drop-shadow(0 0 8px ${color}60)` }}
          />
        </svg>
        <div className="gauge-center">
          <div className="gauge-value" style={{ color }}>{Math.round(animatedValue)}%</div>
          <div className="gauge-label">Current ICU Utilization</div>
        </div>
      </div>
      <div style={{ textAlign: 'center', marginTop: '8px' }}>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
          Crisis Probability: <span style={{ color: crisisProb > 0.5 ? 'var(--danger)' : 'var(--primary)', fontWeight: 600 }}>
            {(crisisProb * 100).toFixed(0)}%
          </span>
        </p>
      </div>
      {/* Mini forecast preview */}
      {icuData?.predictions && (
        <div style={{ display: 'flex', gap: '8px', marginTop: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
          {icuData.predictions.slice(0, 5).map((p, i) => (
            <div key={i} style={{
              background: 'rgba(0,0,0,0.25)', borderRadius: '8px', padding: '6px 10px',
              textAlign: 'center', minWidth: '56px'
            }}>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                {new Date(p.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
              </div>
              <div style={{ fontSize: '14px', fontWeight: 600, color: getColor(p.icu_occupancy_pct) }}>
                {Math.round(p.icu_occupancy_pct)}%
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
