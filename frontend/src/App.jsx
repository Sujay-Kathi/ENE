import { useState } from 'react';
import './index.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <>
      <header className="fixed top-0 w-full z-50 flex justify-between items-center px-8 h-16 bg-surface-dim/80 backdrop-blur-xl border-b border-white/10 shadow-[0_0_20px_rgba(34,211,238,0.05)]">
        <div className="flex items-center gap-4">
          <span className="font-headline-md text-[24px] font-bold text-primary tracking-tight">FutureLens</span>
        </div>
        <div className="flex items-center gap-6">
          <div className="relative">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input className="bg-surface-container-low border border-white/10 rounded-lg pl-10 pr-4 py-1.5 text-sm text-on-surface focus:ring-1 focus:ring-primary focus:border-primary outline-none w-64" placeholder="Search Hospital Database..." type="text" />
          </div>
          <div className="flex items-center gap-4 border-l border-white/10 pl-6">
            <button className="active:scale-95 transition-transform hover:text-primary transition-colors duration-200">
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <button className="active:scale-95 transition-transform hover:text-primary transition-colors duration-200">
              <span className="material-symbols-outlined">settings</span>
            </button>
            <div className="w-8 h-8 rounded-full overflow-hidden border border-primary/20">
              <img alt="Chief Medical Officer Profile" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAjace7kak7-z6Wy5lonni3FhSgGdeWfSk8bkuQAweo_whPgZgFSO9GmKSvw1pQ-a8UyZwfHjwu24v2CcSaznPEsnX2pvWiGoIsUmDOBNnNJDojplDqE0li41_0AYqGjIjziTkSsdOlljdN-tQBM0o4n4V8CkN1Pj-YvyjqxHnDa__6ZGGubQJGDSswMiByx902C6MB6wVfk96QUFufwOGttxZiYDn1xPnd7Ck-xuRD0rQaFGNRHSsYW7E72rwdfGoRQ08pT9PaSOM" />
            </div>
          </div>
        </div>
      </header>

      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="ml-64 mt-16 p-8 min-h-screen space-y-6">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'predictions' && <Dashboard />}
        {activeTab === 'hospitals' && <Dashboard />}
        {activeTab === 'alerts' && <Dashboard />}
      </main>
    </>
  );
}

export default App;
