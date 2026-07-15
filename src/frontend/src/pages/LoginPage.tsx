import { FormEvent, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { ApiError, getFieldErrors } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { ErrorBanner } from "../components/ErrorBanner";

export function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname ?? "/tickets";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setFieldErrors({});
    setLoading(true);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.body.message);
        setFieldErrors(getFieldErrors(err));
      } else {
        setError("Unable to connect to the server.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-shell">
      <main className="login-page">
        <div className="login-brand">
          <div className="login-logo" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" />
              <rect x="9" y="3" width="6" height="4" rx="1" />
              <path d="M9 12h6M9 16h4" />
            </svg>
          </div>
          <h1>Support Desk</h1>
          <p className="login-tagline">Sign in to manage support tickets</p>
        </div>

        <div className="login-card">
          <h2>Welcome back</h2>
          <p className="login-subtitle">Enter your credentials to continue</p>

          <ErrorBanner message={error} />

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="email">Email address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                required
                autoComplete="username"
                autoFocus
              />
              {fieldErrors.email && <div className="field-error">{fieldErrors.email}</div>}
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                autoComplete="current-password"
              />
            </div>
            <button type="submit" className="btn btn-primary btn-login" disabled={loading}>
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>
        </div>

        <p className="login-footer">Support Ticket Management System</p>
      </main>
    </div>
  );
}
