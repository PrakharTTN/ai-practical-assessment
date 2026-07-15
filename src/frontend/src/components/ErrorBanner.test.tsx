import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ErrorBanner } from "./ErrorBanner";

describe("ErrorBanner", () => {
  it("renders nothing when message is null", () => {
    const { container } = render(<ErrorBanner message={null} />);
    expect(container.firstChild).toBeNull();
  });

  it("displays API error message", () => {
    render(<ErrorBanner message="Invalid email or password" />);
    expect(screen.getByRole("alert")).toHaveTextContent("Invalid email or password");
  });
});
