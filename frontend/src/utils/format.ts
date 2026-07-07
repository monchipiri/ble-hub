export function formatDateTime(value?: string | null): string {
  if (!value) {
    return "-";
  }

  return new Date(value).toLocaleString();
}

export function formatRssi(value?: number | null): string {
  return value === null || value === undefined ? "-" : `${value} dBm`;
}
