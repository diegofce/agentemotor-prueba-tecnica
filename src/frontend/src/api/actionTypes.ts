import { DEFAULT_ACTION_TYPES } from "../constants/actionTypes";
import type { ActionType } from "../types/managementAction";
import { API_BASE_URL } from "./config";

interface OpenApiSchema {
  properties?: {
    action_type?: {
      enum?: string[];
    };
  };
}

interface OpenApiDocument {
  components?: {
    schemas?: Record<string, OpenApiSchema>;
  };
}

function isActionType(value: string): value is ActionType {
  return (
    value === "call_no_answer" ||
    value === "call_success" ||
    value === "renewal_scheduled" ||
    value === "renewed" ||
    value === "lost" ||
    value === "note"
  );
}

export async function fetchActionTypes(): Promise<ActionType[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/openapi.json`);
    if (!response.ok) {
      return DEFAULT_ACTION_TYPES;
    }

    const document = (await response.json()) as OpenApiDocument;
    const schema = document.components?.schemas?.ManagementActionCreate;
    const enumValues = schema?.properties?.action_type?.enum ?? [];
    const parsed = enumValues.filter(isActionType);

    return parsed.length > 0 ? parsed : DEFAULT_ACTION_TYPES;
  } catch {
    return DEFAULT_ACTION_TYPES;
  }
}
