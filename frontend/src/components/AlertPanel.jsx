import { AlertTriangle, ShieldAlert, Info } from 'lucide-react';

export default function AlertPanel({ alerts, loading }) {
  if (loading) {
    return (
      <div className="glass-card">
        <div className="loading-container"><div className="loading-spinner" /></div>
      </div>
    );
  }

  const alertList = alerts?.alerts || [];

  const getIcon = (severity) => {
    if (severity === 'critical') return <ShieldAlert size={16} />;
    if (severity === 'high') return <AlertTriangle size={16} />;
    return <Info size={16} />;
  };

  return (
    <div className="glass-card">
      <div className="glass-card-header">
        <span className="glass-card-title">Active Crisis Warnings</span>
        <span className="badge critical">{alertList.length} Active</span>
      </div>
      <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
        {alertList.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px', fontSize: '13px' }}>
            No active alerts. System operating normally.
          </p>
        ) : (
          alertList.slice(0, 8).map((alert, i) => (
            <div key={i} className={`alert-item ${alert.severity}`}>
              <div className={`alert-dot ${alert.severity}`} />
              <div style={{ flex: 1 }}>
                <div className="alert-title">
                  {getIcon(alert.severity)} {alert.title}
                </div>
                <div className="alert-message">{alert.message}</div>
                {alert.recommendation && (
                  <div style={{ fontSize: '11px', color: 'var(--primary-light)', marginTop: '6px', fontStyle: 'italic' }}>
                    💡 {alert.recommendation}
                  </div>
                )}
                <div className="alert-time">
                  {new Date(alert.timestamp).toLocaleString('en-IN', { 
                    hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short' 
                  })}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
