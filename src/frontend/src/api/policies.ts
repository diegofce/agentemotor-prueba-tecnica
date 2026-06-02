import { apiRequest } from "./client";
import type {
  ManagementActionCreatePayload,
  PolicyRenewalPayload,
} from "../types/managementAction";
import type { Policy } from "../types/policy";

export function fetchPolicies(): Promise<Policy[]> {
  return apiRequest<Policy[]>("/policies");
}

export function createPolicyAction(
  policyId: number,
  payload: ManagementActionCreatePayload,
): Promise<void> {
  return apiRequest<void>(`/policies/${policyId}/actions`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function renewPolicy(
  policyId: number,
  payload: PolicyRenewalPayload,
): Promise<Policy> {
  return apiRequest<Policy>(`/policies/${policyId}/renew`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
