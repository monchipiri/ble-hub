import { useQuery } from "@tanstack/react-query";

import { getDevices, getEvents, getHealth, getRules } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { StatCard } from "../components/StatCard";

export function DashboardPage() {
  const health = useQuery({ queryKey: ["health"], queryFn: getHealth });
  const devices = useQuery({ queryKey: ["devices"], queryFn: getDevices });
  const events = useQuery({ queryKey: ["events", 20], queryFn: () => getEvents(20) });
  const rules = useQuery({ queryKey: ["rules"], queryFn: getRules });

  const hasError = health.error || devices.error || events.error || rules.error;

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Resumen operativo del gateway BLE.</p>
        </div>
        <span className={health.data?.status === "ok" ? "badge success" : "badge"}>
          API {health.data?.status ?? "desconocida"}
        </span>
      </div>

      <DataState isLoading={health.isLoading || devices.isLoading || events.isLoading || rules.isLoading} error={hasError}>
        <div className="stats-grid">
          <StatCard label="Dispositivos" value={devices.data?.length ?? 0} hint="Detectados por el scanner" />
          <StatCard label="Eventos recientes" value={events.data?.length ?? 0} hint="Última consulta" />
          <StatCard label="Reglas" value={rules.data?.length ?? 0} hint="Configuradas en backend" />
          <StatCard label="API" value={health.data?.status ?? "-"} hint="Estado de FastAPI" />
        </div>

        <div className="panel">
          <h3>Últimos dispositivos vistos</h3>
          <table>
            <thead>
              <tr>
                <th>MAC</th>
                <th>Nombre</th>
                <th>RSSI</th>
                <th>Última vez</th>
              </tr>
            </thead>
            <tbody>
              {(devices.data ?? []).slice(0, 8).map((device) => (
                <tr key={device.id}>
                  <td className="mono">{device.address}</td>
                  <td>{device.name ?? "-"}</td>
                  <td>{device.last_rssi ?? "-"}</td>
                  <td>{device.last_seen_at ? new Date(device.last_seen_at).toLocaleString() : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </DataState>
    </section>
  );
}
