import { useEffect, useRef, useState } from 'react';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Filler, Tooltip, Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default function ForecastChart({ forecast, disease, loading }) {
  if (loading) {
    return (
      <div className="glass-card">
        <div className="loading-container"><div className="loading-spinner" /><p className="loading-text">Loading forecast...</p></div>
      </div>
    );
  }

  if (!forecast || !forecast.predictions || forecast.predictions.length === 0) {
    return (
      <div className="glass-card">
        <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px' }}>Select a city and disease to view forecast</p>
      </div>
    );
  }

  const labels = forecast.predictions.map(p => {
    const d = new Date(p.date);
    return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
  });

  const data = {
    labels,
    datasets: [
      {
        label: 'Upper Bound',
        data: forecast.predictions.map(p => p.upper_bound),
        borderColor: 'transparent',
        backgroundColor: 'rgba(14, 165, 233, 0.08)',
        fill: '+1',
        pointRadius: 0,
        tension: 0.4,
      },
      {
        label: `${disease.charAt(0).toUpperCase() + disease.slice(1)} — Predicted Cases`,
        data: forecast.predictions.map(p => p.predicted),
        borderColor: '#0ea5e9',
        backgroundColor: 'rgba(14, 165, 233, 0.15)',
        fill: false,
        pointRadius: 2,
        pointHoverRadius: 6,
        pointBackgroundColor: '#0ea5e9',
        pointBorderColor: '#0ea5e9',
        pointHoverBackgroundColor: '#fff',
        borderWidth: 2.5,
        tension: 0.4,
      },
      {
        label: 'Lower Bound',
        data: forecast.predictions.map(p => p.lower_bound),
        borderColor: 'transparent',
        backgroundColor: 'rgba(14, 165, 233, 0.08)',
        fill: false,
        pointRadius: 0,
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        align: 'end',
        labels: {
          color: '#88929b',
          font: { family: 'Inter', size: 11 },
          usePointStyle: true,
          pointStyleWidth: 8,
          filter: (item) => item.text.includes('Predicted'),
        },
      },
      tooltip: {
        backgroundColor: 'rgba(13, 19, 38, 0.95)',
        borderColor: 'rgba(14, 165, 233, 0.3)',
        borderWidth: 1,
        titleFont: { family: 'Inter', size: 12, weight: '600' },
        bodyFont: { family: 'Inter', size: 12 },
        titleColor: '#dae2fd',
        bodyColor: '#bec8d2',
        padding: 12,
        cornerRadius: 8,
        displayColors: false,
      },
    },
    scales: {
      x: {
        grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
        ticks: { color: '#88929b', font: { family: 'Inter', size: 11 }, maxRotation: 0, maxTicksLimit: 10 },
      },
      y: {
        grid: { color: 'rgba(255,255,255,0.04)', drawBorder: false },
        ticks: { color: '#88929b', font: { family: 'Inter', size: 11 } },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="glass-card">
      <div className="glass-card-header">
        <div>
          <span className="glass-card-title">Disease Trend Forecast</span>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            {forecast.forecast_days}-day forecast • Trend: <span style={{ color: forecast.trend_direction === 'rising' ? 'var(--warning)' : 'var(--success)', fontWeight: 600 }}>
              {forecast.trend_direction === 'rising' ? '↑ Rising' : '↓ Falling'}
            </span> • Peak: {forecast.peak_value} cases on {new Date(forecast.peak_date).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
          </p>
        </div>
        <span className={`badge ${forecast.trend_direction === 'rising' ? 'high' : 'low'}`}>
          {forecast.trend_direction}
        </span>
      </div>
      <div className="chart-container">
        <Line data={data} options={options} />
      </div>
    </div>
  );
}
