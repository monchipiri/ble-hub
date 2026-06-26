import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { createRule, getRules } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { JsonBlock } from "../components/JsonBlock";

export function RulesPage() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["rules"], queryFn: getRules });

  const [name, setName] = useState("Dispositivo cerca");
  const [deviceAddress, setDeviceAddress] = useState("");
  const [rssiGt, setRssiGt] = useState("-70");
  const [message, setMessage] = useState("Dispositivo detectado cerca");

  const mutation = useMutation({
    mutationFn: createRule,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["rules"] });
    }
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();

    mutation.mutate({
      name,
      enabled: true,
      conditions: {
        ...(deviceAddress ? { device_address: deviceAddress } : {}),
        rssi_gt: Number(rssiGt)
      },
      actions: [
        {
          type: "alert",
          params: { message }
        }
      ]
    });
  }

  return (
    <section>
      <div className="page-header">
        <div>
          <h2>Reglas</h2>
          <p>Reglas configurables que disparan acciones cuando un evento BLE coincide.</p>
        </div>
      </div>

      <div className="split-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <h3>Nueva regla básica</h3>

          <label>
            Nombre
            <input value={name} onChange={(e) => setName(e.target.value)} />
          </label>

          <label>
            MAC del dispositivo
            <input
              placeholder="AA:BB:CC:DD:EE:FF"
              value={deviceAddress}
              onChange={(e) => setDeviceAddress(e.target.value)}
            />
          </label>

          <label>
            RSSI mayor que
            <input value={rssiGt} onChange={(e) => setRssiGt(e.target.value)} />
          </label>

          <label>
            Mensaje de alerta
            <input value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>

          <button type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Creando..." : "Crear regla"}
          </button>

          {mutation.error ? <div className="form-error">No se ha podido crear la regla.</div> : null}
        </form>

        <div>
          <DataState isLoading={query.isLoading} error={query.error} empty={!query.data?.length}>
            <div className="cards-list">
              {query.data?.map((rule) => (
                <article className="event-card" key={rule.id}>
                  <header>
                    <div>
                      <strong>{rule.name}</strong>
                      <p>{rule.enabled ? "Activa" : "Desactivada"}</p>
                    </div>
                    <span className={rule.enabled ? "badge success" : "badge"}>{rule.enabled ? "ON" : "OFF"}</span>
                  </header>
                  <JsonBlock value={{ conditions: rule.conditions, actions: rule.actions }} />
                </article>
              ))}
            </div>
          </DataState>
        </div>
      </div>
    </section>
  );
}
