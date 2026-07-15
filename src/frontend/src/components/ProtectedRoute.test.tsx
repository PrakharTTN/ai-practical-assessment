import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { ProtectedRoute } from "./ProtectedRoute";

const mockUseAuth = vi.fn();

vi.mock("../context/AuthContext", () => ({
  useAuth: () => mockUseAuth(),
}));

function renderProtected(initialPath = "/tickets") {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route path="/login" element={<div>Login Page</div>} />
        <Route element={<ProtectedRoute />}>
          <Route path="/tickets" element={<div>Tickets Page</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("ProtectedRoute", () => {
  beforeEach(() => {
    mockUseAuth.mockReset();
    mockUseAuth.mockReturnValue({ isAuthenticated: false, loading: false });
  });

  it("redirects unauthenticated users to login", () => {
    mockUseAuth.mockReturnValue({ isAuthenticated: false, loading: false });
    renderProtected();
    expect(screen.getByText("Login Page")).toBeInTheDocument();
  });

  it("renders child route when authenticated", () => {
    mockUseAuth.mockReturnValue({ isAuthenticated: true, loading: false });
    renderProtected();
    expect(screen.getByText("Tickets Page")).toBeInTheDocument();
  });
});
