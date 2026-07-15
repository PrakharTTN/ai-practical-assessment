import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchUsers } from "../api/auth";
import { ApiError, getFieldErrors } from "../api/client";
import { createTicket } from "../api/tickets";
import { ErrorBanner } from "../components/ErrorBanner";
import type { TicketPriority, User } from "../types/api";

export function CreateTicketPage() {
  const navigate = useNavigate();
  const [users, setUsers] = useState<User[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<TicketPriority>("medium");
  const [assignedToId, setAssignedToId] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers().then(setUsers).catch(() => setUsers([]));
  }, []);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setFieldErrors({});
    setLoading(true);
    try {
      const ticket = await createTicket({
        title,
        description,
        priority,
        assigned_to_id: assignedToId ? Number(assignedToId) : null,
      });
      navigate(`/tickets/${ticket.id}`);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.body.message);
        setFieldErrors(getFieldErrors(err));
      } else {
        setError("Failed to create ticket.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-content page-content-narrow">
      <div className="page-header">
        <div>
          <p className="breadcrumb">
            <Link to="/tickets">Tickets</Link>
            <span>/</span>
            <span>New</span>
          </p>
          <h2>Create Ticket</h2>
          <p className="page-subtitle">Submit a new support request</p>
        </div>
      </div>

      <ErrorBanner message={error} />

      <section className="panel">
        <form onSubmit={handleSubmit} className="stacked-form">
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Brief summary of the issue"
              required
            />
            {fieldErrors.title && <div className="field-error">{fieldErrors.title}</div>}
          </div>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Provide details to help the team resolve this"
              required
            />
            {fieldErrors.description && (
              <div className="field-error">{fieldErrors.description}</div>
            )}
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <select
                id="priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value as TicketPriority)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="assignee">Assignee (optional)</label>
              <select
                id="assignee"
                value={assignedToId}
                onChange={(e) => setAssignedToId(e.target.value)}
              >
                <option value="">Unassigned</option>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.name} ({u.email})
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="form-actions">
            <Link to="/tickets" className="btn btn-ghost">
              Cancel
            </Link>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Creating…" : "Create Ticket"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
