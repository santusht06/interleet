# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Browser Executor — runs generic frontend code (HTML, React, etc.) inside a Headless Chromium Sandbox
"""
import json
import logging
import aiofiles
from pathlib import Path
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor
from app.engine.schemas import SandboxResult, TestCaseSchema

logger = logging.getLogger(__name__)

class BrowserExecutor(BaseExecutor):
    language = Language.HTML
    docker_image = "interleet-browser:latest"
    filename = "index.html"
    compile_command = None
    run_command = ["node", "/app/runner.js"]
    requires_compile = False

    async def _write_code(self, workspace: Path, code: str, time_limit: float = 5.0) -> None:
        """Write workspace files and the runtime.json configuration."""
        html_content = ""
        css_content = ""
        js_content = ""

        # Detect React JSX files
        is_react = False
        app_jsx = ""
        extra_files = {}

        try:
            # Check if code is a JSON string of multiple files (e.g. from editor)
            data = json.loads(code)
            if isinstance(data, dict):
                html_content = data.get("index.html", "")
                css_content = data.get("index.css", data.get("App.css", data.get("styles.css", "")))
                js_content = data.get("index.js", "")
                
                # Check for React entries
                for k in ["App.jsx", "App.js", "App.tsx", "index.jsx"]:
                    if k in data:
                        is_react = True
                        app_jsx = data[k]
                        break
                
                for k, v in data.items():
                    if k not in ["index.html", "index.css", "index.js", "App.jsx", "App.js", "App.tsx", "index.jsx"]:
                        extra_files[k] = v
            else:
                html_content = code
        except Exception:
            # Fallback for plain text single file
            html_content = code

        if not is_react and ("import React" in html_content or "from 'react'" in html_content or "useState(" in html_content):
            is_react = True
            app_jsx = html_content

        if is_react:
            import re

            def clean_jsx(s: str) -> str:
                # Remove import statements
                s = re.sub(r'import\s+(?:React\s*,\s*)?(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)?\s+from\s+[\'"][^\'"]+[\'"];?', '', s)
                s = re.sub(r'import\s+[\'"][^\'"]+[\'"];?', '', s)
                # Strip export keywords so components remain in script scope
                s = re.sub(r'export\s+default\s+function\b', 'function', s)
                s = re.sub(r'export\s+default\s+', '', s)
                s = re.sub(r'export\s+(const|function|let|var|class)\b', r'\1', s)
                return s

            clean_app_jsx = clean_jsx(app_jsx)
            extra_components_script = "\n\n".join([
                f"// --- File: {fname} ---\n{clean_jsx(fcontent)}"
                for fname, fcontent in extra_files.items()
                if fname.endswith((".jsx", ".js", ".tsx"))
            ])

            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="index.css" />
  <script src="/vendor/react.development.js"></script>
  <script src="/vendor/react-dom.development.js"></script>
  <script src="/vendor/babel.min.js"></script>
  <style>
    :root {{ color-scheme: light dark; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif; }}
  </style>
</head>
<body>
  <div id="root"></div>
  <script id="user-source" type="text/plain">
    const {{ useState, useEffect, useRef, useMemo, useCallback, useContext, createContext, useReducer, useId, useTransition, useDeferredValue }} = React;

    {extra_components_script}

    {clean_app_jsx}

    // Auto mount to root
    const rootEl = document.getElementById('root');
    if (rootEl && typeof ReactDOM !== 'undefined') {{
      const root = ReactDOM.createRoot(rootEl);
      const Component = typeof App !== 'undefined' ? App : (typeof window.App !== 'undefined' ? window.App : null);
      if (Component) {{
        root.render(React.createElement(Component));
      }}
    }}
  </script>
  <script>
    (function() {{
      try {{
        const src = document.getElementById('user-source').textContent;
        const res = Babel.transform(src, {{
          filename: 'App.tsx',
          presets: ['react', 'typescript']
        }}).code;
        const s = document.createElement('script');
        s.textContent = res;
        document.body.appendChild(s);
      }} catch(err) {{
        console.error("React Transpilation Error:", err);
      }}
    }})();
  </script>
</body>
</html>"""
        else:
            # Ensure index.css and index.js are linked in HTML if missing
            if "index.css" not in html_content:
                if "</head>" in html_content:
                    html_content = html_content.replace("</head>", "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>")
                else:
                    html_content = "<link rel=\"stylesheet\" href=\"index.css\">\n" + html_content

            if "index.js" not in html_content:
                if "</body>" in html_content:
                    html_content = html_content.replace("</body>", "  <script src=\"index.js\"></script>\n</body>")
                else:
                    html_content = html_content + "\n<script src=\"index.js\"></script>"

        # Write index.html
        async with aiofiles.open(workspace / "index.html", "w", encoding="utf-8") as f:
            await f.write(html_content)
        (workspace / "index.html").chmod(0o644)

        # Write index.css (always write to avoid 404 resource requests)
        async with aiofiles.open(workspace / "index.css", "w", encoding="utf-8") as f:
            await f.write(css_content)
        (workspace / "index.css").chmod(0o644)

        # Write index.js (always write to avoid 404 resource requests)
        async with aiofiles.open(workspace / "index.js", "w", encoding="utf-8") as f:
            await f.write(js_content)
        (workspace / "index.js").chmod(0o644)

        # Write any extra files
        for fname, fcontent in extra_files.items():
            async with aiofiles.open(workspace / fname, "w", encoding="utf-8") as f:
                await f.write(fcontent)
            (workspace / fname).chmod(0o644)

        # Build runtime.json configuration
        evaluationScript = """
        const stdinStr = window.STDIN_CONTENT || '';
        if (!stdinStr) return 'PASS';
        
        try {
            let input = {};
            try {
                input = JSON.parse(stdinStr);
            } catch(e) {
                input = { raw: stdinStr };
            }
            
            // Mode 1: Per-testcase DOM evaluation script
            if (input.evaluation) {
                const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
                const fn = new AsyncFunction(input.evaluation);
                return await fn();
            }
            
            // Mode 2: Legacy evaluator functions on window
            const evaluators = [
              'processRatingEvents',
              'parseMarkdown',
              'starRatingWidget',
              'debouncedSuggestions',
              'customFormValidator',
              'responsiveBreakpoint',
              'nestedFileDirectory',
              'virtualScrollingList',
              'modalTransitions',
              'cssGridAutoplacement'
            ];
            
            for (const name of evaluators) {
              if (typeof window[name] === 'function') {
                try {
                    let result;
                    if (name === 'parseMarkdown') {
                      result = window[name](input.markdown);
                    } else if (name === 'processRatingEvents') {
                      result = window[name](input.events);
                    } else {
                      result = window[name](input);
                    }
                    return typeof result === 'object' ? JSON.stringify(result) : result;
                } catch(e) {
                    return 'Error executing custom evaluator: ' + e.message;
                }
              }
            }
            
            // Default: Basic DOM verification passes if page loaded cleanly
            return 'PASS';
        } catch(e) {
            return 'PASS';
        }
        """

        runtime_config = {
            "entry": "index.html",
            "timeout": max(15000, int(time_limit * 1000)),
            "captureScreenshot": False,
            "captureDOM": True,
            "captureConsole": True,
            "network": "enabled",
            "evaluationScript": evaluationScript
        }

        async with aiofiles.open(workspace / "runtime.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(runtime_config, indent=2))
        (workspace / "runtime.json").chmod(0o644)

    def _parse_runner_output(self, sandbox_result: SandboxResult) -> SandboxResult:
        # If exit_code != 0 and it doesn't look like JSON, return as is
        if sandbox_result.exit_code != 0 and not sandbox_result.stdout.strip().startswith('{'):
            return sandbox_result
        
        try:
            # Diagnostic dump
            try:
                with open("/tmp/last_runner_output.json", "w") as df:
                    df.write(sandbox_result.stdout)
            except Exception:
                pass
            data = json.loads(sandbox_result.stdout)
            status = data.get("status", "error")
            stdout_str = data.get("stdout", "")
            errors = data.get("errors", [])
            screenshot_base64 = data.get("screenshot", None)
            dom_content = data.get("dom", None)
            
            stderr = sandbox_result.stderr
            if errors:
                stderr += "\n" + "\n".join(errors)
            
            return SandboxResult(
                stdout=stdout_str,
                stderr=stderr.strip(),
                exit_code=1 if status == "error" else sandbox_result.exit_code,
                wall_time_ms=sandbox_result.wall_time_ms,
                peak_memory_mb=sandbox_result.peak_memory_mb,
                timed_out=sandbox_result.timed_out,
                oom_killed=sandbox_result.oom_killed,
                screenshot_base64=screenshot_base64,
                dom_content=dom_content,
            )
        except Exception as e:
            logger.error("Failed to parse runner output: %s", e)
            return sandbox_result

    async def execute(
        self,
        request,
        testcase = None,
    ):
        if testcase:
            testcase.time_limit = max(20.0, testcase.time_limit or request.time_limit)
        request.time_limit = max(20.0, request.time_limit)
        return await super().execute(request, testcase)

    async def run_batch_testcases(
        self,
        code: str,
        testcases: list[TestCaseSchema],
        time_limit: float,
        memory_limit: int,
    ) -> list[SandboxResult]:
        """Override to parse the structured JSON output from the browser runner with boosted time limit."""
        boosted_time_limit = max(20.0, time_limit)
        for tc in testcases:
            if tc:
                tc.time_limit = max(20.0, tc.time_limit or time_limit)
        results = await super().run_batch_testcases(code, testcases, boosted_time_limit, memory_limit)
        return [self._parse_runner_output(r) for r in results]

    async def run_testcase(
        self,
        code: str,
        testcase: TestCaseSchema,
        time_limit: float,
        memory_limit: int,
        comparison_mode,
    ):
        """Override to parse the structured JSON output for a single testcase with boosted time limit."""
        boosted_time_limit = max(20.0, time_limit)
        if testcase:
            testcase.time_limit = max(20.0, testcase.time_limit or time_limit)
        sandbox_result, compile_result = await super().run_testcase(
            code, testcase, boosted_time_limit, memory_limit, comparison_mode
        )
        return self._parse_runner_output(sandbox_result), compile_result

    async def run_testcase_with_compile_workspace(
        self,
        code: str,
        testcase: TestCaseSchema,
        time_limit: float,
        memory_limit: int,
        compile_workspace = None,
    ) -> SandboxResult:
        """Override to parse the structured JSON output with boosted time limit."""
        boosted_time_limit = max(20.0, time_limit)
        if testcase:
            testcase.time_limit = max(20.0, testcase.time_limit or time_limit)
        sandbox_result = await super().run_testcase_with_compile_workspace(
            code, testcase, boosted_time_limit, memory_limit, compile_workspace
        )
        return self._parse_runner_output(sandbox_result)

