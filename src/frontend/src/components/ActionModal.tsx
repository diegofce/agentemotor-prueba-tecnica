import { useEffect, useState, type FormEvent } from "react";
import { createPolicyAction } from "../api/policies";
import type { ActionType } from "../types/managementAction";
import type { Policy } from "../types/policy";
import { getActionTypeLabelFromEnum } from "../utils/labels";
import { Modal } from "./Modal";

interface ActionModalProps {
  policy: Policy;
  actionTypes: ActionType[];
  onClose: () => void;
  onSuccess: () => Promise<void>;
}

export function ActionModal({
  policy,
  actionTypes,
  onClose,
  onSuccess,
}: ActionModalProps) {
  const [actionType, setActionType] = useState<ActionType | "">("");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (actionType === "" && actionTypes.length > 0) {
      setActionType(actionTypes[0]);
    }
  }, [actionType, actionTypes]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (actionType === "") {
      setError("Seleccione un tipo de gestión");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await createPolicyAction(policy.id, {
        policy_id: policy.id,
        action_type: actionType,
        notes: notes.trim() === "" ? null : notes.trim(),
      });
      await onSuccess();
      onClose();
    } catch (submitError: unknown) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "No se pudo registrar la gestión",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal
      title={`Registrar gestión — ${policy.client_name ?? "Cliente"}`}
      onClose={onClose}
    >
      <form className="modal-form" onSubmit={handleSubmit}>
        {error !== null && (
          <p className="inline-error" role="alert">
            {error}
          </p>
        )}

        <label className="field">
          <span className="field-label">Tipo de gestión</span>
          <select
            className="field-control"
            value={actionType}
            onChange={(event) =>
              setActionType(event.target.value as ActionType | "")
            }
            required
            disabled={submitting || actionTypes.length === 0}
          >
            {actionTypes.length === 0 && (
              <option value="">Sin opciones disponibles</option>
            )}
            {actionTypes.map((option) => (
              <option key={option} value={option}>
                {getActionTypeLabelFromEnum(option)}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field-label">Notas</span>
          <textarea
            className="field-control field-textarea"
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            rows={4}
            disabled={submitting}
          />
        </label>

        <div className="modal-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClose}
            disabled={submitting}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting || actionTypes.length === 0}
          >
            {submitting ? "Guardando…" : "Guardar gestión"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
