import { useState, type FormEvent } from "react";
import { renewPolicy } from "../api/policies";
import type { Policy } from "../types/policy";
import { todayIsoDate } from "../utils/format";
import { Modal } from "./Modal";

interface RenewModalProps {
  policy: Policy;
  onClose: () => void;
  onSuccess: () => Promise<void>;
}

export function RenewModal({ policy, onClose, onSuccess }: RenewModalProps) {
  const [newExpiryDate, setNewExpiryDate] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (newExpiryDate === "") {
      setError("Indique la nueva fecha de vencimiento");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await renewPolicy(policy.id, {
        new_expiration_date: newExpiryDate,
        notes: null,
      });
      await onSuccess();
      onClose();
    } catch (submitError: unknown) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "No se pudo renovar la póliza",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Modal
      title={`Renovar póliza — ${policy.client_name ?? "Cliente"}`}
      onClose={onClose}
    >
      <form className="modal-form" onSubmit={handleSubmit}>
        {error !== null && (
          <p className="inline-error" role="alert">
            {error}
          </p>
        )}

        <label className="field">
          <span className="field-label">Nueva fecha de vencimiento</span>
          <input
            type="date"
            className="field-control"
            value={newExpiryDate}
            min={todayIsoDate()}
            onChange={(event) => setNewExpiryDate(event.target.value)}
            required
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
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Renovando…" : "Confirmar renovación"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
