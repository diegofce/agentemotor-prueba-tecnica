import type { Policy } from "../types/policy";
import { PolicyRow } from "./PolicyRow";

interface PoliciesTableProps {
  policies: Policy[];
  onRegisterAction: (policy: Policy) => void;
  onRenew: (policy: Policy) => void;
}

export function PoliciesTable({
  policies,
  onRegisterAction,
  onRenew,
}: PoliciesTableProps) {
  return (
    <div className="table-wrapper">
      <table className="policies-table">
        <thead>
          <tr>
            <th>Cliente</th>
            <th>Tipo</th>
            <th>Vencimiento</th>
            <th>Window status</th>
            <th>Estado</th>
            <th>Última gestión</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {policies.length === 0 ? (
            <tr>
              <td colSpan={7} className="empty-row">
                No hay pólizas para mostrar.
              </td>
            </tr>
          ) : (
            policies.map((policy) => (
              <PolicyRow
                key={policy.id}
                policy={policy}
                onRegisterAction={onRegisterAction}
                onRenew={onRenew}
              />
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
