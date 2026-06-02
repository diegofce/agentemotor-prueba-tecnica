import { apiRequest } from "./client";
import type { Summary } from "../types/summary";

export function fetchSummary(): Promise<Summary> {
  return apiRequest<Summary>("/summary");
}
