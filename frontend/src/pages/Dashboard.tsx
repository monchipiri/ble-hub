import { useQuery } from '@tanstack/react-query';
import { Activity, Bluetooth, Database, ShieldCheck } from 'lucide-react';
import { api } from '../api/client';
import { StatusBadge } from '../components/StatusBadge';

export function Dashboard() {
  const health = useQuery({ queryKey: ['health'], queryFn: api.health, refetchInterval: 10000 });
  const devices = useQuery({ queryKey: ['devices'], queryFn: api.devices, refetchInterval: 5000 });
  const events = useQuery({ queryKey: ['events', 20], queryFn: () => api.events(20), refetchInterval: 5000 });
  const rules = useQuery({ queryKey: ['rules'], queryFn: api.rules, refetchInterval: 10000 });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>BLE Hub</h1>
          <p>Panel de operación para el gateway BLE.</p>
        </div>
        <StatusBadge status={health.data?.status === 'ok' ? 'ok' : health.isError ? 'error' : 'unknown'} label={health.data?.status === 'ok' ? 'API online' : health.isError ? 'API error' : 'Checking'} />
      </div>

      <div className="cards-grid">
        <div className="card metric-card">
          <Bluetooth />
          <div>
            <span>Dispositivos</span>
            <strong>{devices.data?.length ?? '-'}</strong>
          </div>
        </div>
        <div className="card metric-card">
          <Activity />
          <div>
            <span>Eventos recientes</span>
            <strong>{events.data?.length ?? '-'}</strong>
          </div>
        </div>
        <div className="card metric-card">
          <ShieldCheck />
          <div>
            <span>Reglas</span>
            <strong>{rules.data?.length ?? '-'}</strong>
          </div>
        </div>
        <div className="card metric-card">
          <Database />
          <div>
            <span>Persistencia</span>
            <strong>{events.isError ? 'Error' : 'OK'}</strong>
          </div>
        </div>
      </div>
    </div>
  );
}
