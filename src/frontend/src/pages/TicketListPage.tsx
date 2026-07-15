import { FormEvent, useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ApiError } from "../api/client";
import { exportTicketsCsv, fetchTickets } from "../api/tickets";
import { ErrorBanner } from "../components/ErrorBanner";
import type { Ticket, TicketPriority, TicketStatus } from "../types/api";
import { formatPriority, formatStatus } from "../utils/status";

export function TicketListPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<TicketStatus | "">("");
  const [priorityFilter, setPriorityFilter] = useState<TicketPriority | "">("");
  const [search, setSearch] = useState("");
  const [exporting, setExporting] = useState(false);

  const loadTickets = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTickets({
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
        search: search.trim() || undefined,
      });
      setTickets(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.body.message : "Failed to load tickets.");
    } finally {
      setLoading(false);
    }
  }, [statusFilter, priorityFilter, search]);

  useEffect(() => {
    loadTickets();
  }, [loadTickets]);

  function handleFilterSubmit(e: FormEvent) {
    e.preventDefault();
    loadTickets();
  }

  async function handleExport() {
    setExporting(true);
    setError(null);
    try {
      const csv = await exportTicketsCsv();
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "tickets_export.csv";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof ApiError ? err.body.message : "Export failed.");
    } finally {
      setExporting(false);
    }
  }

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2>All Tickets</h2>
          <p className="page-subtitle">Track, filter, and export support requests</p>
        </div>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={handleExport}
          disabled={exporting}
        >
          {exporting ? "Exporting…" : "Export My Tickets"}
        </button>
      </div>

      <ErrorBanner message={error} />

      <section className="panel panel-filters">
        <form className="filters" onSubmit={handleFilterSubmit}>
          <div className="form-group">
            <label htmlFor="search">Search title</label>
            <input
              id="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search tickets…"
            />
          </div>
          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select
              id="status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as TicketStatus | "")}
            >
              <option value="">All statuses</option>
              <option value="open">Open</option>
              <option value="in_progress">In progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="priority">Priority</label>
            <select
              id="priority"
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value as TicketPriority | "")}
            >
              <option value="">All priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <button type="submit" className="btn btn-primary">
            Apply Filters
          </button>
        </form>
      </section>

      <section className="panel panel-table">
        {loading ? (
          <div className="loading-state">Loading tickets…</div>
        ) : tickets.length === 0 ? (
          <div className="empty-state">
            <p>No tickets match your filters.</p>
            <Link to="/tickets/new" className="btn btn-primary">
              Create a ticket
            </Link>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Priority</th>
                  <th>Assignee</th>
                  <th>Created by</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => (
                  <tr key={t.id}>
                    <td className="cell-muted">#{t.id}</td>
                    <td>
                      <Link to={`/tickets/${t.id}`} className="table-link">
                        {t.title}
                      </Link>
                    </td>
                    <td>
                      <span className={`badge badge-${t.status}`}>
                        {formatStatus(t.status)}
                      </span>
                    </td>
                    <td>
                      <span className={`badge badge-${t.priority}`}>
                        {formatPriority(t.priority)}
                      </span>
                    </td>
                    <td>{t.assigned_to?.name ?? "—"}</td>
                    <td>{t.created_by.name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
