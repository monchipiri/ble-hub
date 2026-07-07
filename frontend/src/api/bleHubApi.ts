import { api } from "./client";
import type {
  BeaconStatus,
  BleDevice,
  BleEvent,
  HealthResponse,
  Rule,
  RuleTrigger
} from "../types/api";

export async function getHealth(): Promise<HealthResponse> {
  const response = await api.get<HealthResponse>("/health");
  return response.data;
}

export async function getDevices(): Promise<BleDevice[]> {
  const response = await api.get<BleDevice[]>("/devices");
  return response.data;
}

export async function getEvents(limit = 50): Promise<BleEvent[]> {
  const response = await api.get<BleEvent[]>("/events", { params: { limit } });
  return response.data;
}

export async function getRules(): Promise<Rule[]> {
  const response = await api.get<Rule[]>("/rules");
  return response.data;
}

export async function createRule(payload: {
  name: string;
  enabled: boolean;
  conditions: Record<string, unknown>;
  actions: Array<Record<string, unknown>>;
}): Promise<Rule> {
  const response = await api.post<Rule>("/rules", payload);
  return response.data;
}

export async function patchRule(
  ruleId: number,
  payload: Partial<Pick<Rule, "name" | "enabled" | "conditions" | "actions">>
): Promise<Rule> {
  const response = await api.patch<Rule>(`/rules/${ruleId}`, payload);
  return response.data;
}

export async function getBeaconStatus(): Promise<BeaconStatus> {
  const response = await api.get<BeaconStatus>("/beacon/status");
  return response.data;
}

export async function startBeacon(payload: Record<string, unknown> = {}): Promise<BeaconStatus> {
  const response = await api.post<BeaconStatus>("/beacon/start", { payload });
  return response.data;
}

export async function stopBeacon(): Promise<BeaconStatus> {
  const response = await api.post<BeaconStatus>("/beacon/stop");
  return response.data;
}

export async function getRuleTriggers(limit = 100): Promise<RuleTrigger[]> {
  const response = await api.get<RuleTrigger[]>("/rule-triggers", { params: { limit } });
  return response.data;
}
