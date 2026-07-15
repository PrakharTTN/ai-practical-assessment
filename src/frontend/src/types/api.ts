export type UserRole = "agent" | "admin";
export type TicketPriority = "low" | "medium" | "high";
export type TicketStatus =
  | "open"
  | "in_progress"
  | "resolved"
  | "closed"
  | "cancelled";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface Comment {
  id: number;
  message: string;
  created_by: User;
  created_at: string;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  priority: TicketPriority;
  status: TicketStatus;
  assigned_to: User | null;
  created_by: User;
  created_at: string;
  updated_at: string;
  comments?: Comment[];
}

export interface ApiErrorBody {
  error: string;
  message: string;
  details?: Record<string, string[]>;
  current_status?: string;
  requested_status?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface TicketCreateInput {
  title: string;
  description: string;
  priority: TicketPriority;
  assigned_to_id?: number | null;
}

export interface TicketUpdateInput {
  title?: string;
  description?: string;
  priority?: TicketPriority;
  assigned_to_id?: number | null;
}
