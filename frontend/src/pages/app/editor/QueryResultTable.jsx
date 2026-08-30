import React from "react";
import { Table, CheckCircle, AlertCircle, Clock } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

export function QueryResultTable({ data, timeMs, error }) {
  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-950/20 p-4 text-xs font-mono text-red-300">
        <div className="flex items-center gap-2 mb-2 font-semibold text-red-400">
          <AlertCircle className="h-4 w-4" />
          <span>Query Execution Error</span>
        </div>
        <pre className="whitespace-pre-wrap">{error}</pre>
      </div>
    );
  }

  let parsed = data;
  if (typeof data === "string") {
    try {
      parsed = JSON.parse(data);
    } catch {
      parsed = null;
    }
  }

  if (!parsed || !Array.isArray(parsed) || parsed.length === 0) {
    return (
      <div className="rounded-lg border border-border/60 bg-zinc-900/40 p-4 text-center text-xs font-mono text-zinc-500">
        {data ? (
          <pre className="text-left text-zinc-300 overflow-x-auto">{typeof data === "string" ? data : JSON.stringify(data, null, 2)}</pre>
        ) : (
          "No records returned (0 rows)."
        )}
      </div>
    );
  }

  const columns = Object.keys(parsed[0] || {});

  return (
    <div className="rounded-lg border border-border/60 bg-zinc-950 overflow-hidden">
      {/* Header stats */}
      <div className="flex items-center justify-between px-3 py-2 bg-zinc-900/60 border-b border-border/60 text-[11px] font-mono text-zinc-400">
        <div className="flex items-center gap-2">
          <Table className="h-3.5 w-3.5 text-emerald-400" />
          <span className="font-semibold text-zinc-200">{parsed.length} Records</span>
        </div>
        {timeMs !== undefined && (
          <div className="flex items-center gap-1 text-zinc-500">
            <Clock className="h-3 w-3" />
            <span>{timeMs}ms</span>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto max-h-[300px]">
        <table className="w-full text-[11px] font-mono text-left text-zinc-300">
          <thead className="bg-zinc-800/60 text-zinc-400 uppercase sticky top-0 text-[10px]">
            <tr>
              {columns.map((col) => (
                <th key={col} className="px-3 py-2 border-b border-border/60 font-semibold">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {parsed.map((row, idx) => (
              <tr key={idx} className="border-b border-border/20 hover:bg-zinc-800/30 transition-colors">
                {columns.map((col) => (
                  <td key={col} className="px-3 py-1.5 whitespace-nowrap">
                    {row[col] === null ? (
                      <span className="text-zinc-600 italic">NULL</span>
                    ) : typeof row[col] === "object" ? (
                      JSON.stringify(row[col])
                    ) : (
                      String(row[col])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
