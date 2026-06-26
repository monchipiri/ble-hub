type DataStateProps = {
  isLoading: boolean;
  error: unknown;
  empty?: boolean;
  children: React.ReactNode;
};

export function DataState({ isLoading, error, empty, children }: DataStateProps) {
  if (isLoading) {
    return <div className="state-card">Cargando...</div>;
  }

  if (error) {
    return <div className="state-card error">Error cargando datos. Revisa que la API esté arrancada.</div>;
  }

  if (empty) {
    return <div className="state-card">Sin datos todavía.</div>;
  }

  return <>{children}</>;
}
