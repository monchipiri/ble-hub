export interface Device {
  id: number;
  address: string;
  name?: string | null;
  device_type?: string | null;
  notes?: string | null;
  last_rssi?: number | null;
  last_seen_at?: string | null;
  created_at?: string | null;
}

export interface BleEvent {
  id: number;
  source: string;
  device_address: string;
  local_name?: string | null;
  rssi?: number | null;
  service_uuids?: string[] | null;
  manufacturer_data?: Record<string, unknown> | null;
  payload?: Record<string, unknown> | null;
  created_at?: string | null;
}

export interface Rule {
  id: number;
  name: string;
  enabled: boolean;
  conditions: Record<string, unknown>;
  actions: Array<Record<string, unknown>>;
  created_at?: string | null;
}

export interface HealthResponse {
  status: string;
}
