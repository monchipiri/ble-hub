import { FormEvent, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import { DataTable } from '../components/DataTable';
import { JsonBlock } from '../components/JsonBlock';
import type { Rule } from '../types/ble';

export function RulesPage() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ['rules'], queryFn: api.rules, refetchInterval: 10000 });
  const [name, setName] = useState('Dispositivo cerca');
  const [deviceAddress, setDeviceAddress] = useState('');
  const [rssiGt, setRssiGt] = useState('-70');
  const [message, setMessage] = useState('Dispositivo detectado cerca');

  const mutation = useMutation({
    mutationFn: api.createRule,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['rules'] }),
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    mutation.mutate({
      name,
      enabled: true,
      conditions: {
        ...(deviceAddress ? { device_address: deviceAddress } : {}),
        rssi_gt: Number(rssiGt),
      },
      actions: [
        {
          type: 'alert',
          params: { message },
        },
      ],
    });
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Reglas</h1>
          <p>Reglas configurables para disparar acciones.</p>
        </div>
      </div>

      <div className="card form-card">
        <h2>Nueva regla simple</h2>
        <form onSubmit={handleSubmit} className="rule-form">
          <label>
            Nombre
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
          <label>
            MAC del dispositivo
            <input value={deviceAddress} onChange={(event) => setDeviceAddress(event.target.value)} placeholder="AA:BB:CC:DD:EE:FF" />
          </label>
          <label>
            RSSI mayor que
            <input type="number" value={rssiGt} onChange={(event) => setRssiGt(event.target.value)} />
          </label>
          <label>
            Mensaje alerta
            <input value={message} onChange={(event) => setMessage(event.target.value)} />
          </label>
          <button type="submit" disabled={mutation.isPending}>{mutation.isPending ? 'Creando...' : 'Crear regla'}</button>
        </form>
        {mutation.isError && <div className="error-box">Error creando regla: {(mutation.error as Error).message}</div>}
      </div>

      {query.isError && <div className="error-box">Error cargando reglas: {(query.error as Error).message}</div>}

      <DataTable<Rule>
        rows={query.data ?? []}
        emptyMessage="No hay reglas configuradas."
        columns={[
          { key: 'name', header: 'Nombre', render: (row) => row.name },
          { key: 'enabled', header: 'Activa', render: (row) => row.enabled ? 'Sí' : 'No' },
          { key: 'conditions', header: 'Condiciones', render: (row) => <JsonBlock value={row.conditions} /> },
          { key: 'actions', header: 'Acciones', render: (row) => <JsonBlock value={row.actions} /> },
        ]}
      />
    </div>
  );
}
