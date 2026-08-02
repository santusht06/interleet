// Copyright 2026 Sharexpress Contributors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { useState } from "react";
import { Lightbulb, Sparkles, Loader2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { API } from "@/api/api";

/**
 * AI hints + post-submission code review for the editor toolbar.
 * Self-contained: renders two buttons and shows the model's reply in a
 * floating panel (absolutely positioned so it never disturbs the toolbar).
 */
export default function AiAssist({ slug, code, language, stderr }) {
  const [loading, setLoading] = useState(null); // "hint" | "review" | null
  const [error, setError] = useState("");
  const [result, setResult] = useState(null); // { kind, text }

  const call = async (kind) => {
    setLoading(kind);
    setError("");
    try {
      const url = kind === "hint" ? "/api/ai/hint" : "/api/ai/review";
      const { data } = await API.post(url, {
        problem_slug: slug,
        code: code || "",
        language: language || "",
        ...(kind === "review" ? { stderr: stderr || "" } : {}),
      });
      setResult({ kind, text: (kind === "hint" ? data.hint : data.review) || "" });
    } catch (e) {
      setError(e?.response?.data?.detail || "Something went wrong. Please try again.");
      setResult(null);
    } finally {
      setLoading(null);
    }
  };

  const dismiss = () => {
    setResult(null);
    setError("");
  };

  return (
    <div className="relative flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={() => call("hint")}
        disabled={loading !== null}
        className="flex-1 sm:flex-none"
      >
        {loading === "hint" ? (
          <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
        ) : (
          <Lightbulb className="mr-1.5 h-3.5 w-3.5" />
        )}
        Hint
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => call("review")}
        disabled={loading !== null}
        className="flex-1 sm:flex-none"
      >
        {loading === "review" ? (
          <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
        ) : (
          <Sparkles className="mr-1.5 h-3.5 w-3.5" />
        )}
        AI Review
      </Button>

      {(result || error) && (
        <div className="absolute right-0 top-full z-50 mt-2 w-[22rem] max-w-[90vw] max-h-80 overflow-auto rounded-lg border border-border bg-popover p-3 text-xs leading-relaxed shadow-xl">
          <div className="mb-1.5 flex items-center justify-between">
            <span className="font-semibold text-primary">
              {result?.kind === "review" ? "AI Review" : "Hint"}
            </span>
            <button
              type="button"
              onClick={dismiss}
              className="text-muted-foreground hover:text-foreground"
              aria-label="Dismiss"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
          {error ? (
            <div className="text-destructive">{error}</div>
          ) : (
            <div className="whitespace-pre-wrap text-foreground/90">{result.text}</div>
          )}
        </div>
      )}
    </div>
  );
}
