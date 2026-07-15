import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AdminRoute } from "./components/AdminRoute";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { CreateTicketPage } from "./pages/CreateTicketPage";
import { LoginPage } from "./pages/LoginPage";
import { TicketDetailPage } from "./pages/TicketDetailPage";
import { TicketListPage } from "./pages/TicketListPage";
import { UsersPage } from "./pages/UsersPage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/tickets" element={<TicketListPage />} />
            <Route path="/tickets/new" element={<CreateTicketPage />} />
            <Route path="/tickets/:id" element={<TicketDetailPage />} />
            <Route element={<AdminRoute />}>
              <Route path="/users" element={<UsersPage />} />
            </Route>
          </Route>
        </Route>
        <Route path="/" element={<Navigate to="/tickets" replace />} />
        <Route path="*" element={<Navigate to="/tickets" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
