import { apiFetch } from "./client";
import type { User, UserRole } from "../types/api";

export interface UserCreateInput {
  name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface UserUpdateInput {
  name?: string;
  email?: string;
  password?: string;
  role?: UserRole;
}

export async function createUser(input: UserCreateInput): Promise<User> {
  return apiFetch<User>("/api/users", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateUser(id: number, input: UserUpdateInput): Promise<User> {
  return apiFetch<User>(`/api/users/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}
