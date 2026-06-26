import { useState } from 'react';
import { Activity, Bluetooth, Gauge, ShieldCheck } from 'lucide-react';
import { Dashboard } from './pages/Dashboard';
import { DevicesPage } from './pages/DevicesPage';
import { EventsPage } from './pages/EventsPage';
import { RulesPage } from './pages/RulesPage';

type Page = 'dashboard' | 'devices' | 'events' | 'rules';

export function App() {
  const [page, setPage] = useState<Page>('dashboard');

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Bluetooth />
          <div>
            <strong>BLE Hub</strong>
            <span>Gateway</span>
          </div>
        </div>

        <nav>
          <button className={page === 'dashboard' ? 'active' : ''} onClick={() => setPage('dashboard')}><Gauge /> Dashboard</button>
          <button className={page === 'devices' ? 'active' : ''} onClick={() => setPage('devices')}><Bluetooth /> Devices</button>
          <button className={page === 'events' ? 'active' : ''} onClick={() => setPage('events')}><Activity /> Events</button>
          <button className={page === 'rules' ? 'active' : ''} onClick={() => setPage('rules')}><ShieldCheck /> Rules</button>
        </nav>
      </aside>

      <main>
        {page === 'dashboard' && <Dashboard />}
        {page === 'devices' && <DevicesPage />}
        {page === 'events' && <EventsPage />}
        {page === 'rules' && <RulesPage />}
      </main>
    </div>
  );
}
