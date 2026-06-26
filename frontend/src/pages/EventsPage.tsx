import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { DataTable } from '../components/DataTable';
import { JsonBlock } from '../components/JsonBlock';
import type { BleEvent } from '../types/ble';

export function EventsPage() {
  const query = useQuery({ queryKey: ['events', 100], queryFn: () => api.events(100), refetchInterval: 3000 });

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Eventos</h1>
          <p>Últimos anuncios BLE registrados.</p>
        </div>
      </div>

      {query.isError && <div className="error-box">Error cargando eventos: {(query.error as Error).message}</div>}

      <DataTable<BleEvent>
        rows={query.data ?? []}
        emptyMessage="No hay eventos registrados."
        columns={[
          { key: 'created_at', header: 'Fecha', render: (row) => row.created_at ? new Date(row.created_at).toLocaleString() : '-' },
          { key: 'device_address', header: 'MAC', render: (row) => <code>{row.device_address}</code> },
          { key: 'local_name', header: 'Nombre', render: (row) => row.local_name || '-' },
          { key: 'rssi', header: 'RSSI', render: (row) => row.rssi ?? '-' },
          { key: 'payload', header: 'Payload', render: (row) => <JsonBlock value={row.payload} /> },
        ]}
      />
    </div>
  );
}
