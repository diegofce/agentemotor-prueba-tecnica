export type PolicyType = "auto" | "hogar" | "vida";

export type PolicyStatus = "active" | "renewed" | "lost";

export type WindowStatus = "expiring" | "in_window" | "out_of_window";

export interface Policy {
  id: number;
  client_id: number;
  insurer: string;
  policy_type: PolicyType;
  policy_number: string | null;
  expiration_date: string;
  status: PolicyStatus;
  created_at: string;
  updated_at: string;
  client_name: string | null;
  client_phone: string | null;
  window_status: WindowStatus | null;
  days_overdue: number | null;
  days_remaining_in_window: number | null;
  last_action: string | null;
  last_action_at: string | null;
  total_actions: number | null;
}
