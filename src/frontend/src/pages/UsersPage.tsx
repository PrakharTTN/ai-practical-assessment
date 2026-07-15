import { FormEvent, useCallback, useEffect, useState } from "react";
import { fetchUsers } from "../api/auth";
import { ApiError, getFieldErrors } from "../api/client";
import { createUser, updateUser } from "../api/users";
import { ErrorBanner } from "../components/ErrorBanner";
import type { User, UserRole } from "../types/api";

function formatRole(role: UserRole): string {
  return role === "admin" ? "Admin" : "Support";
}

const EMPTY_FORM = {
  name: "",
  email: "",
  password: "",
  role: "agent" as UserRole,
};

export function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const [name, setName] = useState(EMPTY_FORM.name);
  const [email, setEmail] = useState(EMPTY_FORM.email);
  const [password, setPassword] = useState(EMPTY_FORM.password);
  const [role, setRole] = useState<UserRole>(EMPTY_FORM.role);

  const loadUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.body.message : "Failed to load users.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  function resetForm() {
    setEditingUser(null);
    setName(EMPTY_FORM.name);
    setEmail(EMPTY_FORM.email);
    setPassword(EMPTY_FORM.password);
    setRole(EMPTY_FORM.role);
    setFieldErrors({});
  }

  function startEdit(user: User) {
    setEditingUser(user);
    setName(user.name);
    setEmail(user.email);
    setPassword("");
    setRole(user.role);
    setFieldErrors({});
    setError(null);
    setSuccess(null);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setFieldErrors({});
    setSubmitting(true);
    try {
      if (editingUser) {
        await updateUser(editingUser.id, {
          name,
          email,
          role,
          ...(password ? { password } : {}),
        });
        setSuccess("User updated successfully.");
      } else {
        await createUser({ name, email, password, role });
        setSuccess("User created successfully.");
      }
      resetForm();
      await loadUsers();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.body.message);
        setFieldErrors(getFieldErrors(err));
      } else {
        setError(editingUser ? "Failed to update user." : "Failed to create user.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2>Team Members</h2>
          <p className="page-subtitle">Onboard and manage admins and support agents</p>
        </div>
      </div>

      <ErrorBanner message={error} />
      {success && <div className="success-banner" role="status">{success}</div>}

      <div className="page-grid">
        <section className="panel">
          <div className="panel-header">
            <h3>{editingUser ? "Edit User" : "Add User"}</h3>
            <p>
              {editingUser
                ? `Updating ${editingUser.name}. Leave password blank to keep it unchanged.`
                : "New users can sign in immediately with the password you set."}
            </p>
          </div>
          <form onSubmit={handleSubmit} className="stacked-form">
            <div className="form-group">
              <label htmlFor="user-name">Full name</label>
              <input
                id="user-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Jane Smith"
                required
              />
              {fieldErrors.name && <div className="field-error">{fieldErrors.name}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="user-email">Email address</label>
              <input
                id="user-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jane@company.com"
                required
              />
              {fieldErrors.email && <div className="field-error">{fieldErrors.email}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="user-password">
                {editingUser ? "New password (optional)" : "Temporary password"}
              </label>
              <input
                id="user-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={editingUser ? "Leave blank to keep current" : "Min. 6 characters"}
                minLength={editingUser ? undefined : 6}
                required={!editingUser}
              />
              {fieldErrors.password && <div className="field-error">{fieldErrors.password}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="user-role">Role</label>
              <select
                id="user-role"
                value={role}
                onChange={(e) => setRole(e.target.value as UserRole)}
              >
                <option value="agent">Support</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div className="form-actions form-actions-start">
              {editingUser && (
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={resetForm}
                  disabled={submitting}
                >
                  Cancel
                </button>
              )}
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting
                  ? editingUser
                    ? "Saving…"
                    : "Creating…"
                  : editingUser
                    ? "Save Changes"
                    : "Create User"}
              </button>
            </div>
          </form>
        </section>

        <section className="panel panel-table">
          <div className="panel-header">
            <h3>All Users</h3>
            <p>{users.length} team member{users.length === 1 ? "" : "s"}</p>
          </div>
          {loading ? (
            <div className="loading-state">Loading users…</div>
          ) : users.length === 0 ? (
            <div className="empty-state">No users found.</div>
          ) : (
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th aria-label="Actions" />
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id} className={editingUser?.id === u.id ? "row-selected" : ""}>
                      <td className="cell-strong">{u.name}</td>
                      <td>{u.email}</td>
                      <td>
                        <span className={`role-badge role-${u.role}`}>
                          {formatRole(u.role)}
                        </span>
                      </td>
                      <td className="cell-actions">
                        <button
                          type="button"
                          className="btn btn-ghost btn-sm"
                          onClick={() => startEdit(u)}
                          disabled={submitting}
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
