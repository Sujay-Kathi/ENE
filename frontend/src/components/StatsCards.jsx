import { Building2, Bed, HeartPulse, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react';

const cards = [
  { label: 'Total Hospitals', value: '69,800', change: '+2.1%', up: true, icon: Building2, variant: 'primary' },
  { label: 'Total Beds', value: '1.9M', change: '+1.4%', up: true, icon: Bed, variant: 'success' },
  { label: 'Free ICU Beds', value: '12,400', change: '-5.2%', up: false, icon: HeartPulse, variant: 'warning' },
  { label: 'Active Alerts', value: '8', change: '+3', up: true, icon: AlertTriangle, variant: 'danger' },
];

export default function StatsCards({ summary }) {
  const displayCards = summary ? [
    { ...cards[0], value: (summary.total_hospitals || 69800).toLocaleString() },
    { ...cards[1], value: ((summary.total_beds || 1900000) / 1000000).toFixed(1) + 'M' },
    { ...cards[2], value: (summary.total_free_icu || 12400).toLocaleString() },
    { ...cards[3], value: String(summary.critical_hospitals || 8) },
  ] : cards;

  return (
    <div className="stats-grid">
      {displayCards.map((card, i) => {
        const Icon = card.icon;
        return (
          <div key={i} className={`stat-card ${card.variant} animate-in`}>
            <div className={`stat-icon ${card.variant}`}>
              <Icon size={22} />
            </div>
            <div className="stat-label">{card.label}</div>
            <div className="stat-value">{card.value}</div>
            <span className={`stat-change ${card.up ? 'up' : 'down'}`}>
              {card.up ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
              {card.change}
            </span>
          </div>
        );
      })}
    </div>
  );
}
