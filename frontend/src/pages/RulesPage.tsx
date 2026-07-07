import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Power, PowerOff } from "lucide-react";

import { createRule, getRules, patchRule } from "../api/bleHubApi";
import { DataState } from "../components/DataState";
import { JsonBlock } from "../components/JsonBlock";

export function RulesPage() {
  const queryClient = useQueryClient();
  const query = useQuery({ queryKey: ["rules"], queryFn: getRules });

  const [name, setName] = useState("Dispositivo cerca");
  const [deviceAddress, setDeviceAddress] = useState("");
  const [rssiGt, setRssiGt] = useState("-70");
  const [message, setMessage] = useState("Dispositivo detectado cerca");
  const [formError, setFormError] = useState<string | null>(null);

  const createMutation = useMutation({
    mutationFn: createRule,
    onSuccess: async () => {
      setFormError(null);
      await queryClient.invalidateQueries({ queryKey: ["rules"] });
    }
  });

  const toggleMutation = useMutation({
    mutationFn: ({ ruleId, enabled }: { ruleId: number; enabled: boolean }) =>
      patchRule(ruleId, { enabled }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["rules"] });
    }
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const trimmedName = name.trim();
    const trimmedAddress = deviceAddress.trim();
    const rssiThreshold = Number(rssiGt);

    if (!trimmedName) {
      setFormError("El nombre de la regla es obligatorio.");
      return;
    }

    if (!Number.isFinite(rssiThreshold)) {
      setFormError("RSSI debe ser un número válido.");
      return;
    }

    setFormError(null);

    createMutation.mutate({
      name: trimmedName,
      enabled: true,
      conditions: {
        ...(trimmedAddress ? { device_address: trimmedAddress } : {}),
        rssi_gt: rssiThreshold
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
            <input type="number" value={rssiGt} onChange={(e) => setRssiGt(e.target.value)} />
          </label>

          <label>
            Mensaje de alerta
            <input value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>

          <button type="submit" disabled={createMutation.isPending}>
            <Plus size={18} />
            {createMutation.isPending ? "Creando..." : "Crear regla"}
          </button>

          {formError ? <div className="form-error">{formError}</div> : null}
          {createMutation.error ? <div className="form-error">No se ha podido crear la regla.</div> : null}
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
                    <div className="card-actions">
                      <span className={rule.enabled ? "badge success" : "badge"}>
                        {rule.enabled ? "ON" : "OFF"}
                      </span>
                      <button
                        className="icon-button secondary"
                        type="button"
                        title={rule.enabled ? "Desactivar regla" : "Activar regla"}
                        onClick={() =>
                          toggleMutation.mutate({ ruleId: rule.id, enabled: !rule.enabled })
                        }
                        disabled={toggleMutation.isPending}
                      >
                        {rule.enabled ? <PowerOff size={18} /> : <Power size={18} />}
                      </button>
                    </div>
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
