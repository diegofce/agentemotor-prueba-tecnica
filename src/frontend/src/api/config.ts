function normalizeBaseUrl(value: string | undefined): string {
  if (value === undefined || value.trim() === "") {
    return "";
  }
  return value.trim().replace(/\/+$/, "");
}

export const API_BASE_URL: string = normalizeBaseUrl(
  import.meta.env.VITE_API_BASE_URL,
);
