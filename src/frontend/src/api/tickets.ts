import { apiFetch } from "./client";
import type {
  Comment,
  Ticket,
  TicketCreateInput,
  TicketPriority,
  TicketStatus,
  TicketUpdateInput,
} from "../types/api";

export async function fetchTickets(params?: {
  status?: TicketStatus;
  priority?: TicketPriority;
  search?: string;
}): Promise<Ticket[]> {
  const query = new URLSearchParams();
  if (params?.status) query.set("status", params.status);
  if (params?.priority) query.set("priority", params.priority);
  if (params?.search) query.set("search", params.search);
  const qs = query.toString();
  return apiFetch<Ticket[]>(`/api/tickets${qs ? `?${qs}` : ""}`);
}

export async function fetchTicket(id: number): Promise<Ticket> {
  return apiFetch<Ticket>(`/api/tickets/${id}`);
}

export async function createTicket(input: TicketCreateInput): Promise<Ticket> {
  return apiFetch<Ticket>("/api/tickets", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateTicket(
  id: number,
  input: TicketUpdateInput,
): Promise<Ticket> {
  return apiFetch<Ticket>(`/api/tickets/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function updateTicketStatus(
  id: number,
  status: TicketStatus,
): Promise<Ticket> {
  return apiFetch<Ticket>(`/api/tickets/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

export async function addComment(
  ticketId: number,
  message: string,
): Promise<Comment> {
  return apiFetch<Comment>(`/api/tickets/${ticketId}/comments`, {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

export async function exportTicketsCsv(): Promise<string> {
  return apiFetch<string>("/api/tickets/export");
}
