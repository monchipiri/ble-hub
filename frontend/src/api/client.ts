import type { BleEvent, Device, HealthResponse, Rule } from '../types/ble';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>('/health'),
  devices: () => request<Device[]>('/devices'),
  events: (limit = 50) => request<BleEvent[]>(`/events?limit=${limit}`),
  rules: () => request<Rule[]>('/rules'),
  createRule: (payload: Omit<Rule, 'id' | 'created_at'>) =>
    request<Rule>('/rules', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
