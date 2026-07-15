import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function AdminRoute() {
  const { isAdmin, loading } = useAuth();

  if (loading) {
    return <div className="loading-state">Loading…</div>;
  }

  if (!isAdmin) {
    return <Navigate to="/tickets" replace />;
  }

  return <Outlet />;
}
