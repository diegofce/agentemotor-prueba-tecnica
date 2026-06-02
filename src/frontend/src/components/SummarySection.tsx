import type { Summary } from "../types/summary";
import { SummaryCard } from "./SummaryCard";

interface SummarySectionProps {
  summary: Summary | null;
  loading: boolean;
  error: string | null;
}

export function SummarySection({
  summary,
  loading,
  error,
}: SummarySectionProps) {
  return (
    <section className="summary-section" aria-labelledby="summary-heading">
      <h1 id="summary-heading" className="page-title">
        Cartera de pólizas
      </h1>

      {error !== null && (
        <p className="inline-error section-error" role="alert">
          {error}
        </p>
      )}

      {loading && <p className="section-status">Cargando resumen…</p>}

      {!loading && error === null && summary !== null && (
        <div className="summary-grid">
          <SummaryCard label="Por vencer" value={summary.por_vencer} />
          <SummaryCard label="En ventana" value={summary.en_ventana} />
          <SummaryCard
            label="Fuera de ventana"
            value={summary.fuera_de_ventana}
          />
          <SummaryCard label="Renovadas" value={summary.renovadas} />
        </div>
      )}
    </section>
  );
}
