import { FormEvent, useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchUsers } from "../api/auth";
import { ApiError, getFieldErrors } from "../api/client";
import {
  addComment,
  fetchTicket,
  updateTicket,
  updateTicketStatus,
} from "../api/tickets";
import { ErrorBanner } from "../components/ErrorBanner";
import type { Ticket, TicketPriority, TicketStatus, User } from "../types/api";
import {
  formatPriority,
  formatStatus,
  getAllowedTransitions,
} from "../utils/status";

export function TicketDetailPage() {
  const { id } = useParams<{ id: string }>();
  const ticketId = Number(id);

  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusError, setStatusError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [commentError, setCommentError] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<TicketPriority>("medium");
  const [assignedToId, setAssignedToId] = useState<string>("");

  const loadTicket = useCallback(async () => {
    if (!ticketId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTicket(ticketId);
      setTicket(data);
      setTitle(data.title);
      setDescription(data.description);
      setPriority(data.priority);
      setAssignedToId(data.assigned_to?.id?.toString() ?? "");
    } catch (err) {
      setError(err instanceof ApiError ? err.body.message : "Failed to load ticket.");
    } finally {
      setLoading(false);
    }
  }, [ticketId]);

  useEffect(() => {
    loadTicket();
    fetchUsers().then(setUsers).catch(() => setUsers([]));
  }, [loadTicket]);

  async function handleUpdate(e: FormEvent) {
    e.preventDefault();
    if (!ticket) return;
    setSaving(true);
    setError(null);
    setFieldErrors({});
    try {
      const updated = await updateTicket(ticket.id, {
        title,
        description,
        priority,
        assigned_to_id: assignedToId ? Number(assignedToId) : null,
      });
      setTicket(updated);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.body.message);
        setFieldErrors(getFieldErrors(err));
      } else {
        setError("Update failed.");
      }
    } finally {
      setSaving(false);
    }
  }

  async function handleStatusChange(target: TicketStatus) {
    if (!ticket) return;
    setStatusError(null);
    try {
      const updated = await updateTicketStatus(ticket.id, target);
      setTicket(updated);
      setTitle(updated.title);
      setDescription(updated.description);
      setPriority(updated.priority);
    } catch (err) {
      if (err instanceof ApiError) {
        setStatusError(err.body.message);
      } else {
        setStatusError("Status change failed.");
      }
    }
  }

  async function handleAddComment(e: FormEvent) {
    e.preventDefault();
    if (!ticket || !commentText.trim()) return;
    setCommentError(null);
    try {
      await addComment(ticket.id, commentText.trim());
      setCommentText("");
      await loadTicket();
    } catch (err) {
      setCommentError(err instanceof ApiError ? err.body.message : "Failed to add comment.");
    }
  }

  if (loading) {
    return <div className="loading-state">Loading ticket…</div>;
  }

  if (!ticket) {
    return (
      <div className="page-content">
        <ErrorBanner message={error} />
        <Link to="/tickets" className="btn btn-ghost">
          ← Back to tickets
        </Link>
      </div>
    );
  }

  const allowed = getAllowedTransitions(ticket.status);

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <p className="breadcrumb">
            <Link to="/tickets">Tickets</Link>
            <span>/</span>
            <span>#{ticket.id}</span>
          </p>
          <h2>{ticket.title}</h2>
          <div className="ticket-meta">
            <span className={`badge badge-${ticket.status}`}>
              {formatStatus(ticket.status)}
            </span>
            <span className={`badge badge-${ticket.priority}`}>
              {formatPriority(ticket.priority)}
            </span>
            <span className="meta-text">
              Created by {ticket.created_by.name} ·{" "}
              {new Date(ticket.created_at).toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      <ErrorBanner message={error} />
      <ErrorBanner message={statusError} />

      {allowed.length > 0 && (
        <section className="panel panel-status">
          <div className="panel-header">
            <h3>Workflow</h3>
            <p>Move this ticket to the next valid status</p>
          </div>
          <div className="status-actions">
            {allowed.map((s) => (
              <button
                key={s}
                type="button"
                className="btn btn-secondary"
                onClick={() => handleStatusChange(s)}
              >
                Mark as {formatStatus(s)}
              </button>
            ))}
          </div>
        </section>
      )}

      <div className="detail-grid">
        <form onSubmit={handleUpdate} className="panel">
          <div className="panel-header">
            <h3>Ticket Details</h3>
            <p>Update title, description, priority, or assignee</p>
          </div>
          <div className="stacked-form">
            <div className="form-group">
              <label htmlFor="edit-title">Title</label>
              <input
                id="edit-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
              {fieldErrors.title && <div className="field-error">{fieldErrors.title}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="edit-description">Description</label>
              <textarea
                id="edit-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="edit-priority">Priority</label>
                <select
                  id="edit-priority"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value as TicketPriority)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="edit-assignee">Assignee</label>
                <select
                  id="edit-assignee"
                  value={assignedToId}
                  onChange={(e) => setAssignedToId(e.target.value)}
                >
                  <option value="">Unassigned</option>
                  {users.map((u) => (
                    <option key={u.id} value={u.id}>
                      {u.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? "Saving…" : "Save Changes"}
            </button>
          </div>
        </form>

        <section className="panel">
          <div className="panel-header">
            <h3>Comments</h3>
            <p>Discussion and updates on this ticket</p>
          </div>
          <ErrorBanner message={commentError} />
          <ul className="comments-list">
            {(ticket.comments ?? []).length === 0 ? (
              <li className="empty-comment">No comments yet.</li>
            ) : (
              ticket.comments!.map((c) => (
                <li key={c.id}>
                  <div className="comment-meta">
                    {c.created_by.name} · {new Date(c.created_at).toLocaleString()}
                  </div>
                  <div className="comment-body">{c.message}</div>
                </li>
              ))
            )}
          </ul>
          <form onSubmit={handleAddComment} className="stacked-form comment-form">
            <div className="form-group">
              <label htmlFor="comment">Add comment</label>
              <textarea
                id="comment"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write an update…"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Post Comment
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}
