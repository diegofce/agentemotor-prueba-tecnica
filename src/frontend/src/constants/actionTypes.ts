import type { ActionType } from "../types/managementAction";

export const DEFAULT_ACTION_TYPES: ActionType[] = [
  "call_no_answer",
  "call_success",
  "renewal_scheduled",
  "renewed",
  "lost",
  "note",
];
