import type { ActionType } from "../types/managementAction";
import type { PolicyStatus, PolicyType, WindowStatus } from "../types/policy";

const POLICY_TYPE_LABELS: Record<PolicyType, string> = {
  auto: "Auto",
  hogar: "Hogar",
  vida: "Vida",
};

const POLICY_STATUS_LABELS: Record<PolicyStatus, string> = {
  active: "Activa",
  renewed: "Renovada",
  lost: "Perdida",
};

const WINDOW_STATUS_LABELS: Record<WindowStatus, string> = {
  expiring: "Por vencer",
  in_window: "En ventana",
  out_of_window: "Fuera de ventana",
};

const ACTION_TYPE_LABELS: Record<ActionType, string> = {
  call_no_answer: "Llamada sin respuesta",
  call_success: "Llamada exitosa",
  renewal_scheduled: "Renovación agendada",
  renewed: "Renovada",
  lost: "Perdida",
  note: "Nota",
};

export function getPolicyTypeLabel(policyType: PolicyType | string): string {
  if (policyType in POLICY_TYPE_LABELS) {
    return POLICY_TYPE_LABELS[policyType as PolicyType];
  }
  return policyType;
}

export function getPolicyStatusLabel(status: PolicyStatus): string {
  return POLICY_STATUS_LABELS[status];
}

export function getWindowStatusLabel(
  windowStatus: WindowStatus | null,
): string {
  if (windowStatus === null) {
    return "—";
  }
  return WINDOW_STATUS_LABELS[windowStatus];
}

export function getActionTypeLabel(actionType: string): string {
  if (actionType in ACTION_TYPE_LABELS) {
    return ACTION_TYPE_LABELS[actionType as ActionType];
  }
  return actionType;
}

export function getActionTypeLabelFromEnum(actionType: ActionType): string {
  return ACTION_TYPE_LABELS[actionType];
}
