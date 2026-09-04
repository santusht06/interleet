import { describe, it, expect } from "vitest";
import {
  LANG_TO_MONACO,
  LANG_LABEL,
  LANG_BADGE,
  LANG_FILE,
  BACKEND_LANG_TO_SHORT,
  getStarter,
  getStarterWithDb,
} from "../pages/app/editor/editor.config";

describe("Editor Configuration & Language Mappings", () => {
  it("exports LANG_TO_MONACO and contains all expected language mappings", () => {
    expect(LANG_TO_MONACO).toBeDefined();
    expect(typeof LANG_TO_MONACO).toBe("object");

    // Strictly verify React and frontend mappings
    expect(LANG_TO_MONACO.jsx).toBe("javascript");
    expect(LANG_TO_MONACO.tsx).toBe("typescript");
    expect(LANG_TO_MONACO.react).toBe("javascript");

    // Standard programming languages
    expect(LANG_TO_MONACO.ts).toBe("typescript");
    expect(LANG_TO_MONACO.js).toBe("javascript");
    expect(LANG_TO_MONACO.py).toBe("python");
    expect(LANG_TO_MONACO.go).toBe("go");
    expect(LANG_TO_MONACO.sql).toBe("sql");
  });

  it("exports LANG_LABEL, LANG_BADGE, and LANG_FILE mappings", () => {
    expect(LANG_LABEL).toBeDefined();
    expect(LANG_LABEL.jsx).toContain("JSX");
    expect(LANG_LABEL.tsx).toContain("TSX");

    expect(LANG_BADGE).toBeDefined();
    expect(LANG_FILE).toBeDefined();
    expect(LANG_FILE.jsx).toBe("App.jsx");
    expect(LANG_FILE.tsx).toBe("App.tsx");
  });

  it("getStarter extracts code for given language from dbChallenge", () => {
    expect(typeof getStarter).toBe("function");
    const mockChallenge = {
      starter_code: {
        py: "def solution():\n    pass",
        ts: "export function solution() {}",
      },
    };

    const pyStarter = getStarter("two-sum", "py", mockChallenge);
    expect(pyStarter).toBe("def solution():\n    pass");

    const tsStarter = getStarter("two-sum", "ts", mockChallenge);
    expect(tsStarter).toBe("export function solution() {}");
  });

  it("getStarterWithDb handles multi-file starters for React JSX and TSX", () => {
    expect(typeof getStarterWithDb).toBe("function");
    const mockChallenge = {
      domain: "React",
      starter_code: {
        "App.jsx": "export default function App() {}",
        "App.tsx": "export default function App(): JSX.Element {}",
        "index.css": "/* style */",
      },
    };

    const jsxResult = getStarterWithDb("counter", "jsx", mockChallenge);
    expect(jsxResult.code).toBeDefined();
    const jsxFiles = JSON.parse(jsxResult.code);
    expect(jsxFiles["App.jsx"]).toBeDefined();
    expect(jsxFiles["index.css"]).toBeDefined();
    expect(jsxFiles["App.tsx"]).toBeUndefined();

    const tsxResult = getStarterWithDb("counter", "tsx", mockChallenge);
    expect(tsxResult.code).toBeDefined();
    const tsxFiles = JSON.parse(tsxResult.code);
    expect(tsxFiles["App.tsx"]).toBeDefined();
    expect(tsxFiles["index.css"]).toBeDefined();
    expect(tsxFiles["App.jsx"]).toBeUndefined();
  });
});
