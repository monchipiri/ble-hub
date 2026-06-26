interface StatusBadgeProps {
  status: 'ok' | 'error' | 'unknown';
  label: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  return <span className={`status-badge status-${status}`}>{label}</span>;
}
