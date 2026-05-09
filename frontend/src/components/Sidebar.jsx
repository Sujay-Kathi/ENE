const navItems = [
  { icon: 'dashboard', label: 'Dashboard', id: 'dashboard' },
  { icon: 'hub', label: 'Network', id: 'hospitals' },
  { icon: 'warning', label: 'Alerts', id: 'alerts' },
  { icon: 'assessment', label: 'Reports', id: 'predictions' },
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-64 flex flex-col py-8 bg-surface-container-lowest border-r border-white/5 pt-20">
      <div className="px-6 mb-8">
        <div className="flex items-center gap-3">
          <span className="material-symbols-outlined text-primary text-3xl">hub</span>
          <div>
            <h2 className="font-headline-md text-[24px] font-bold text-primary leading-tight">FutureLens</h2>
            <p className="font-label-caps text-[10px] text-on-surface-variant tracking-widest uppercase">Predictive Engine</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-1 px-4">
        {navItems.map(({ icon, label, id }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={`w-full flex items-center gap-3 px-4 py-3 transition-all ${
              activeTab === id 
                ? 'bg-primary-container/20 text-primary border-r-4 border-primary' 
                : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant/30'
            }`}
          >
            <span className="material-symbols-outlined">{icon}</span>
            <span className="font-label-caps text-[12px] font-bold uppercase tracking-widest">{label}</span>
          </button>
        ))}
      </nav>
      <div className="px-4 mt-auto space-y-1">
        <button className="w-full mb-6 bg-error-container text-on-error-container font-label-caps text-[12px] font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:brightness-110 active:scale-95 transition-all">
          <span className="material-symbols-outlined text-sm">emergency_home</span>
          EMERGENCY PROTOCOLS
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant hover:text-on-surface hover:bg-surface-variant/30 transition-all">
          <span className="material-symbols-outlined">help</span>
          <span className="font-label-caps text-[12px] font-bold uppercase tracking-widest">Support</span>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant hover:text-on-surface hover:bg-surface-variant/30 transition-all">
          <span className="material-symbols-outlined">settings</span>
          <span className="font-label-caps text-[12px] font-bold uppercase tracking-widest">Settings</span>
        </button>
      </div>
    </aside>
  );
}
