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
Database Executor — runs SQL (PostgreSQL, MySQL, SQLite) and NoSQL (MongoDB, Redis) queries
inside the isolated `interleet-database` sandbox.
"""

import json
import logging
import aiofiles
from pathlib import Path
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor
from app.engine.schemas import SandboxResult, TestCaseSchema

logger = logging.getLogger(__name__)


class DatabaseExecutor(BaseExecutor):
    language = Language.SQL
    docker_image = "interleet-database:latest"
    filename = "solution.sql"
    compile_command = None
    run_command = ["python3", "/app/runner.py"]
    requires_compile = False

    def __init__(self, language: Language = Language.SQL):
        self.language = language
        if language in [Language.MONGODB]:
            self.filename = "solution.json"
        elif language in [Language.REDIS]:
            self.filename = "solution.txt"
        else:
            self.filename = "solution.sql"

    async def _write_code(self, workspace: Path, code: str, time_limit: float = 5.0) -> None:
        """Write user query file."""
        code_content = code
        # If code is passed as JSON object of files
        try:
            parsed = json.loads(code)
            if isinstance(parsed, dict):
                # Pick the query file
                for k in ["solution.sql", "solution.json", "solution.txt", "query.sql", "query.json"]:
                    if k in parsed:
                        code_content = parsed[k]
                        break
                else:
                    code_content = list(parsed.values())[0] if parsed else code
        except Exception:
            code_content = code

        async with aiofiles.open(workspace / self.filename, "w", encoding="utf-8") as f:
            await f.write(code_content)
        (workspace / self.filename).chmod(0o644)

    async def _write_stdin(self, workspace: Path, stdin_data: str) -> None:
        """Write configuration, schema and fixtures into stdin."""
        async with aiofiles.open(workspace / "stdin.txt", "w", encoding="utf-8") as f:
            await f.write(stdin_data or "{}")
        (workspace / "stdin.txt").chmod(0o644)
