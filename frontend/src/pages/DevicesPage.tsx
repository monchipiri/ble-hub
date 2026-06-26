import { useQuery } from "@tanstack/react-query";

import { getDevices } from "../api/bleHubApi";
import { DataState } from "../components/DataState";

export function DevicesPage() {
  const query = useQuery({ queryKey: ["devices"], queryFn: getDevices });

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Dispositivos</h2>
          <p>Dispositivos BLE detectados y último estado conocido.</p>
        </div>
      </div>

      <DataState isLoading={query.isLoading} error={query.error} empty={!query.data?.length}>
        <div className="panel">
          <table>
            <thead>
              <tr>
                <th>MAC</th>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>RSSI</th>
                <th>Última detección</th>
              </tr>
            </thead>
            <tbody>
              {query.data?.map((device) => (
                <tr key={device.id}>
                  <td className="mono">{device.address}</td>
                  <td>{device.name ?? "-"}</td>
                  <td>{device.device_type ?? "-"}</td>
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
