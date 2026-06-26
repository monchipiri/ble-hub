import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { DataTable } from '../components/DataTable';
import type { Device } from '../types/ble';

export function DevicesPage() {
  const query = useQuery({ queryKey: ['devices'], queryFn: api.devices, refetchInterval: 3000 });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Dispositivos</h1>
          <p>Últimos dispositivos BLE detectados por la Raspberry.</p>
        </div>
      </div>

      {query.isError && <div className="error-box">Error cargando dispositivos: {(query.error as Error).message}</div>}

      <DataTable<Device>
        rows={query.data ?? []}
        emptyMessage="No hay dispositivos detectados."
        columns={[
          { key: 'address', header: 'MAC', render: (row) => <code>{row.address}</code> },
          { key: 'name', header: 'Nombre', render: (row) => row.name || '-' },
          { key: 'rssi', header: 'RSSI', render: (row) => row.last_rssi ?? '-' },
          { key: 'last_seen_at', header: 'Última vez', render: (row) => row.last_seen_at ? new Date(row.last_seen_at).toLocaleString() : '-' },
        ]}
      />
    </div>
  );
}
