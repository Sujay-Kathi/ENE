import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const riskColors = {
  critical: '#ef4444',
  high: '#f59e0b',
  moderate: '#0ea5e9',
  low: '#10b981',
};

export default function HospitalMap({ mapData, loading }) {
  if (loading) {
    return (
      <div className="glass-card">
        <div className="glass-card-header">
          <span className="glass-card-title">Hospital Network — India</span>
        </div>
        <div className="loading-container"><div className="loading-spinner" /></div>
      </div>
    );
  }

  const cities = mapData || [];

  return (
    <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
      <div className="glass-card-header" style={{ padding: 'var(--space-6)' }}>
        <span className="glass-card-title">Hospital Network — India</span>
        <div style={{ display: 'flex', gap: '12px' }}>
          {Object.entries(riskColors).map(([level, color]) => (
            <div key={level} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: color, display: 'inline-block' }} />
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{level}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="map-container">
        <MapContainer
          center={[22.5, 78.9]}
          zoom={5}
          style={{ height: '100%', width: '100%' }}
          scrollWheelZoom={true}
          attributionControl={false}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          {cities.map((city, i) => (
            <CircleMarker
              key={i}
              center={[city.lat, city.lng]}
              radius={Math.max(8, Math.min(20, city.hospital_count / 2))}
              pathOptions={{
                color: riskColors[city.risk_level] || '#0ea5e9',
                fillColor: riskColors[city.risk_level] || '#0ea5e9',
                fillOpacity: 0.5,
                weight: 2,
              }}
            >
              <Popup>
                <div style={{ fontFamily: 'Inter', color: '#1e293b', minWidth: '180px' }}>
                  <strong style={{ fontSize: '14px' }}>{city.city}</strong>
                  <div style={{ fontSize: '12px', marginTop: '6px', lineHeight: '1.8' }}>
                    🏥 Hospitals: <strong>{city.hospital_count}</strong><br />
                    🛏️ Total Beds: <strong>{city.total_beds?.toLocaleString()}</strong><br />
                    ❤️ ICU Beds: <strong>{city.icu_beds?.toLocaleString()}</strong><br />
                    ✅ Free Beds: <strong>{city.free_beds?.toLocaleString()}</strong><br />
                    📊 Occupancy: <strong>{city.avg_occupancy?.toFixed(1)}%</strong><br />
                    🚨 ICU Load: <strong style={{ color: city.avg_icu_occupancy > 80 ? '#ef4444' : '#10b981' }}>
                      {city.avg_icu_occupancy?.toFixed(1)}%
                    </strong>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
