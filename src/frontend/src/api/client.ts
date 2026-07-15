import { API_BASE_URL } from "../config/api";
import type { ApiErrorBody } from "../types/api";

const TOKEN_KEY = "ticket_auth_token";

export class ApiError extends Error {
  constructor(
    public status: number,
    public body: ApiErrorBody,
  ) {
    super(body.message);
    this.name = "ApiError";
  }
}

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  sessionStorage.removeItem(TOKEN_KEY);
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  const token = getToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("text/csv")) {
    return (await response.text()) as T;
  }

  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    throw new ApiError(response.status, data as ApiErrorBody);
  }

  return data as T;
}

export function getFieldErrors(error: ApiError): Record<string, string> {
  const out: Record<string, string> = {};
  if (error.body.details) {
    for (const [field, messages] of Object.entries(error.body.details)) {
      out[field] = messages[0] ?? "Invalid value";
    }
  }
  return out;
}
