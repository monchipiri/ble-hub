import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { getBeaconStatus, startBeacon, stopBeacon } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { JsonBlock } from "../components/JsonBlock";

export function BeaconPage() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["beacon"], queryFn: getBeaconStatus });

  const start = useMutation({
    mutationFn: startBeacon,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["beacon"] })
  });

  const stop = useMutation({
    mutationFn: stopBeacon,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["beacon"] })
  });

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Baliza BLE</h2>
          <p>Estado de advertising BLE. En el backend actual es todavía un placeholder.</p>
        </div>
      </div>

      <DataState isLoading={query.isLoading} error={query.error}>
        <div className="panel">
          <div className="beacon-actions">
            <button onClick={() => start.mutate()} disabled={start.isPending}>Arrancar baliza</button>
            <button className="secondary" onClick={() => stop.mutate()} disabled={stop.isPending}>Parar baliza</button>
          </div>

          <JsonBlock value={query.data} />
        </div>
      </DataState>
    </section>
  );
}
