import { apiFetch } from "./client";
import type { LoginResponse, User } from "../types/api";

export async function login(email: string, password: string): Promise<LoginResponse> {
  return apiFetch<LoginResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function fetchMe(): Promise<User> {
  return apiFetch<User>("/api/auth/me");
}

export async function fetchUsers(): Promise<User[]> {
  return apiFetch<User[]>("/api/users");
}
