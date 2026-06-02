import type { ActionType } from "../types/managementAction";
import type { Policy } from "../types/policy";
import { ActionModal } from "./ActionModal";
import { PoliciesTable } from "./PoliciesTable";
import { RenewModal } from "./RenewModal";

interface PoliciesSectionProps {
  policies: Policy[];
  actionTypes: ActionType[];
  loading: boolean;
  error: string | null;
  actionTypesError: string | null;
  selectedActionPolicy: Policy | null;
  selectedRenewPolicy: Policy | null;
  onRegisterAction: (policy: Policy) => void;
  onRenew: (policy: Policy) => void;
  onCloseActionModal: () => void;
  onCloseRenewModal: () => void;
  onMutationSuccess: () => Promise<void>;
}

export function PoliciesSection({
  policies,
  actionTypes,
  loading,
  error,
  actionTypesError,
  selectedActionPolicy,
  selectedRenewPolicy,
  onRegisterAction,
  onRenew,
  onCloseActionModal,
  onCloseRenewModal,
  onMutationSuccess,
}: PoliciesSectionProps) {
  return (
    <section className="policies-section" aria-labelledby="policies-heading">
      <h2 id="policies-heading" className="section-title">
        Pólizas
      </h2>

      {error !== null && (
        <p className="inline-error section-error" role="alert">
          {error}
        </p>
      )}

      {actionTypesError !== null && (
        <p className="inline-error section-error" role="alert">
          {actionTypesError}
        </p>
      )}

      {loading && <p className="section-status">Cargando pólizas…</p>}

      {!loading && (
        <PoliciesTable
          policies={policies}
          onRegisterAction={onRegisterAction}
          onRenew={onRenew}
        />
      )}

      {selectedActionPolicy !== null && (
        <ActionModal
          policy={selectedActionPolicy}
          actionTypes={actionTypes}
          onClose={onCloseActionModal}
          onSuccess={onMutationSuccess}
        />
      )}

      {selectedRenewPolicy !== null && (
        <RenewModal
          policy={selectedRenewPolicy}
          onClose={onCloseRenewModal}
          onSuccess={onMutationSuccess}
        />
      )}
    </section>
  );
}
