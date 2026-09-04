/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Sentry & Production Runtime Error Monitoring Client
 */

import * as Sentry from "@sentry/react";

const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN;

export function initSentry() {
  if (!SENTRY_DSN) {
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.info("[Monitoring] Sentry DSN not provided (VITE_SENTRY_DSN). Running in local logging mode.");
    }
    return;
  }

  try {
    Sentry.init({
      dsn: SENTRY_DSN,
      environment: import.meta.env.MODE || "production",
      integrations: [
        Sentry.browserTracingIntegration(),
        Sentry.replayIntegration({
          maskAllText: false,
          blockAllMedia: false,
        }),
      ],
      tracesSampleRate: import.meta.env.PROD ? 0.2 : 1.0,
      replaysSessionSampleRate: 0.1,
      replaysOnErrorSampleRate: 1.0,
    });
    // eslint-disable-next-line no-console
    console.info("[Monitoring] Sentry initialized successfully.");
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error("[Monitoring] Failed to initialize Sentry:", err);
  }
}

export function captureException(error, context = {}) {
  // eslint-disable-next-line no-console
  console.error("[Interleet Runtime Exception Captured]", error, context);
  if (SENTRY_DSN) {
    try {
      Sentry.captureException(error, { extra: context });
    } catch (_) {}
  }
}

export function captureMessage(message, level = "info") {
  if (SENTRY_DSN) {
    try {
      Sentry.captureMessage(message, level);
    } catch (_) {}
  }
}

export { Sentry };
