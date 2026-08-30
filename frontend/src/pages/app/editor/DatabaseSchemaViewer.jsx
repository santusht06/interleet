import React, { useState } from "react";
import { Database, Table, Eye, ChevronDown, ChevronRight, Layers, FileJson } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

export function DatabaseSchemaViewer({ schemaSql, fixtures, schemaJson, domain }) {
  const [expandedTables, setExpandedTables] = useState(() => {
    // Default expand first table
    if (fixtures && typeof fixtures === "object") {
      const keys = Object.keys(fixtures);
      return keys.length > 0 ? { [keys[0]]: true } : {};
    }
    return {};
  });

  const toggleTable = (name) => {
    setExpandedTables((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  const tables = fixtures && typeof fixtures === "object" ? Object.keys(fixtures) : [];

  return (
    <div className="flex h-full flex-col bg-zinc-950/80 border-t border-border lg:border-t-0 lg:border-l border-border/60">
      {/* Header */}
      <div className="flex h-10 items-center justify-between border-b border-border/60 px-4 bg-card/20">
        <div className="flex items-center gap-2 text-xs font-semibold text-zinc-300">
          <Database className="h-3.5 w-3.5 text-orange-500" />
          <span>Schema & Fixtures Inspector</span>
        </div>
        <Badge variant="outline" className="text-[10px] font-mono border-orange-500/30 text-orange-400 bg-orange-500/10">
          {tables.length} {tables.length === 1 ? "Entity" : "Entities"}
        </Badge>
      </div>

      {/* Content */}
      <ScrollArea className="flex-1 p-3">
        {tables.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 text-center text-muted-foreground text-xs">
            <Layers className="h-8 w-8 mb-2 opacity-30 text-zinc-400" />
            <p>No schema fixtures defined for this challenge.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tables.map((table) => {
              const rows = fixtures[table] || [];
              const isExpanded = !!expandedTables[table];
              const cols = rows.length > 0 && typeof rows[0] === "object" ? Object.keys(rows[0]) : [];

              return (
                <div key={table} className="rounded-lg border border-border/60 bg-zinc-900/50 overflow-hidden">
                  {/* Table Header Row */}
                  <button
                    onClick={() => toggleTable(table)}
                    className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-zinc-200 hover:bg-zinc-800/40 transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      {isExpanded ? (
                        <ChevronDown className="h-3.5 w-3.5 text-zinc-400" />
                      ) : (
                        <ChevronRight className="h-3.5 w-3.5 text-zinc-400" />
                      )}
                      <Table className="h-3.5 w-3.5 text-orange-400" />
                      <span className="font-mono font-semibold">{table}</span>
                    </div>
                    <span className="text-[11px] text-zinc-500 font-mono">
                      {rows.length} {rows.length === 1 ? "row" : "rows"}
                    </span>
                  </button>

                  {/* Table Body Preview */}
                  {isExpanded && (
                    <div className="border-t border-border/40 p-2 bg-zinc-950/40">
                      {rows.length > 0 && cols.length > 0 ? (
                        <div className="overflow-x-auto">
                          <table className="w-full text-[11px] text-left text-zinc-300 font-mono">
                            <thead className="bg-zinc-800/60 text-zinc-400 text-[10px] uppercase">
                              <tr>
                                {cols.map((col) => (
                                  <th key={col} className="px-2 py-1 border-b border-border/40 font-semibold">
                                    {col}
                                  </th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {rows.slice(0, 5).map((row, idx) => (
                                <tr key={idx} className="border-b border-border/20 hover:bg-zinc-800/20">
                                  {cols.map((col) => (
                                    <td key={col} className="px-2 py-1 max-w-[140px] truncate text-zinc-300">
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
                          {rows.length > 5 && (
                            <p className="text-[10px] text-zinc-500 text-center py-1 font-mono">
                              + {rows.length - 5} more rows
                            </p>
                          )}
                        </div>
                      ) : (
                        <pre className="text-[11px] font-mono text-zinc-400 p-2 overflow-x-auto">
                          {JSON.stringify(rows, null, 2)}
                        </pre>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </ScrollArea>
    </div>
  );
}
