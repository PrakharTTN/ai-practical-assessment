import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function navClass({ isActive }: { isActive: boolean }) {
  return isActive ? "nav-link active" : "nav-link";
}

export function Layout() {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <div className="app-logo" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" />
              <rect x="9" y="3" width="6" height="4" rx="1" />
              <path d="M9 12h6M9 16h4" />
            </svg>
          </div>
          <div>
            <Link to="/tickets" className="app-title">
              Support Desk
            </Link>
            <p className="app-tagline">Ticket management</p>
          </div>
        </div>

        <nav className="app-nav">
          <NavLink to="/tickets" end className={navClass}>
            Tickets
          </NavLink>
          <NavLink to="/tickets/new" className={navClass}>
            New Ticket
          </NavLink>
          {isAdmin && (
            <NavLink to="/users" className={navClass}>
              Team
            </NavLink>
          )}
        </nav>

        <div className="app-user">
          {user && (
            <div className="user-chip">
              <span className="user-name">{user.name}</span>
              <span className={`role-badge role-${user.role}`}>
                {user.role === "admin" ? "Admin" : "Support"}
              </span>
            </div>
          )}
          <button type="button" className="btn btn-ghost" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </header>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
