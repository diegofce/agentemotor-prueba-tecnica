export type ActionType =
  | "call_no_answer"
  | "call_success"
  | "renewal_scheduled"
  | "renewed"
  | "lost"
  | "note";

export interface ManagementActionCreatePayload {
  policy_id: number;
  action_type: ActionType;
  notes: string | null;
}

export interface PolicyRenewalPayload {
  new_expiration_date: string;
  notes: string | null;
}
