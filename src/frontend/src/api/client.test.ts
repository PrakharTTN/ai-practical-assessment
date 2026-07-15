import { describe, expect, it, beforeEach } from "vitest";
import { ApiError, getFieldErrors, getToken, setToken, clearToken } from "./client";

describe("getFieldErrors", () => {
  it("maps validation details to first message per field", () => {
    const error = new ApiError(422, {
      error: "validation_error",
      message: "Request validation failed",
      details: {
        title: ["Field required"],
        priority: ["Invalid enum"],
      },
    });
    expect(getFieldErrors(error)).toEqual({
      title: "Field required",
      priority: "Invalid enum",
    });
  });
});

describe("token storage", () => {
  beforeEach(() => {
    clearToken();
  });

  it("stores and retrieves JWT from sessionStorage", () => {
    setToken("test-jwt");
    expect(getToken()).toBe("test-jwt");
  });

  it("clears token on logout", () => {
    setToken("test-jwt");
    clearToken();
    expect(getToken()).toBeNull();
  });
});
