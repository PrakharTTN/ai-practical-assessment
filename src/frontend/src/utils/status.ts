import type { TicketStatus } from "../types/api";

const ALLOWED: Record<TicketStatus, TicketStatus[]> = {
  open: ["in_progress", "cancelled"],
  in_progress: ["resolved", "cancelled"],
  resolved: ["closed"],
  closed: [],
  cancelled: [],
};

export function getAllowedTransitions(status: TicketStatus): TicketStatus[] {
  return ALLOWED[status] ?? [];
}

export function formatStatus(status: TicketStatus): string {
  return status.replace(/_/g, " ");
}

export function formatPriority(priority: string): string {
  return priority.charAt(0).toUpperCase() + priority.slice(1);
}
