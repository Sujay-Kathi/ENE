export default function StatsCards({ summary }) {
  const displayCards = summary ? [
    { label: 'Total Hospitals', value: (summary.total_hospitals || 69800).toLocaleString(), icon: 'local_hospital', type: 'normal' },
    { label: 'Total Beds', value: (summary.total_beds || 1900000).toLocaleString(), icon: 'bed', type: 'normal' },
    { label: 'Free ICU Beds', value: (summary.total_free_icu || 12400).toLocaleString(), icon: 'emergency', type: 'cyan' },
    { label: 'Active Alerts', value: String(summary.critical_hospitals || 8), icon: 'priority_high', type: 'red' },
  ] : [
    { label: 'Total Hospitals', value: '69,800', icon: 'local_hospital', type: 'normal' },
    { label: 'Total Beds', value: '1,900,000', icon: 'bed', type: 'normal' },
    { label: 'Free ICU Beds', value: '12,400', icon: 'emergency', type: 'cyan' },
    { label: 'Active Alerts', value: '8', icon: 'priority_high', type: 'red' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {displayCards.map((card, i) => {
        if (card.type === 'cyan') {
          return (
            <div key={i} className="glass-panel p-6 rounded-xl border-primary/30 neon-glow-cyan bg-primary-container/5">
              <p className="font-label-caps text-[12px] font-bold text-primary uppercase mb-2 tracking-widest">{card.label}</p>
              <div className="flex items-end justify-between">
                <div className="flex flex-col">
                  <span className="font-data-lg text-4xl text-primary font-bold">{card.value}</span>
                  <span className="text-[10px] text-primary/60 font-medium tracking-wider mt-1">REAL-TIME MONITOR</span>
                </div>
                <span className="material-symbols-outlined text-primary text-4xl animate-pulse">{card.icon}</span>
              </div>
            </div>
          );
        } else if (card.type === 'red') {
          return (
            <div key={i} className="glass-panel p-6 rounded-xl border-secondary-container/50 neon-glow-red bg-secondary-container/10">
              <p className="font-label-caps text-[12px] font-bold text-secondary uppercase mb-2 tracking-widest">{card.label}</p>
              <div className="flex items-end justify-between">
                <div className="flex flex-col">
                  <span className="font-data-lg text-4xl text-secondary font-bold">{card.value}</span>
                  <span className="text-[10px] text-secondary/60 font-medium tracking-wider mt-1">IMMEDIATE ATTENTION</span>
                </div>
                <span className="material-symbols-outlined text-secondary text-4xl">{card.icon}</span>
              </div>
            </div>
          );
        } else {
          return (
            <div key={i} className="glass-panel p-6 rounded-xl">
              <p className="font-label-caps text-[12px] font-bold text-on-surface-variant uppercase mb-2 tracking-widest">{card.label}</p>
              <div className="flex items-end justify-between">
                <span className="font-data-lg text-4xl text-on-surface font-bold">{card.value}</span>
                <span className="material-symbols-outlined text-primary/40 text-4xl">{card.icon}</span>
              </div>
            </div>
          );
        }
      })}
    </div>
  );
}
