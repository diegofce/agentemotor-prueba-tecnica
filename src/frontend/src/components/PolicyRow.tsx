import type { Policy } from "../types/policy";
import { formatDate, formatDateTime } from "../utils/format";
import {
  getActionTypeLabel,
  getPolicyStatusLabel,
  getPolicyTypeLabel,
} from "../utils/labels";
import { WindowStatusBadge } from "./WindowStatusBadge";

interface PolicyRowProps {
  policy: Policy;
  onRegisterAction: (policy: Policy) => void;
  onRenew: (policy: Policy) => void;
}

export function PolicyRow({
  policy,
  onRegisterAction,
  onRenew,
}: PolicyRowProps) {
  const canRenew = policy.status !== "renewed";

  return (
    <tr>
      <td>{policy.client_name ?? "—"}</td>
      <td>{getPolicyTypeLabel(policy.policy_type)}</td>
      <td>{formatDate(policy.expiration_date)}</td>
      <td>
        <WindowStatusBadge windowStatus={policy.window_status} />
      </td>
      <td>{getPolicyStatusLabel(policy.status)}</td>
      <td>
        {policy.last_action_at !== null ? (
          <>
            <span className="cell-primary">
              {policy.last_action !== null
                ? getActionTypeLabel(policy.last_action)
                : "—"}
            </span>
            <span className="cell-secondary">
              {formatDateTime(policy.last_action_at)}
            </span>
          </>
        ) : (
          "—"
        )}
      </td>
      <td className="actions-cell">
        <button
          type="button"
          className="btn btn-secondary btn-small"
          onClick={() => onRegisterAction(policy)}
        >
          Registrar gestión
        </button>
        {canRenew && (
          <button
            type="button"
            className="btn btn-primary btn-small"
            onClick={() => onRenew(policy)}
          >
            Renovar
          </button>
        )}
      </td>
    </tr>
  );
}
