import { useQuery } from "@tanstack/react-query";
import { getRuleTriggers } from "../api/bleHubApi";

export function RuleTriggersPage() {
  const query = useQuery({
    queryKey: ["rule-triggers"],
    queryFn: () => getRuleTriggers(100),
    refetchInterval: 3000,
  });

  if (query.isLoading) return <div>Cargando disparos...</div>;
  if (query.error) return <div>Error cargando reglas disparadas</div>;

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Reglas disparadas</h2>
          <p>Dispositivos que han provocado la ejecución de reglas.</p>
        </div>
      </div>

      <div className="cards-list">
        {query.data?.map((trigger: any) => (
          <article className="event-card" key={trigger.id}>
            <header>
              <div>
                <strong>{trigger.rule_name}</strong>
                <p className="mono">{trigger.device_address}</p>
              </div>
              <span className="badge">RSSI {trigger.rssi ?? "-"}</span>
            </header>

            <p>{trigger.local_name ?? "Sin nombre"}</p>
            <div className="event-meta">
              {new Date(trigger.created_at).toLocaleString()}
            </div>

            <pre className="json-block">
              {JSON.stringify(
                {
                  actions: trigger.actions,
                  payload: trigger.payload,
                },
                null,
                2
              )}
            </pre>
          </article>
        ))}
      </div>
    </section>
  );
}
