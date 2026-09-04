/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Global Error Boundary & Crash Recovery UI
 */

import React, { Component, useState } from "react";
import { useRouteError } from "react-router-dom";
import { AlertTriangle, RefreshCw, Home, Copy, Check, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { captureException } from "@/lib/sentry";

function ErrorFallbackView({ error, onReset }) {
  const [copied, setCopied] = useState(false);
  const [showStack, setShowStack] = useState(false);

  const errorMessage = error?.message || (typeof error === "string" ? error : "An unexpected application error occurred.");
  const errorStack = error?.stack || JSON.stringify(error, null, 2) || "";

  const handleCopy = async () => {
    try {
      const textToCopy = `[Interleet Crash Report]\nError: ${errorMessage}\nURL: ${window.location.href}\nTime: ${new Date().toISOString()}\n\nStack:\n${errorStack}`;
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch (_) {}
  };

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-[#0a0a0a] px-4 py-12 text-foreground selection:bg-orange-500/30">
      <div className="relative w-full max-w-xl overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950/80 p-8 shadow-2xl backdrop-blur-xl">
        {/* Ambient background glow */}
        <div className="pointer-events-none absolute -left-12 -top-12 h-40 w-40 rounded-full bg-red-500/10 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-12 -right-12 h-40 w-40 rounded-full bg-orange-500/10 blur-3xl" />

        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/10 text-red-400">
            <AlertTriangle className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">Something went wrong</h1>
            <p className="text-xs text-zinc-400">Interleet encountered an unexpected view error</p>
          </div>
        </div>

        {/* Error message box */}
        <div className="mt-6 rounded-lg border border-red-900/30 bg-red-950/20 p-4">
          <div className="font-mono text-xs font-semibold text-red-400">
            {error?.name || "ApplicationError"}:
          </div>
          <div className="mt-1 font-mono text-xs text-zinc-300 break-words">
            {errorMessage}
          </div>
        </div>

        {/* Action buttons */}
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <Button
            onClick={onReset || (() => window.location.reload())}
            className="flex items-center gap-2 bg-orange-500 text-white hover:bg-orange-600 shadow-sm"
          >
            <RefreshCw className="h-4 w-4" /> Try Again
          </Button>

          <Button
            variant="outline"
            onClick={() => (window.location.href = "/challenges")}
            className="flex items-center gap-2 border-zinc-800 text-zinc-300 hover:bg-zinc-900 hover:text-white"
          >
            <Home className="h-4 w-4" /> Challenges
          </Button>

          <Button
            variant="ghost"
            onClick={handleCopy}
            className="flex items-center gap-2 text-zinc-400 hover:text-white"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4 text-emerald-400" /> Copied Report
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" /> Copy Details
              </>
            )}
          </Button>
        </div>

        {/* Technical stack trace drawer */}
        {errorStack && (
          <div className="mt-6 border-t border-zinc-900 pt-4">
            <button
              onClick={() => setShowStack(!showStack)}
              className="flex items-center gap-1.5 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              {showStack ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
              {showStack ? "Hide Technical Details" : "View Technical Details"}
            </button>

            {showStack && (
              <pre className="mt-3 max-h-48 overflow-auto rounded-lg border border-zinc-900 bg-black/60 p-3 font-mono text-[11px] text-zinc-400">
                {errorStack}
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// React Router Route Error Boundary
export function RouteErrorBoundary() {
  const error = useRouteError();
  React.useEffect(() => {
    captureException(error, { context: "React Router ErrorBoundary" });
  }, [error]);

  return <ErrorFallbackView error={error} onReset={() => window.location.reload()} />;
}

// Component Error Boundary (Wraps entire React tree or individual widgets)
export class RootErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    captureException(error, { errorInfo, context: "RootErrorBoundary" });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onReset) {
      this.props.onReset();
    } else {
      window.location.reload();
    }
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback({ error: this.state.error, reset: this.handleReset });
      }
      return <ErrorFallbackView error={this.state.error} onReset={this.handleReset} />;
    }
    return this.props.children;
  }
}

export default RootErrorBoundary;
