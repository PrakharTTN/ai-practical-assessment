import { describe, expect, it } from "vitest";
import {
  formatPriority,
  formatStatus,
  getAllowedTransitions,
} from "./status";

describe("getAllowedTransitions", () => {
  it("returns valid next statuses for open", () => {
    expect(getAllowedTransitions("open")).toEqual(["in_progress", "cancelled"]);
  });

  it("returns valid next statuses for in_progress", () => {
    expect(getAllowedTransitions("in_progress")).toEqual(["resolved", "cancelled"]);
  });

  it("returns closed only from resolved", () => {
    expect(getAllowedTransitions("resolved")).toEqual(["closed"]);
  });

  it("returns empty for terminal states", () => {
    expect(getAllowedTransitions("closed")).toEqual([]);
    expect(getAllowedTransitions("cancelled")).toEqual([]);
  });

  it("does not allow skip-ahead transitions in UI options", () => {
    expect(getAllowedTransitions("open")).not.toContain("resolved");
    expect(getAllowedTransitions("open")).not.toContain("closed");
  });
});

describe("formatStatus", () => {
  it("replaces underscores with spaces", () => {
    expect(formatStatus("in_progress")).toBe("in progress");
  });
});

describe("formatPriority", () => {
  it("capitalizes priority label", () => {
    expect(formatPriority("high")).toBe("High");
  });
});
