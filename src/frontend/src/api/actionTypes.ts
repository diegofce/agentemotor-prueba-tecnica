import { API_BASE_URL } from "./config";
import type { ActionType } from "../types/managementAction";

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
  const response = await fetch(`${API_BASE_URL}/openapi.json`);
  if (!response.ok) {
    throw new Error("No se pudieron cargar los tipos de gestión");
  }

  const document = (await response.json()) as OpenApiDocument;
  const schema = document.components?.schemas?.ManagementActionCreate;
  const enumValues = schema?.properties?.action_type?.enum ?? [];

  return enumValues.filter(isActionType);
}
