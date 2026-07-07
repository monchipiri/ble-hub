import { useQuery } from "@tanstack/react-query";

import { getRuleTriggers } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { JsonBlock } from "../components/JsonBlock";
import { formatDateTime, formatRssi } from "../utils/format";

export function RuleTriggersPage() {
  const query = useQuery({
    queryKey: ["rule-triggers"],
    queryFn: () => getRuleTriggers(100),
    refetchInterval: 3000,
  });

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Reglas disparadas</h2>
          <p>Dispositivos que han provocado la ejecución de reglas.</p>
        </div>
      </div>

      <DataState isLoading={query.isLoading} error={query.error} empty={!query.data?.length}>
        <div className="cards-list">
          {query.data?.map((trigger) => (
            <article className="event-card" key={trigger.id}>
              <header>
                <div>
                  <strong>{trigger.rule_name}</strong>
                  <p className="mono">{trigger.device_address ?? "Sin MAC"}</p>
                </div>
                <span className="badge">RSSI {formatRssi(trigger.rssi)}</span>
              </header>

              <p>{trigger.local_name ?? "Sin nombre"}</p>
              <div className="event-meta">{formatDateTime(trigger.created_at)}</div>

              <JsonBlock value={{ actions: trigger.actions, payload: trigger.payload }} />
            </article>
          ))}
        </div>
      </DataState>
    </section>
  );
}
