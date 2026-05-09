import { LayoutDashboard, TrendingUp, Building2, AlertTriangle, Settings } from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard' },
  { icon: TrendingUp, label: 'Predictions', id: 'predictions' },
  { icon: Building2, label: 'Hospitals', id: 'hospitals' },
  { icon: AlertTriangle, label: 'Alerts', id: 'alerts' },
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">FL</div>
      <nav className="sidebar-nav">
        {navItems.map(({ icon: Icon, label, id }) => (
          <button
            key={id}
            className={`sidebar-item ${activeTab === id ? 'active' : ''}`}
            onClick={() => setActiveTab(id)}
            title={label}
          >
            <Icon />
          </button>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <button className="sidebar-item" title="Settings">
          <Settings />
        </button>
      </div>
    </aside>
  );
}
