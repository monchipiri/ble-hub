import { useQuery } from "@tanstack/react-query";

import { getEvents } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { JsonBlock } from "../components/JsonBlock";
import { formatDateTime, formatRssi } from "../utils/format";

export function EventsPage() {
  const query = useQuery({ queryKey: ["events", 100], queryFn: () => getEvents(100) });

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Eventos</h2>
          <p>Últimos anuncios BLE registrados en PostgreSQL.</p>
        </div>
      </div>

      <DataState isLoading={query.isLoading} error={query.error} empty={!query.data?.length}>
        <div className="cards-list">
          {query.data?.map((event) => (
            <article className="event-card" key={event.id}>
              <header>
                <div>
                  <strong className="mono">{event.device_address ?? "Sin MAC"}</strong>
                  <p>{event.local_name ?? "Sin nombre"}</p>
                </div>
                <span className="badge">RSSI {formatRssi(event.rssi)}</span>
              </header>
              <div className="event-meta">{formatDateTime(event.created_at)}</div>
              <JsonBlock
                value={{
                  service_uuids: event.service_uuids,
                  manufacturer_data: event.manufacturer_data,
                  payload: event.payload
                }}
              />
            </article>
          ))}
        </div>
      </DataState>
    </section>
  );
}
