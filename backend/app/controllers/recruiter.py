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

from datetime import datetime

from app.core.db import get_db


class RecruiterController:
    """Read-only summaries over saved interview reports for recruiter surfaces."""

    @staticmethod
    async def list_reports(*, role: str | None = None, limit: int = 50):
        db = get_db()
        query: dict = {}
        if role:
            query["role"] = role
        limit = max(1, min(int(limit), 200))

        cursor = (
            db.interview_reports.find(query, {"_id": 0})
            .sort("created_at", -1)
            .limit(limit)
        )

        reports = []
        async for doc in cursor:
            rep = doc.get("report", {}) or {}
            created = doc.get("created_at")
            reports.append(
                {
                    "session_id": doc.get("session_id"),
                    "role": doc.get("role") or rep.get("role"),
                    "interview_type": doc.get("interview_type"),
                    "score": rep.get("overall_score") or rep.get("average_score") or 0,
                    "status": rep.get("status", "completed"),
                    "created_at": created.isoformat() if isinstance(created, datetime) else created,
                }
            )

        return {"success": True, "reports": reports}
