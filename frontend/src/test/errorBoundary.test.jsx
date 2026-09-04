import { describe, it, expect, vi } from "vitest";
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { RootErrorBoundary } from "../components/common/RootErrorBoundary";

// A component that intentionally throws
function BuggyComponent({ shouldThrow }) {
  if (shouldThrow) {
    throw new ReferenceError("TEST_UNDEFINED_VARIABLE is not defined");
  }
  return <div>Component rendered successfully</div>;
}

describe("RootErrorBoundary (Crash Recovery & Monitoring)", () => {
  it("renders children when there are no errors", () => {
    render(
      <RootErrorBoundary>
        <BuggyComponent shouldThrow={false} />
      </RootErrorBoundary>
    );

    expect(screen.getByText("Component rendered successfully")).toBeInTheDocument();
  });

  it("catches ReferenceError and renders graceful crash recovery UI", () => {
    // Suppress console.error from React test runner
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});

    render(
      <RootErrorBoundary>
        <BuggyComponent shouldThrow={true} />
      </RootErrorBoundary>
    );

    expect(screen.getByText("Something went wrong")).toBeInTheDocument();
    expect(screen.getByText(/TEST_UNDEFINED_VARIABLE is not defined/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();

    spy.mockRestore();
  });
});
