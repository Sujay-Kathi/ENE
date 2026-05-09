import { useState } from 'react';
import './index.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="app-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="main-content">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'predictions' && <Dashboard />}
        {activeTab === 'hospitals' && <Dashboard />}
        {activeTab === 'alerts' && <Dashboard />}
      </main>
    </div>
  );
}

export default App;
